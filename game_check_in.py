import requests
from log import log_info, log_debug, log_error
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

# 获取游戏签到请求头
def getgameheaders(token):
    gameheaders = {
        "Host": "api.kurobbs.com",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-site",
        "devCode": f"{get_ip_address()}, Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
        "source": "ios",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "token": token,
        "Origin": "https://web-static.kurobbs.com",
        "Content-Length": "83",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
        "Connection": "keep-alive"
    }
    log_debug(f"生成游戏签到请求头: {gameheaders}")
    return gameheaders

# 获取签到奖品
def getsignprize(gameheaders, gameId, serverId, roleId, userId):
    try:
        urlqueryRecord = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
        headers = gameheaders
        datasign = {
            "gameId": gameId,
            "serverId": serverId,
            "roleId": roleId,
            "userId": userId
        }
        response = requests.post(urlqueryRecord, headers=headers, data=datasign)
        response.raise_for_status()
        log_debug(f"签到奖品响应: {response.text}")
        response_data = response.json()
        if response_data.get("code") != 200:
            error_message = f"获取签到奖品失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}"
            log_error(error_message)
            return error_message
        data = response_data["data"]
        if isinstance(data, list) and len(data) > 0:
            first_goods_name = data[0]["goodsName"]
            log_info(f"成功获取签到奖品: {first_goods_name}")
            return first_goods_name
        error_message = "签到奖品数据格式不正确或数据为空"
        log_error(error_message)
        return error_message
    except Exception as e:
        error_message = f"获取签到奖品失败: {e}"
        log_error(error_message)
        return error_message

# 鸣潮签到
def mingchaosignin(gameheaders, wwroleId, userId, month):
    try:
        urlsignin = "https://api.kurobbs.com/encourage/signIn/v2"
        headers = gameheaders

        datasign = {
            "gameId": "3",
            "serverId": "76402e5b20be2c39f095a152090afddc",
            "roleId": wwroleId,
            "userId": userId,
            "reqMonth": month
        }
        response = requests.post(urlsignin, headers=headers, data=datasign)
        response.raise_for_status()
        log_debug(f"鸣潮签到响应: {response.text}")
        response_data = response.json()
        if response_data.get("code") != 200:
            error_message = f"鸣潮签到失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}"
            log_error(error_message)
            return error_message
        # 如果成功，调用 getsignprize 获取奖品列表
        goods_names = getsignprize(gameheaders, 3, "76402e5b20be2c39f095a152090afddc", wwroleId, userId)
        return goods_names
    except Exception as e:
        error_message = f"鸣潮签到失败: {e}"
        log_error(error_message)
        return error_message

# 战双签到
def zhanshuangsignin(eeeroleId, userId, month, gameheaders):
    try:
        url = "https://api.kurobbs.com/encourage/signIn/v2"
        headers = gameheaders
        data = {
            'gameId': 2,
            'serverId': 1000,
            'roleId': eeeroleId,
            'userId': userId,
            'reqMonth': month
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        log_debug(f"战双签到响应: {response.text}")
        response_data = response.json()
        if response_data.get("code") != 200:
            error_message = f"战双签到失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}"
            log_error(error_message)
            return error_message
        # 如果成功，调用 getsignprize 获取奖品列表
        goods_names = getsignprize(gameheaders, 2, 1000, eeeroleId, userId)
        return goods_names
    except Exception as e:
        error_message = f"战双签到失败: {e}"
        log_error(error_message)
        return error_message

def ww_game_check_in(token, wwroleId, userId, month):
    log_info("开始鸣潮签到")
    gameheaders = getgameheaders(token)
    gamemessage = mingchaosignin(gameheaders, wwroleId, userId, month)
    if gamemessage:
        log_info(f"鸣潮签到成功，今天的奖励为: {gamemessage}")
    else:
        log_error("鸣潮签到失败或没有奖励")
    return gamemessage

def eee_game_check_in(token, eeeroleId, userId, month):
    log_info("开始战双签到")
    gameheaders = getgameheaders(token)
    gamemessage = zhanshuangsignin(eeeroleId, userId, month, gameheaders)
    if gamemessage:
        log_info(f"战双签到成功，今天的奖励为: {gamemessage}")
    else:
        log_error("战双签到失败或没有奖励")
    return gamemessage