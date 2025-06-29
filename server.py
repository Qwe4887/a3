import socket
import threading

# 定义服务器的IP和端口
HOST = 'localhost'  # 服务器地址，'localhost' 表示本机
PORT = 51235  # 端口号，必须与客户端保持一致

# 存储元组空间
tuple_space = {}


# 处理客户端请求的函数
def handle_client(client_socket, client_address):
    print(f"新客户端连接: {client_address}")

    while True:
        try:
            # 接收客户端发送的请求
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break  # 如果没有请求，断开连接

            print(f"收到请求: {request}")
            # 解析请求
            response = handle_request(request)
            # 发送响应
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"处理客户端 {client_address} 时发生错误: {e}")
            break

    # 关闭连接
    client_socket.close()
    print(f"客户端 {client_address} 断开连接")


# 处理请求的函数
def handle_request(request):
    print(f"处理请求: {request}")  # 打印请求内容
    parts = request.split(" ", 1)
    if len(parts) < 2:
        return "无效的请求格式"

    command = parts[0]
    key_value = parts[1]

    if command == "PUT":
        key, value = key_value.split(" ", 1)
        tuple_space[key] = value
        print(f"PUT 请求处理: {key} -> {value}")  # 打印 PUT 请求的处理结果
        return f"OK ({key}, {value}) added"

    elif command == "GET":
        if key_value in tuple_space:
            value = tuple_space.pop(key_value)
            print(f"GET 请求处理: 删除 {key_value} -> {value}")  # 打印 GET 请求的处理结果
            return f"OK ({key_value}, {value}) removed"
        else:
            return "错误：键未找到"

    elif command == "READ":
        if key_value in tuple_space:
            print(f"READ 请求处理: {key_value} -> {tuple_space[key_value]}")  # 打印 READ 请求的处理结果
            return f"OK ({key_value}, {tuple_space[key_value]})"
        else:
            return "错误：键未找到"

    else:
        return "无效的命令"


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
