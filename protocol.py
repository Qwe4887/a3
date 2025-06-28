class Protocol:
    @staticmethod
    def encode_request(op, key, value=None):
        """
        编码请求消息
        :param op: 操作类型 ('R', 'G', 'P')
        :param key: 键
        :param value: 值 (仅PUT操作需要)
        :return: 编码后的消息字符串
        """
        if op == 'P' and value is not None:
            message = f"{op} {key} {value}"
        else:
            message = f"{op} {key}"

        # 计算总长度 (包括长度字段本身)
        total_len = len(message) + 4  # 3位长度 + 1位空格
        if total_len > 999:
            raise ValueError("Message too long")

        return f"{total_len:03d} {message}"

    @staticmethod
    def decode_request(data):
        """
        解码请求消息
        :param data: 原始消息字符串
        :return: (操作类型, 键, 值)
        """
        # 提取长度和消息体
        length = int(data[:3])
        message = data[4:4 + length - 3].strip()

        # 验证长度
        if len(data) != length:
            raise ValueError(f"Invalid message length: expected {length}, got {len(data)}")

        # 解析操作类型和参数
        parts = message.split(' ', 1)
        op = parts[0]

        if op == 'P':
            # PUT操作：键和值
            key_value = parts[1].split(' ', 1)
            if len(key_value) < 2:
                raise ValueError("Invalid PUT format")
            return op, key_value[0], key_value[1]
        elif op in ('R', 'G'):
            # READ或GET操作：只有键
            return op, parts[1], None
        else:
            raise ValueError(f"Unknown operation: {op}")

    @staticmethod
    def encode_response(status, key, value=None, op_type=None):
        """
        编码响应消息
        :param status: 状态 ('OK' 或 'ERR')
        :param key: 键
        :param value: 值
        :param op_type: 操作类型 ('read', 'removed', 'added')
        :return: 编码后的响应字符串
        """
        if status == 'OK':
            if op_type == 'read':
                message = f"OK ({key},{value}) read"
            elif op_type == 'removed':
                message = f"OK ({key},{value}) removed"
            elif op_type == 'added':
                message = f"OK ({key},{value}) added"
            else:
                raise ValueError("Invalid op_type for OK response")
        else:
            # ERR 响应
            if "exists" in op_type:
                message = f"ERR {key} already exists"
            else:
                message = f"ERR {key} does not exist"

        total_len = len(message) + 4  # 3位长度 + 1位空格
        return f"{total_len:03d} {message}"

    @staticmethod
    def decode_response(data):
        """
        解码响应消息
        :param data: 原始响应字符串
        :return: (状态, 键, 值, 操作类型)
        """
        length = int(data[:3])
        message = data[4:4 + length - 3].strip()

        if message.startswith("OK"):
            # 成功响应
            parts = message.split(' ', 1)
            status = parts[0]

            # 提取键值对
            kv_start = message.find('(') + 1
            kv_end = message.find(')')
            kv_str = message[kv_start:kv_end]
            key, value = kv_str.split(',', 1)

            # 提取操作类型
            op_type = message[kv_end + 2:].split()[0]

            return status, key, value, op_type
        else:
            # 错误响应
            status = message.split()[0]
            key = message.split()[1]
            err_msg = ' '.join(message.split()[2:])
            return status, key, None, err_msg