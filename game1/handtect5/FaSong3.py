import cv2  # 导入OpenCV库，用于图像处理
import mediapipe as mp  # 导入MediaPipe库，用于人体姿态估计
import socket  # 导入socket库，用于网络通信
from cvzone.HandTrackingModule import HandDetector  # 从cvzone库导入手部检测模块
from cvzone.ClassificationModule import Classifier  # 从cvzone库导入分类模块
import numpy as np  # 导入numpy库，用于数值计算
import math  # 导入math库，用于数学运算
import time  # 导入time库，用于时间控制
import os
from collections import Counter  # 导入Counter用于统计出现次数

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 设置TensorFlow日志级别为3，禁用所有日志输出

# 定义全局变量
cx1 = 0  # 髋关节中心点X轴坐标的分类结果

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

# 初始化摄像头和手部检测器
cap = cv2.VideoCapture(0)  # 打开默认摄像头进行视频捕捉
detector = HandDetector(maxHands=1)  # 实例化手部检测器，设置最大检测手的数量为1
classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")  # 实例化分类器，指定模型路径和标签文件路径
offset = 20  # 定义偏移量，用于裁剪手部图像时增加边缘
imgSize = 300  # 定义图像尺寸，用于调整裁剪后的手部图像大小
labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]  # 定义类别标签列表

# 初始化UDP套接字
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建一个UDP套接字
print(f"UDP服务器正在 {server_address} 上运行...")  # 打印提示信息，表示服务器已启动

# 初始化UDP套接字
server_address2 = ('127.0.0.1', 7778)  # 指定服务器地址和端口
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建一个UDP套接字
print(f"UDP服务器正在 {server_address2} 上运行...")  # 打印提示信息，表示服务器已启动

# 初始化UDP套接字
server_address3 = ('127.0.0.1', 7779)  # 指定服务器地址和端口
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建一个UDP套接字
print(f"UDP服务器正在 {server_address3} 上运行...")  # 打印提示信息，表示服务器已启动

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

# 新增变量：用于存储前10次的标签值
recent_labels = []
true_label = None  # 初始化真值为None

# 辅助函数
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

# 控制发送频率的变量
last_send_time = time.time()  # 初始化上次发送的时间戳
send_interval = 1  # 设置发送间隔为0.2秒

last_send_time2 = time.time()  # 初始化上次发送的时间戳
send_interval2 = 0.3  # 设置发送间隔为0.2秒

