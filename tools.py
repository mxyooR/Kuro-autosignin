import socket
import json
import os
from log import log_debug, log_error, log_info
import yaml
import requests
import uuid

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




def convert_json_to_yaml(json_path, output_dir="/config"):
    """
    将 JSON 配置文件中的用户信息转换为多个 YAML 文件，每个用户存放在单独文件中，文件名以用户的 name 字段命名。
    :param json_path: 原始 JSON 配置文件路径
    :param output_dir: 输出目录（将自动创建）
    """
    if not os.path.exists(json_path):
        log_error(f"文件不存在: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    
    users = config.get("users", [])
    os.makedirs(output_dir, exist_ok=True)
    
    for user in users:
        # 使用用户的名字作为文件名，去除可能非法字符
        user_name = user.get("name", "unknown").strip().replace(" ", "_")
        file_name = f"{user_name}.yaml"
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, 'w', encoding='utf-8') as yml_file:
            yaml.safe_dump(user, yml_file, allow_unicode=True, default_flow_style=False)
        log_info(f"已生成 YAML 文件: {output_path}")

def get_user_info_by_token(token, devcode, distinct_id):
    """
    根据 token 和用户 ID 获取用户信息
    :param token: 用户的 token
    :param devcode: 设备代码
    :param distinct_id: 唯一标识符
    :return: 用户 ID 或错误信息
    """

    url = "https://api.kurobbs.com/user/mineV2"
    headers = {
        "osversion": "Android",
        "devcode": devcode,
        "distinct_id": distinct_id,
        "countrycode": "CN",
        "ip": "10.0.2.233",
        "model": "2211133C",
        "source": "android",
        "lang": "zh-Hans",
        "version": "1.0.9",
        "versioncode": "1090",
        "token": token,
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.10.0",
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            log_info("获取用户信息成功")
            log_debug(f"用户信息: {result}")
            user_id = result.get("data", {}).get("mine", {}).get("userId", "未知用户ID")
            #print(f"用户ID: {user_id}")
            return user_id
        else:
            log_error(f"获取用户信息失败: {result.get('msg')}")
            return {"error": result.get("msg")}
    except requests.RequestException as e:
        log_error(f"请求失败: {e}")
        return {"error": str(e)}
    
def get_game_user_id(token,gameid,devcode,distinct_id):
    """
    获取绑定游戏账号列表
    :param token: 用户的 token
    :param gameid: 游戏 id (战双 = 2, 鸣潮 = 3)
    :param devcode: 设备代码
    :param distinct_id: 唯一标识符
    :return: 游戏账号 id 列表或错误信息
    """
    url = "https://api.kurobbs.com/user/role/findRoleList"
    headers = {
        "osversion": "Android",
        "devcode": devcode,
        "distinct_id": distinct_id,
        "countrycode": "CN",
        "ip": "10.0.2.233",
        "model": "2211133C",
        "source": "android",
        "lang": "zh-Hans",
        "version": "1.0.9",
        "versioncode": "1090",
        "token": token,
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.10.0",
    }
    data = f"gameId={gameid}"

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            log_info("获取绑定游戏账号列表成功")
            log_debug(f"绑定游戏账号列表: {result}")
            role_ids = result.get("data", [])[0].get("roleId") if result.get("data") else None
            #print(f"绑定游戏账号列表: {role_ids}")
            return role_ids
        else:
            log_error(f"获取绑定游戏账号列表失败: {result.get('msg')}")
            return None
    except requests.RequestException as e:
        log_error(f"请求失败: {e}")
        return {"error": str(e)}



if __name__ == "__main__":
    pass