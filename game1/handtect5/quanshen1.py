import cv2
import mediapipe as mp
import time
import socket
result1 = 0
result2 = 0
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"UDP服务器正在 {server_address} 上运行...")
# 初始化 MediaPipe Holistic 解决方案。
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,  # 最小检测置信度
    min_tracking_confidence=0.5  # 最小跟踪置信度
)

# 初始化 MediaPipe 绘图工具，用于在图像上绘制地标。
mp_drawing = mp.solutions.drawing_utils

# 加载视频文件或摄像头流。
cap = cv2.VideoCapture(0)

# 检查视频是否成功打开。
if not cap.isOpened():
    print("错误：无法打开视频。")
    exit()

last_time = time.time()  # 记录上次打印时间戳
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("到达视频结尾。")
        break

    # 将帧水平翻转以获得自拍视图显示效果。
    frame = cv2.flip(frame, 1)

    # 将 BGR 图像转换为 RGB。
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 处理图像并检测整体（脸、手和身体）关键点。
    results = holistic.process(image_rgb)

    mid_x, mid_y = 0, 0  # 默认值为0

    if results.pose_landmarks:  # 如果检测到身体姿态关键点
        # 获取左右髋关节坐标
        left_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]

        # 计算髋关节中点
        mid_x = (left_hip.x + right_hip.x) / 2
        mid_y = (left_hip.y + right_hip.y) / 2


    if 0.99 > mid_x > 0.73:
       result1 = 1
    elif 0.09<mid_x < 0.37:
        result1 = 2
    elif 0.37< mid_x < 0.73:
        result1 = 3
    elif mid_x == 0:
        result1 = 0

    message = f"{result1}"
    number_str = str(message)
    encoded_bytes = number_str.encode('utf-8')
    # 发送数据报
    sent = sock.sendto(message.encode(), server_address)
    print(f"已发送: {message}")
       # print(f"髋关节中点坐标 - X: {mid_x:.4f}, Y: {mid_y:.4f}")
    # 在帧上绘制脸部、姿态和手部地标。
    if results.face_landmarks:  # 如果检测到脸部关键点
        mp_drawing.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS  # 使用面部轮廓连线
        )

    if results.pose_landmarks:  # 如果检测到身体姿态关键点
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS  # 使用姿态连接线
        )

    if results.left_hand_landmarks:  # 如果检测到左手关键点
        mp_drawing.draw_landmarks(
            frame,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS  # 使用手部连接线
        )

    if results.right_hand_landmarks:  # 如果检测到右手关键点
        mp_drawing.draw_landmarks(
            frame,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS  # 使用手部连接线
        )

    # 显示带有地标的帧。
    cv2.imshow('Holistic Estimation', frame)

    # 如果按下 'q' 键则退出循环。
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("服务器被手动停止")
        sock.close()
        break

# 释放视频捕获对象并关闭显示窗口。
cap.release()
cv2.destroyAllWindows()
