import socket
import threading

# 定义服务器的IP和端口
HOST = 'localhost'  # 服务器地址，'localhost' 表示本机
PORT = 51235        # 更改端口号以避免冲突

# 处理客户端请求的函数
def handle_client(client_socket, client_address):
    print(f"新客户端连接: {client_address}")

    # 发送欢迎信息，将中文编码为UTF-8
    client_socket.send("欢迎连接到服务器！\n".encode('utf-8'))

    while True:
        try:
            # 接收客户端发送的消息
            request = client_socket.recv(1024)
            if not request:
                break
            print(f"收到来自 {client_address} 的消息: {request.decode()}")

            # 这里只是一个简单的回显示例
            client_socket.send(f"服务器响应: {request.decode()}\n".encode('utf-8'))

        except Exception as e:
            print(f"处理客户端 {client_address} 时发生错误: {e}")
            break

    # 关闭连接
    client_socket.close()
    print(f"客户端 {client_address} 断开连接")

# 启动服务器
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # 绑定IP和端口
    server_socket.listen(5)  # 最大连接数为5

    print(f"服务器正在 {HOST}:{PORT} 上等待连接...")

    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()

        # 为每个客户端创建一个新线程来处理请求
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# 启动服务器
if __name__ == "__main__":
    start_server()
