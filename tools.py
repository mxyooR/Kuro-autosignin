import socket
def get_ip_address():
        """
        获取本机 IP 地址
        :return: 本机 IP 地址
        日志记录：无
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
        except socket.error:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address

def update_config_from_old_version():
    pass