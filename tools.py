"""
工具函数模块
"""

import socket
import json
import os
import time
import random
from typing import (
    Optional,
    # Dict,
    # Any
)

# import uuid
import yaml

# import requests
from log import (
    # log_debug,
    log_error,
    log_info,
)


def get_ip_address() -> str:
    """
    获取本机 IP 地址
    :return: 本机 IP 地址
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address


def random_delay(min_seconds: int = 5, max_seconds: int = 15) -> float:
    """
    生成随机延迟时间并等待
    :param min_seconds: 最小延迟秒数
    :param max_seconds: 最大延迟秒数
    :return: 实际延迟的秒数
    """
    delay_seconds = random.uniform(min_seconds, max_seconds)
    log_info(f"将在 {delay_seconds:.2f} 秒后重试...")
    time.sleep(delay_seconds)
    return delay_seconds


# dev 暂时不用
def convert_json_to_yaml(json_path, output_dir="/config"):
    """
    将 JSON 配置文件中的用户信息转换为多个 YAML 文件，每个用户存放在单独文件中，文件名以用户的 name 字段命名。
    :param json_path: 原始 JSON 配置文件路径
    :param output_dir: 输出目录（将自动创建）
    """
    if not os.path.exists(json_path):
        log_error(f"文件不存在: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)

    users = config.get("users", [])
    os.makedirs(output_dir, exist_ok=True)

    for user in users:
        # 使用用户的名字作为文件名，去除可能非法字符
        user_name = user.get("name", "unknown").strip().replace(" ", "_")
        file_name = f"{user_name}.yaml"
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, "w", encoding="utf-8") as yml_file:
            yaml.safe_dump(user, yml_file, allow_unicode=True, default_flow_style=False)
        log_info(f"已生成 YAML 文件: {output_path}")


def get_user_info_by_token(token: str, devcode: str, distinct_id: str) -> Optional[str]:
    """
    根据 token 获取用户信息
    :param token: 用户的 token
    :param devcode: 设备代码
    :param distinct_id: 唯一标识符
    :return: 用户 ID 或 None
    """
    from http_client import KuroHttpClient
    from constants import API

    try:
        client = KuroHttpClient(token, devcode, distinct_id)
        response = client.user_info_post(API.USER_MINE, raise_on_error=False)

        if response.is_success() and response.data:
            user_id = response.data.get("mine", {}).get("userId")
            if user_id:
                log_info(f"获取用户信息成功，用户ID: {user_id}")
                return user_id

        log_error(f"获取用户信息失败: {response.message}")
        return None
    except Exception as e:
        log_error(f"请求失败: {e}")
        return None


def get_game_user_id(
    token: str, game_id: int, devcode: str, distinct_id: str
) -> Optional[str]:
    """
    获取绑定游戏账号角色ID
    :param token: 用户的 token
    :param game_id: 游戏 id (战双 = 2, 鸣潮 = 3)
    :param devcode: 设备代码
    :param distinct_id: 唯一标识符
    :return: 游戏角色 ID 或 None
    """
    from http_client import KuroHttpClient
    from constants import API

    try:
        client = KuroHttpClient(token, devcode, distinct_id)
        response = client.user_info_post(
            API.USER_ROLE_LIST, data={"gameId": str(game_id)}, raise_on_error=False
        )

        if response.is_success() and response.data:
            roles = response.data
            if roles and len(roles) > 0:
                role_id = roles[0].get("roleId")
                log_info(f"获取游戏{game_id}角色ID成功: {role_id}")
                return role_id

        log_error(f"获取绑定游戏账号列表失败: {response.message}")
        return None
    except Exception as e:
        log_error(f"请求失败: {e}")
        return None


if __name__ == "__main__":
    pass
