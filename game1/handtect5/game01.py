import cv2
import json
import asyncio
import websockets


# 假设get_body_center_x是一个函数，它返回人体中心点在摄像头x轴上的位置（-20到20）
def get_body_center_x(frame):
    # 这里应该包含你的姿态估计算法逻辑来获取人体中心点的x坐标
    # 返回一个介于-20到20之间的值
    pass


async def send_data(uri):
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # 获取人体中心点x坐标
            center_x = get_body_center_x(frame)

            # 将数据转换为JSON字符串并发送
            await websocket.send(json.dumps({"center_x": center_x}))

            # 可选：显示图像以供调试
            # cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data('ws://localhost:8765'))