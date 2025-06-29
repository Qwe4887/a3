import socket

# 读取请求文件的函数
def read_request_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except OSError as e:
        print(f"文件打开错误: {e}")
        return []

# 向服务器发送请求并接收响应
def send_request_to_server(client_socket, request):
    try:
        # 发送请求
        client_socket.send(request.encode('utf-8'))

        # 接收服务器响应
        response = client_socket.recv(1024).decode('utf-8')
        return response

    except Exception as e:
        print(f"连接或请求过程中发生错误: {e}")
        return None

# 主程序
def main():
    # 硬编码的服务器信息和请求文件路径
    host = 'localhost'  # 服务器的主机名或IP地址
    port = 51235        # 服务器的端口号
    file_path = r'C:\Users\Administrator\Desktop\a3\a3\client_1.txt'  # 请求文件路径

    # 读取请求文件
    requests = read_request_file(file_path)

    # 创建客户端 socket 并连接到服务器
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  # 建立连接

        for request in requests:
            # 去除多余的空格和换行符
            request = request.strip()

            if request:
                print(f"发送请求: {request}")
                response = send_request_to_server(client_socket, request)
                print(f"收到响应: {response}")
            else:
                print("空行，跳过...")

if __name__ == "__main__":
    main()
