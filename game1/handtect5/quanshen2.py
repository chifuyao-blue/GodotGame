import cv2
import mediapipe as mp
import time
result1 = 0

class HolisticTracker:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5, interval=0.1):
        # 初始化 MediaPipe Holistic 解决方案。
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        # 加载视频文件或摄像头流。
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("错误：无法打开视频。")
            exit()

        self.last_time = time.time()  # 记录上次打印时间戳
        self.interval = interval  # 设置打印间隔时间

    def process_frame(self):
        """处理每一帧视频，计算状态值"""
        ret, frame = self.cap.read()
        if not ret:
            print("到达视频结尾。")
            return False, None, frame

        # 将帧水平翻转以获得自拍视图显示效果。
        frame = cv2.flip(frame, 1)

        # 将 BGR 图像转换为 RGB。
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 处理图像并检测整体（脸、手和身体）关键点。
        results = self.holistic.process(image_rgb)

        mid_x, mid_y = 0, 0  # 默认值为0

        status = None
        if results.pose_landmarks:  # 如果检测到身体姿态关键点
            # 获取左右髋关节坐标
            left_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_HIP]

            # 计算髋关节中点
            mid_x = (left_hip.x + right_hip.x) / 2
            mid_y = (left_hip.y + right_hip.y) / 2

        current_time = time.time()

        if mid_x > 0.73:
            status = 1
        elif mid_x < 0.37:
            status = 2
        else:
            status = 3
            self.last_time = current_time

        return True, status, frame, results

    def display_frame(self, frame, results):
        """在图像上绘制关键点，并显示处理后的视频帧"""
        if results.face_landmarks:  # 如果检测到脸部关键点
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(
                frame,
                results.face_landmarks,
                self.mp_holistic.FACEMESH_CONTOURS  # 使用面部轮廓连线
            )

        if results.pose_landmarks:  # 如果检测到身体姿态关键点
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_holistic.POSE_CONNECTIONS  # 使用姿态连接线
            )

        if results.left_hand_landmarks:  # 如果检测到左手关键点
            mp_drawing.draw_landmarks(
                frame,
                results.left_hand_landmarks,
                self.mp_holistic.HAND_CONNECTIONS  # 使用手部连接线
            )

        if results.right_hand_landmarks:  # 如果检测到右手关键点
            mp_drawing.draw_landmarks(
                frame,
                results.right_hand_landmarks,
                self.mp_holistic.HAND_CONNECTIONS  # 使用手部连接线
            )

        # 显示带有地标的帧。
        cv2.imshow('Holistic Estimation', frame)

    def get_status(self):
        """调用此方法处理一帧并返回状态值"""
        success, status, frame, results = self.process_frame()
        if success and status is not None:
            self.display_frame(frame, results)
        return status if success and status is not None else 0

# 示例使用：
if __name__ == "__main__":
    tracker = HolisticTracker()
    while True:
        status = tracker.get_status()
        print(status)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tracker.cap.release()
    cv2.destroyAllWindows()