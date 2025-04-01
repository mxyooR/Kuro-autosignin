import socket
import json
import os
from log import log_debug, log_error, log_info

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

def update_config_from_old_version(config_path):
    """
    更新老版本的配置文件到新版本
    :param config_path: 配置文件路径
    """
    if not os.path.exists(config_path):
        log_error("配置文件不存在，无法更新")
        return

    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)

    # 检查并更新每个用户的配置
    for user in config.get("users", []):
        if "is_enable" not in user:
            user["is_enable"] = True  # 添加默认值

    # 保存更新后的配置
    with open(config_path, 'w', encoding='utf-8-sig') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    log_info("配置文件已成功更新")