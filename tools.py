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

def fill_raw_config(config_path, token, devcode=str(uuid.uuid4()), distinct_id=str(uuid.uuid4())):
    """
    填充原始 YAML 格式的配置文件
    更新 game_info 中的 token, devCode 以及 distinct_id
    :param config_path: YAML 配置文件路径
    :param token: 用户 token
    :param devcode: 设备代码
    :param distinct_id: 唯一标识符
    """
    if not os.path.exists(config_path):
        log_error(f"配置文件不存在: {config_path}")
        return

    try:
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            config_data = yaml.safe_load(f)
        
        if not config_data:
            config_data = {}

        # 更新 game_info 部分
        if 'game_info' not in config_data:
            config_data['game_info'] = {}

        config_data['user_info']['userId'] = get_user_info_by_token(token, devcode, distinct_id)
        
        #如果用户没有给devcode和distinct_id，使用随机
        config_data['game_info']['devcode'] = devcode
        config_data['game_info']['distinct_id'] = distinct_id

        #更新gameid
        ww_role_id = get_game_user_id(token, 3, devcode, distinct_id)
        eee_role_id = get_game_user_id(token, 2, devcode, distinct_id)

        config_data['game_info']["wwroleId"] = int(ww_role_id) if ww_role_id else None
        config_data['game_info']["eeeroleId"] = int(eee_role_id) if eee_role_id else None


        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config_data, f, allow_unicode=True, default_flow_style=False)

        log_info("YAML 配置文件已成功填充")
    except Exception as e:
        log_error(f"填充 YAML 配置文件失败: {e}")

if __name__ == "__main__":

    get_user_info_by_token(token, devcode, distinct_id)
    # gameid = 2
    role_ids = get_game_user_id(token, 2, devcode, distinct_id)