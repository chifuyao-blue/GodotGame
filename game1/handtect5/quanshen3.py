import cv2
import mediapipe as mp
import time

def process_video_and_return_result(frame_count=100):
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
        return None

    result1 = 0
    frame_index = 0

    while cap.isOpened() and frame_index < frame_count:
        ret, frame = cap.read()
        if not ret:
            print("到达视频结尾或读取帧失败。")
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

        # 根据mid_x的值更新result1
        if 0.99 > mid_x > 0.73:
            result1 = 1
        elif 0.09 < mid_x < 0.37:
            result1 = 2
        elif 0.37 < mid_x < 0.73:
            result1 = 3
        elif mid_x == 0:
            result1 = 0

        # 在帧上绘制脸部、姿态和手部地标（这里为了性能考虑可以注释掉）
        # if results.face_landmarks:
        #     mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)
        # if results.pose_landmarks:
        #     mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        # if results.left_hand_landmarks:
        #     mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # if results.right_hand_landmarks:
        #     mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # 显示带有地标的帧（这里为了函数返回结果考虑，注释掉显示部分）
        # cv2.imshow('Holistic Estimation', frame)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break

        frame_index += 1

    # 释放视频捕获对象
    cap.release()
    # cv2.destroyAllWindows()  # 如果不需要显示窗口，则不需要调用此行

    return result1

# 调用函数并打印结果
result = process_video_and_return_result()
print(f"Result1的值: {result}")