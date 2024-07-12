import requests
from log import log_message

# 获取游戏签到请求头
def getgameheaders(token):
    gameheaders = {
        "Host": "api.kurobbs.com",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-site",
        "devCode": "127.0.0.1, Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
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
    return gameheaders




# 获取签到奖品
def getsignprize(gameheaders, gameId,serverId,roleId, userId):
    urlqueryRecord = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
    headers = gameheaders
    datasign = {
        "gameId": gameId,
        "serverId": serverId,
        "roleId": roleId,
        "userId": userId
    }
    response = requests.post(urlqueryRecord, headers=headers, data=datasign)
    # 检查响应状态码
    if response.status_code != 200:
        return (f"请求失败，状态码: {response.status_code}, 消息: {response.text}")
    response_data = response.json()
    # 检查响应中的 code
    if response_data.get("code") != 200:
        return (f"请求失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}")
    data = response_data["data"]
    if isinstance(data, list) and len(data) > 0:
        first_goods_name = data[0]["goodsName"]
        return first_goods_name

    return ("数据格式不正确或数据为空")

# 鸣潮签到
def mingchaosignin(gameheaders, wwroleId, userId, month):
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
    # 检查响应状态码
    if response.status_code != 200:
        return (f"请求失败，状态码: {response.status_code}, 消息: {response.text}")
    response_data = response.json()
    # 检查响应中的 code
    if response_data.get("code") != 200:
        return (f"请求失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}")
    # 如果成功，调用 getsignprize 获取奖品列表
    try:
        goods_names = getsignprize(gameheaders,3, "76402e5b20be2c39f095a152090afddc",wwroleId, userId)
        return goods_names
    except ValueError as e:
        print(f"获取奖品失败: {e}")
        return None
    
#战双签到
def zhanshuangsignin(eeeroleId, userId, month,gameheaders):
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
    # 检查响应状态码
    if response.status_code != 200:
        return (f"请求失败，状态码: {response.status_code}, 消息: {response.text}")
    response_data = response.json()
    # 检查响应中的 code
    if response_data.get("code") != 200:
        return (f"请求失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}")
    # 如果成功，调用 getsignprize 获取奖品列表
    try:
        goods_names = getsignprize(gameheaders,3, 1000,eeeroleId, userId)
        return goods_names
    except ValueError as e:
        print(f"获取奖品失败: {e}")
        return None






    
def ww_game_check_in(token, wwroleId, userId, month):
    log_message("开始鸣潮签到")
    gameheaders = getgameheaders(token)
    gamemessage=mingchaosignin(gameheaders, wwroleId, userId, month)
    if gamemessage:
        
        log_message("今天的奖励为：" + gamemessage)
    else:
        log_message("签到失败或没有奖励")
    return gamemessage

def eee_game_check_in(token, eeeroleId, userId, month):
    log_message("开始战双签到")
    gameheaders = getgameheaders(token)
    gamemessage=zhanshuangsignin(2, eeeroleId, userId, month,gameheaders)
    if gamemessage:
        log_message("今天的奖励为：" + gamemessage)
    else:
        log_message("签到失败或没有奖励")
    return gamemessage