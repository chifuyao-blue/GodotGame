import cv2  # 导入OpenCV库，用于图像处理
from cvzone.HandTrackingModule import HandDetector  # 从cvzone库导入手部检测模块
from cvzone.ClassificationModule import Classifier  # 从cvzone库导入分类模块
import numpy as np  # 导入numpy库，用于数值计算
import math  # 导入math库，用于数学运算
import time  # 导入time库，用于时间操作
import socket  # 导入socket库，用于网络通信

# 初始化UDP套接字
server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建一个UDP套接字
print(f"UDP服务器正在 {server_address} 上运行...")  # 打印提示信息，表示服务器已启动

cap = cv2.VideoCapture(0)  # 打开默认摄像头进行视频捕捉
detector = HandDetector(maxHands=1)  # 实例化手部检测器，设置最大检测手的数量为1
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")  # 实例化分类器，指定模型路径和标签文件路径

offset = 20  # 定义偏移量，用于裁剪手部图像时增加边缘
imgSize = 300  # 定义图像尺寸，用于调整裁剪后的手部图像大小
counter = 0  # 计数器，未在代码中使用
labels = ["a", "b", "c","d"]  # 定义类别标签列表
folder = "Data/c"  # 数据存储文件夹，未在代码中使用

while True:  # 开始无限循环，持续处理每一帧图像
    success, img = cap.read()  # 读取一帧图像
    img = cv2.flip(img,1)  #反转镜头
    imgOutput = img.copy()  # 复制当前帧图像，用于后续绘制结果
    hands, img = detector.findHands(img)  # 在当前帧中查找手部

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
        print(prediction, index)  # 打印预测结果和索引
        cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50), (255, 0, 255),
                      cv2.FILLED)  # 绘制矩形框
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255),
                    2)  # 在图像上显示预测的手势标签
        # print(labels[index])  # 打印手势标签
        # print(index)  # 打印索引
        message = f"{labels[index]}"  # 构造要发送的消息
        sock.sendto(message.encode(), server_address)  # 发送消息至指定服务器地址
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255),
                      4)  # 在输出图像上绘制手部边界框
        # cv2.imshow("ImageCrop", imgCrop)
        # cv2.imshow("ImageWhite", imgWhite)
    else:
        index = 3
    print(labels[index])  # 打印手势标签
    print(index)  # 打印索引
    cv2.imshow("Image",imgOutput)
    # image1 = cv2.flip(imgOutput,1)
    # cv2.imshow("Image", image1)  # 显示输出图像
    cv2.waitKey(1)  # 等待按键事件，延迟1ms