# 主循环
while cap.isOpened():
    success, image = cap.read()  # 读取一帧图像
    if not success: break  # 如果读取失败则退出循环
    image = cv2.flip(image, 1)  # 水平翻转图像
    cv2.imshow("Image", image)
    img = image.copy()
    imgOutput = img.copy()  # 复制当前帧图像，用于后续绘制结果
    hands, img = detector.findHands(img)  # 在当前帧中查找手部
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 将BGR图像转换为RGB
    results = holistic.process(image_rgb)  # 处理图像以获取人体姿态估计结果

    if hands:  # 如果检测到手部
        hand = hands[0]  # 获取第一只手的信息
        x, y, w, h = hand['bbox']  # 获取手部边界框坐标
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # 创建一个白色背景的正方形图像
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # 根据边界框裁剪手部图像，并增加边缘
        imgCropShape = imgCrop.shape  # 获取裁剪后图像的形状

        aspectRatio = h / w  # 计算宽高比
        if aspectRatio > 1:  # 如果高度大于宽度
            k = imgSize / h  # 计算缩放比例
            wCal = math.ceil(k * w)  # 计算新的宽度
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))  # 调整裁剪图像大小
            imgResizeShape = imgResize.shape  # 获取调整后图像的形状
            wGap = math.ceil((imgSize - wCal) / 2)  # 计算填充宽度
            imgWhite[:, wGap:wCal + wGap] = imgResize  # 将调整后的图像放置于白色背景图像中央
        else:  # 如果宽度大于或等于高度
            k = imgSize / w  # 计算缩放比例
            hCal = math.ceil(k * h)  # 计算新的高度
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))  # 调整裁剪图像大小
            imgResizeShape = imgResize.shape  # 获取调整后图像的形状
            hGap = math.ceil((imgSize - hCal) / 2)  # 计算填充高度
            imgWhite[hGap:hCal + hGap, :] = imgResize  # 将调整后的图像放置于白色背景图像中央

        prediction, index = classifier.getPrediction(imgWhite, draw=False)  # 对白色背景上的手部图像进行预测
        cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50), (255, 0, 255),
                      cv2.FILLED)  # 绘制矩形框
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255),
                    2)  # 在图像上显示预测的手势标签
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255),
                      4)  # 在输出图像上绘制手部边界框
    else:
        index = 9

    # 更新 recent_labels 列表并计算真值
    if len(recent_labels) < 10:  # 如果还没有收集到10个标签
        recent_labels.append(labels[index])  # 添加当前标签
    else:  # 如果已经收集到10个标签
        # 统计出现次数最多的标签
        label_counts = Counter(recent_labels)
        true_label = label_counts.most_common(1)[0][0]  # 获取出现次数最多的标签
        # 移除最早的一个标签并添加新的标签
        recent_labels.pop(0)
        recent_labels.append(labels[index])

    # 使用真值发送消息
    if true_label is not None:
        message = f"{true_label}"  # 使用真值发送消息
    else:
        k = "k"
        message = f"{k}"  # 如果还没有真值，则使用当前值

    if results.pose_landmarks:
        hip_points = extract_landmarks(results, [23, 24], image.shape[1], image.shape[0])  # 提取髋部地标
        shoulder_points = extract_landmarks(results, [11, 12], image.shape[1], image.shape[0])  # 提取肩部地标
        cx = int(np.mean([point[0] for point in hip_points]))  # 计算髋部中心X坐标
        if 20 < cx < 290:
            cx1 = 1  # 根据X坐标分类
        elif 300 < cx < 400:
            cx1 = 2
        elif 400 < cx:
            cx1 = 3
        cy, _ = calculate_center_y(hip_points, shoulder_points)  # 计算髋部中心Y坐标和髋部与肩部之间的距离

        buffers["center_y"].push(cy)  # 更新缓冲区中的Y坐标
        cy_max = buffers["center_y"].smooth_update(cy_max, buffers["center_y"].max())  # 平滑更新cy_max
        cy_min = buffers["center_y"].smooth_update(cy_min, buffers["center_y"].min())  # 平滑更新cy_min

        prev_flip_flag = flip_flag
        flip_flag = update_counters(cy, _, cy_max, cy_min, flip_flag, thresholds)  # 更新翻转标志
        jump_status = 2 if prev_flip_flag < flip_flag else 1  # 根据翻转标志判断是否跳跃

        message2 = f"{labels[index]},{jump_status}"
        message3 = f"{cx1}"
    else:
        print("没有人")
        jump_status = 1  # 当没有人时，默认状态为不跳跃
        message = f"{k}"  # 没有时发送0
        message2 = f"{2},{jump_status}"

    sock.sendto(message2.encode(), server_address2)  # 发送消息至指定服务器地址
    # 控制发送频率
    current_time = time.time()
    if current_time - last_send_time >= send_interval:
        print(message)
        sock.sendto(message.encode(), server_address)  # 发送消息至指定服务器地址
        last_send_time = current_time  # 更新上次发送的时间戳

    current_time2 = time.time()
    if current_time2 - last_send_time2 >= send_interval2:
        sock.sendto(message3.encode(), server_address3)  # 发送消息至指定服务器地址
        last_send_time2 = current_time2  # 更新上次发送的时间戳

    if cv2.waitKey(5) & 0xFF == 27: break  # 按ESC键退出循环

# 释放资源
cap.release()  # 释放摄像头资源
cv2.destroyAllWindows()  # 关闭所有窗口
sock.close()  # 关闭UDP套接字