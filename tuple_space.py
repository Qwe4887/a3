import socket
import threading

# 初始化元组空间
tuple_space = {}


# 处理客户端请求的函数
def handle_client(client_socket, client_address):
    print(f"客户端 {client_address} 连接成功")
    try:
        while True:
            # 接收客户端请求
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # 客户端关闭连接时退出循环

            print(f"收到客户端 {client_address} 的请求: {message}")
            # 在这里处理客户端的请求（比如READ、GET、PUT操作）
            response = process_request(message)

            # 发送响应给客户端
            client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()
        print(f"客户端 {client_address} 断开连接")


# 处理请求的函数（根据协议进行解析）
def process_request(message):
    # 解析消息并执行相应操作
    # 这里只是一个简单的示例，需要根据协议来编写逻辑
    parts = message.split()
    command = parts[1]
    key = parts[2]

    if command == 'P':  # PUT操作
        value = parts[3]
        if key in tuple_space:
            return f"ERR {key} already exists"
        else:
            tuple_space[key] = value
            return f"OK ({key}, {value}) added"

    elif command == 'R':  # READ操作
        if key in tuple_space:
            return f"OK ({key}, {tuple_space[key]}) read"
        else:
            return f"ERR {key} does not exist"

    elif command == 'G':  # GET操作
        if key in tuple_space:
            value = tuple_space.pop(key)
            return f"OK ({key}, {value}) removed"
        else:
            return f"ERR {key} does not exist"


# 启动服务器并监听客户端连接
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 51234))  # 设置服务器地址和端口
    server.listen(5)  # 最大连接数

    print("服务器正在启动，等待客户端连接...")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()


# 启动服务器
if __name__ == '__main__':
    start_server()
