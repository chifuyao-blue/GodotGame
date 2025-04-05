import cv2  # 导入OpenCV库，用于图像处理
import mediapipe as mp  # 导入MediaPipe库，用于人体姿态估计
import numpy as np  # 导入numpy库，用于数值计算
import socket  # 导入socket库，用于网络通信

cx1 = 0  # 定义一个全局变量，用于存储髋关节中心点X轴坐标的分类结果

class BufferList:
    def __init__(self, buffer_time, default_value=0):
        """初始化缓冲列表"""
        self.buffer = [default_value] * buffer_time  # 初始化一个固定长度的缓冲区

    def push(self, value):
        """更新缓冲区中的值"""
        self.buffer.pop(0)  # 移除第一个元素
        self.buffer.append(value)  # 添加新值到末尾

    def max(self):
        """返回缓冲区中的最大值"""
        return max(self.buffer)

    def min(self):
        """返回缓冲区中的最小值，忽略None值"""
        return min(filter(lambda x: x is not None, self.buffer), default=0)

    def smooth_update(self, old_value, new_value, alpha=0.5):
        """平滑更新旧值为新值"""
        return alpha * new_value + (1 - alpha) * old_value

# 初始化UDP套接字
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建一个UDP套接字
print(f"UDP服务器正在 {server_address} 上运行...")  # 打印提示信息，表示服务器已启动

# MediaPipe Holistic初始化
mp_holistic = mp.solutions.holistic  # 加载MediaPipe Holistic模块
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # 实例化Holistic对象
mp_drawing = mp.solutions.drawing_utils  # 加载绘图工具

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

cy_max, cy_min = 100, 100  # 初始化cy_max和cy_min
flip_flag = thresholds["flag_high"]  # 初始化翻转标志
jump_status = 1  # 默认状态为不跳跃
count = 0  # 计数器，未在代码中使用

cap = cv2.VideoCapture(0)  # 打开默认摄像头进行视频捕捉

def extract_landmarks(results, landmarks_indices, image_width, image_height):
    """从检测结果中提取特定地标的位置"""
    return [(lm.x * image_width, lm.y * image_height) for i, lm in enumerate(results.pose_landmarks.landmark) if i in landmarks_indices]

def calculate_center_y(hip_points, shoulder_points):
    """计算髋部和肩部的中心Y坐标"""
    cy_hip = int(np.mean([point[1] for point in hip_points]))  # 髋部中心Y坐标
    cy_shoulder = int(np.mean([point[1] for point in shoulder_points]))  # 肩部中心Y坐标
    return cy_hip, cy_hip - cy_shoulder  # 返回髋部中心Y坐标和髋部与肩部之间的距离

def update_counters(cy, cy_shoulder_hip, cy_max, cy_min, flip_flag, thresholds):
    """根据当前Y坐标更新计数器"""
    dy = cy_max - cy_min  # Y坐标范围
    if dy > thresholds["dy_ratio"] * cy_shoulder_hip:  # 如果范围超过阈值
        if cy > cy_max - thresholds["up_ratio"] * dy and flip_flag == thresholds["flag_low"]:
            flip_flag = thresholds["flag_high"]  # 更新翻转标志为高
        elif cy < cy_min + thresholds["down_ratio"] * dy and flip_flag == thresholds["flag_high"]:
            flip_flag = thresholds["flag_low"]  # 更新翻转标志为低
    return flip_flag

while cap.isOpened():
    success, image = cap.read()  # 读取一帧图像
    if not success: break  # 如果读取失败则退出循环
    image = cv2.flip(image, 1)  # 水平翻转图像
    cv2.imshow("Image",image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 将BGR图像转换为RGB
    results = holistic.process(image_rgb)  # 处理图像以获取人体姿态估计结果

    if results.pose_landmarks:
        hip_points = extract_landmarks(results, [23, 24], image.shape[1], image.shape[0])  # 提取髋部地标
        shoulder_points = extract_landmarks(results, [11, 12], image.shape[1], image.shape[0])  # 提取肩部地标
        cx = int(np.mean([point[0] for point in hip_points]))  # 计算髋部中心X坐标
        if 20<cx<290:
            cx1 = 1  # 根据X坐标分类
        elif 300<cx<500:
            cx1 = 2
        elif 500<cx:
            cx1 = 3
        cy, _ = calculate_center_y(hip_points, shoulder_points)  # 计算髋部中心Y坐标和髋部与肩部之间的距离

        buffers["center_y"].push(cy)  # 更新缓冲区中的Y坐标
        cy_max = buffers["center_y"].smooth_update(cy_max, buffers["center_y"].max())  # 平滑更新cy_max
        cy_min = buffers["center_y"].smooth_update(cy_min, buffers["center_y"].min())  # 平滑更新cy_min

        prev_flip_flag = flip_flag
        flip_flag = update_counters(cy, _, cy_max, cy_min, flip_flag, thresholds)  # 更新翻转标志
        jump_status = 2 if prev_flip_flag < flip_flag else 1  # 根据翻转标志判断是否跳跃

        print(f"髋关节中心点X轴坐标: {cx1:.4f}, 状态: {'跳跃' if jump_status == 2 else '不跳'}")
        message = f"1,{cx1},{jump_status}"  # 有人时发送1,cx,jump_status
    else:
        print("没有人")
        jump_status = 1  # 当没有人时，默认状态为不跳跃
        message = "0"  # 没有时发送0

    sock.sendto(message.encode(), server_address)  # 发送消息至指定服务器地址

    if cv2.waitKey(5) & 0xFF == 27: break  # 按ESC键退出循环

cap.release()  # 释放摄像头资源
cv2.destroyAllWindows()  # 关闭所有窗口
sock.close()  # 关闭UDP套接字