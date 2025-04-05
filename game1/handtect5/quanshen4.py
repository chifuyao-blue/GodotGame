import cv2
import mediapipe as mp
import socket
import time
import numpy as np

from tiaoyue2 import BufferList, extract_landmarks, calculate_center_y, update_counters

# UDP服务器配置
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"UDP服务器正在 {server_address} 上运行...")

# 初始化 MediaPipe Holistic 解决方案。
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 初始化 MediaPipe 绘图工具。
mp_drawing = mp.solutions.drawing_utils

# 加载视频文件或摄像头流。
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("错误：无法打开视频。")
    exit()

# 缓冲区和阈值设置
thresholds = {
    "buffer_time": 50,
    "dy_ratio": 0.3,
    "up_ratio": 0.55,
    "down_ratio": 0.35,
    "flag_low": 150,
    "flag_high": 250,
}

buffers = {
    "center_y": BufferList(thresholds["buffer_time"]),
    "center_y_up": BufferList(thresholds["buffer_time"]),
    "center_y_down": BufferList(thresholds["buffer_time"]),
    "center_y_flip": BufferList(thresholds["buffer_time"]),
    "center_y_pref_flip": BufferList(thresholds["buffer_time"]),
}

cy_max, cy_min = 100, 100
flip_flag = thresholds["flag_high"]
count = 0

last_time = time.time()  # 记录上次打印时间戳

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("到达视频结尾。")
        break

    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(image_rgb)

    mid_x, mid_y = 0, 0
    result1 = 0
    result4 = 0

    if results.pose_landmarks:
        left_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]

        mid_x = (left_hip.x + right_hip.x) / 2
        mid_y = (left_hip.y + right_hip.y) / 2

        if 0.99 > mid_x > 0.73:
            result1 = 1
        elif 0.09 < mid_x < 0.37:
            result1 = 2
        elif 0.37 < mid_x < 0.73:
            result1 = 3
        elif mid_x == 0:
            result1 = 0

        hip_points = extract_landmarks(results, [23, 24], frame.shape[1], frame.shape[0])
        shoulder_points = extract_landmarks(results, [11, 12], frame.shape[1], frame.shape[0])
        cx = int(np.mean([point[0] for point in hip_points]))
        cy, cy_shoulder_hip = calculate_center_y(hip_points, shoulder_points)

        buffers["center_y"].push(cy)
        cy_max = buffers["center_y"].smooth_update(cy_max, buffers["center_y"].max())
        cy_min = buffers["center_y"].smooth_update(cy_min, buffers["center_y"].min())

        prev_flip_flag = flip_flag
        flip_flag = update_counters(cy, cy_shoulder_hip, cy_max, cy_min, flip_flag, thresholds)
        if prev_flip_flag < flip_flag:
            result4 = 1
        else:
            result4 = 0
    print(result1,result4)
    message = f"{result1},{result4}"
    sent = sock.sendto(message.encode(), server_address)

    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS
        )

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS
        )

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
        )

    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
        )

    cv2.imshow('Holistic Estimation', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("服务器被手动停止")
        sock.close()
        break

cap.release()
cv2.destroyAllWindows()