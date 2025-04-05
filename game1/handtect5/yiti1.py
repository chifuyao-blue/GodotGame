import cv2
import mediapipe as mp
import socket
import time

class HolisticTracker:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5, interval=0.1):
        # 初始化 MediaPipe Holistic 解决方案。
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("错误：无法打开视频。")
            exit()
        self.last_time = time.time()  # 记录上次打印时间戳
        self.interval = interval  # 设置打印间隔时间
        self.server_address = ('127.0.0.1', 7777)  # UDP服务器地址和端口
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("到达视频结尾。")
            return False, None, frame

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(image_rgb)
        mid_x, mid_y = 0, 0

        status = None
        if results.pose_landmarks:
            left_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_HIP]
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

    def send_status_via_udp(self, status):
        """发送状态值到指定的UDP服务器"""
        message = str(status).encode('utf-8')
        self.sock.sendto(message, self.server_address)
        print(f"已发送: {status}")

    def get_status(self):
        success, status, frame, results = self.process_frame()
        if success and status is not None:
            self.display_frame(frame, results)
            self.send_status_via_udp(status)  # 发送状态值
        return status if success and status is not None else 0

if __name__ == "__main__":
    tracker = HolisticTracker()
    while True:
        status = tracker.get_status()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tracker.cap.release()
    cv2.destroyAllWindows()