import cv2
import mediapipe as mp
import numpy as np
import socket

class BufferList:
    def __init__(self, buffer_time, default_value=0):
        self.buffer = [default_value] * buffer_time

    def push(self, value):
        self.buffer.pop(0)
        self.buffer.append(value)

    def max(self):
        return max(self.buffer)

    def min(self):
        return min(filter(lambda x: x is not None, self.buffer), default=0)

    def smooth_update(self, old_value, new_value, alpha=0.5):
        return alpha * new_value + (1 - alpha) * old_value

# 初始化UDP套接字
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"UDP服务器正在 {server_address} 上运行...")

# MediaPipe Holistic初始化
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 阈值设置
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
jump_status = 1  # 默认状态为不跳跃
count = 0

cap = cv2.VideoCapture(0)

def extract_landmarks(results, landmarks_indices, image_width, image_height):
    return [(lm.x * image_width, lm.y * image_height) for i, lm in enumerate(results.pose_landmarks.landmark) if i in landmarks_indices]

def calculate_center_y(hip_points, shoulder_points):
    cy_hip = int(np.mean([point[1] for point in hip_points]))
    cy_shoulder = int(np.mean([point[1] for point in shoulder_points]))
    return cy_hip, cy_hip - cy_shoulder

def update_counters(cy, cy_shoulder_hip, cy_max, cy_min, flip_flag, thresholds):
    dy = cy_max - cy_min
    if dy > thresholds["dy_ratio"] * cy_shoulder_hip:
        if cy > cy_max - thresholds["up_ratio"] * dy and flip_flag == thresholds["flag_low"]:
            flip_flag = thresholds["flag_high"]
        elif cy < cy_min + thresholds["down_ratio"] * dy and flip_flag == thresholds["flag_high"]:
            flip_flag = thresholds["flag_low"]
    return flip_flag

while cap.isOpened():
    success, image = cap.read()
    if not success: break
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image_rgb)

    if results.pose_landmarks:
        hip_points = extract_landmarks(results, [23, 24], image.shape[1], image.shape[0])
        shoulder_points = extract_landmarks(results, [11, 12], image.shape[1], image.shape[0])
        cx = int(np.mean([point[0] for point in hip_points]))
        cy, _ = calculate_center_y(hip_points, shoulder_points)

        buffers["center_y"].push(cy)
        cy_max = buffers["center_y"].smooth_update(cy_max, buffers["center_y"].max())
        cy_min = buffers["center_y"].smooth_update(cy_min, buffers["center_y"].min())

        prev_flip_flag = flip_flag
        flip_flag = update_counters(cy, _, cy_max, cy_min, flip_flag, thresholds)
        jump_status = 2 if prev_flip_flag < flip_flag else 1

        print(f"髋关节中心点X轴坐标: {cx:.4f}, 状态: {'跳跃' if jump_status == 2 else '不跳'}")
    else:
        print("没有人")
        jump_status = 1  # 当没有人时，默认状态为不跳跃

    message = f"{jump_status}"
    sock.sendto(message.encode(), server_address)

    if cv2.waitKey(5) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()
sock.close()