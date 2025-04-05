import socket
import random
from quanshen3 import process_video_and_return_result

def udp_server():
    server_address = ('127.0.0.1', 7777)  # 指定服务器地址和端口
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"UDP服务器正在 {server_address} 上运行...")


    try:
        while True:
            message = process_video_and_return_result()
            number_str = str(message)
            encoded_bytes = number_str.encode('utf-8')

            # 发送数据报
            sent = sock.sendto(number_str.encode(), server_address)
            print(f"已发送: {message}")
            # 为了避免过于频繁地发送数据，这里简单地sleep一段时间
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("服务器被手动停止")
    finally:
        sock.close()

if __name__ == '__main__':
    import time
    udp_server()