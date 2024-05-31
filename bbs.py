import requests

def getbbsforum(token,devcode) :
    urletbbsforum = "https://api.kurobbs.com/forum/list"
    headers = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": "yourid",
        "version": "2.2.0",
        "Content-Length": "66",
        "devCode": devcode,
        "token": token,
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "model": "iPhone15,2",
        "osVersion": "17.3",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }

    data = {
        "forumId": "9",
        "gameId": "3",
        "pageIndex": "1",
        "pageSize": "20",
        "searchType": "3",
        "timeType": "0"
    }
    response = requests.post(urletbbsforum, headers=headers, data=data)
    return response.json()

def getpostdetail(token,devcode,postid):
    urlgetpostdetail = "https://api.kurobbs.com/forum/getPostDetail"
    headers = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": "yourid",
        "version": "2.2.0",
        "Content-Length": "66",
        "devCode": devcode,
        "token": token,
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "model": "iPhone15,2",
        "osVersion": "17.3",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }

    data = {
        "isOnlyPublisher": "0",
        "postId": postid,
        "showOrderTyper":"2"
    }
    response = requests.post(urlgetpostdetail, headers=headers, data=data)
    return response.json()

def likeposts(token,devcode,postid,userid):
    urllike = "https://api.kurobbs.com/forum/like"
    headers = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": "yourid",
        "version": "2.2.0",
        "Content-Length": "135",
        "devCode": devcode,
        "token": token,
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "model": "iPhone15,2",
        "osVersion": "17.3",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }

    data = {
        "forumId": 11,
        "gameId": 3,
        "likeType": 1,
        "operateType": 1,
        "postCommentId": "",
        "postCommentReplyId": "",
        "postId":postid,
        "postType": 1,
        "toUserId": userid
        }   

    response = requests.post(urllike, headers=headers, data=data)
    if response.json()["code"]==200:
        return "点赞成功"
    else:
        return response.text



def shareposts(token,devcode):

    urlshare = "https://api.kurobbs.com/encourage/level/shareTask"
    headers = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": "yourid",
        "version": "2.2.0",
        "Content-Length": "8",
        "devCode": devcode,
        "token": token,
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "model": "iPhone15,2",
        "osVersion": "17.3",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }

    data = {
        "gameId": 3,
        }   

    response = requests.post(urlshare, headers=headers, data=data)
    if response.json()["code"]==200:
        return "分享成功"
    else:
         return response.text

def getTotalGold(token,devcode):

    urlgetTotalGold = "https://api.kurobbs.com/encourage/gold/getTotalGold"
    headers = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": "yourid",
        "version": "2.2.0",
        "Content-Length": "0",
        "devCode": devcode,
        "token": token,
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "model": "iPhone15,2",
        "osVersion": "17.3",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }



    response = requests.post(urlgetTotalGold, headers=headers)
    return response.json()


def getsignprize(token, roleId, userId):
    urlqueryRecord = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
    headers = {
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

    datasign = {
        "gameId": "3",
        "serverId": "76402e5b20be2c39f095a152090afddc",
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


def mingchaosignin(token, roleId, userId, month):
    urlsignin = "https://api.kurobbs.com/encourage/signIn/v2"
    headers = {
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

    datasign = {
        "gameId": "3",
        "serverId": "76402e5b20be2c39f095a152090afddc",
        "roleId": roleId,
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
        goods_names = getsignprize(token, roleId, userId)
        return goods_names
    except ValueError as e:
        print(f"获取奖品失败: {e}")
        return None


def bbssignin(token):
        urlbbssignin = "https://api.kurobbs.com/user/signIn"
        headers = {
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

        databbs = {
            "gameId": "3",

        }
        response = requests.post(urlbbssignin, headers=headers, data=databbs)
        if response.json()["code"]==200:
            return "签到成功"
        else:
            return response.text
