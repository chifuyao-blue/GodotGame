import cv2
import mediapipe as mp
import time
import socket
import numpy as np
result1 = 0
result2 = 0
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"UDP服务器正在 {server_address} 上运行...")
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


def extract_landmarks(results, landmarks_indices, image_width, image_height):
    """提取指定关节的坐标"""
    return [
        (lm.x * image_width, lm.y * image_height)
        for i, lm in enumerate(results.pose_landmarks.landmark)
        if i in landmarks_indices
    ]


def calculate_center_y(hip_points, shoulder_points):
    """计算中心Y轴及肩-臀垂直距离"""
    cy_hip = int(np.mean([point[1] for point in hip_points]))
    cy_shoulder = int(np.mean([point[1] for point in shoulder_points]))
    return cy_hip, cy_hip - cy_shoulder


def update_counters(cy, cy_shoulder_hip, cy_max, cy_min, flip_flag, thresholds):
    """更新波动计数逻辑"""
    dy = cy_max - cy_min
    if dy > thresholds["dy_ratio"] * cy_shoulder_hip:
        if (
            cy > cy_max - thresholds["up_ratio"] * dy
            and flip_flag == thresholds["flag_low"]
        ):
            flip_flag = thresholds["flag_high"]
        elif (
            cy < cy_min + thresholds["down_ratio"] * dy
            and flip_flag == thresholds["flag_high"]
        ):
            flip_flag = thresholds["flag_low"]
    return flip_flag

# 初始化 MediaPipe Holistic 解决方案。
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,  # 最小检测置信度
    min_tracking_confidence=0.5  # 最小跟踪置信度
)
# 设置阈值
thresholds = {
    "buffer_time": 50,  # 缓冲区时间长度
    "dy_ratio": 0.3,  # Y轴移动幅度阈值
    "up_ratio": 0.55,  # 上升阶段阈值
    "down_ratio": 0.35,  # 下降阶段阈值
    "flag_low": 150,  # 翻转标志低点阈值
    "flag_high": 250,  # 翻转标志高点阈值
}
# 初始化缓冲区
buffers = {
    "center_y": (thresholds["buffer_time"]),  # 中心点Y坐标缓冲区
    "center_y_up": (thresholds["buffer_time"]),  # 中心点Y坐标上升阶段缓冲区
    "center_y_down": (thresholds["buffer_time"]),  # 中心点Y坐标下降阶段缓冲区
    "center_y_flip": (thresholds["buffer_time"]),  # 中心点Y坐标翻转检测缓冲区
    "center_y_pref_flip": (thresholds["buffer_time"]),  # 中心点Y坐标翻转前检测缓冲区（未使用）
}
# 初始化变量
cy_max, cy_min = 100, 100  # 中心点Y坐标的最大值和最小值
flip_flag = thresholds["flag_high"]  # 翻转标志初始值
count = 0  # 跳跃次数
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
    #print(f"已发送: {message}")
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
