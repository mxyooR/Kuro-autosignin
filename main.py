"""
任务名称
name: 库街区签到任务
定时规则
cron: 1 9 * * *
"""
import time
import datetime
import json
import requests


def sc_send(text, desp, key=''):
    if key == '':
        print("请填写server酱的KEY")
        return
    url = f'https://sctapi.ftqq.com/{key}.send'
    data = {'text': text, 'desp': desp}
    response = requests.post(url, data=data)
    result = response.text
    return result


def getbbsforum(token, devcode):
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


def getpostdetail(token, devcode, postid):
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
        "showOrderTyper": "2"
    }
    response = requests.post(urlgetpostdetail, headers=headers, data=data)
    return response.json()


def likeposts(token, devcode, postid, userid):
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
        "postId": postid,
        "postType": 1,
        "toUserId": userid
    }

    response = requests.post(urllike, headers=headers, data=data)
    if response.json()["code"] == 200:
        return "点赞成功"
    else:
        return response.text


def shareposts(token, devcode):

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
    if response.json()["code"] == 200:
        return "分享成功"
    else:
        return response.text


def getTotalGold(token, devcode):

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
    if response.json()["code"] == 200:
        return "签到成功"
    else:
        return response.text


def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")

    # 从JSON文件中读取数据
    with open('data.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    serverKey = data['serverKey']
    # 从数据中获取用户数据列表
    users = data['users']

    for user in users:
        wechattext = ""
        name = user['name']
        roleId = user['roleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode = user['devCode']

        data = {
            "gameId": "3",
            "serverId": "76402e5b20be2c39f095a152090afddc",
            "roleId": roleId,
            "userId": userId
        }

        # 鸣潮签到

        print(now.strftime("%Y-%m-%d"))
        wechattext = wechattext+now.strftime("%Y-%m-%d")+" "+name+"签到\n\n"
        print(name)
        print("=====================================")
        response0 = mingchaosignin(tokenraw, roleId, userId, month)
        if response0:

            print("今天的奖励为：" + response0)
            wechattext = wechattext+"今天的奖励为："+response0+"\n\n"
        else:
            print("签到失败或没有奖励")

        print("=====================================")
        time.sleep(1)

        # 库街区签到

        response1 = bbssignin(tokenraw)
        wechattext = wechattext+str(response1)+"\n\n"
        print(response1)
        print("=====================================")
        time.sleep(1)
        print("签到完毕，开始点赞帖子")
        wechattext = wechattext+"签到完毕，开始点赞帖子\n\n"

        idlist = getbbsforum(tokenraw, devcode)
        post_user_pairs = [(post["postId"], post["userId"])
                           for post in idlist["data"]["postList"]]
        i = 0
        for postid, userid in post_user_pairs:
            getpostdetail(tokenraw, devcode, postid)
            time.sleep(5)
            print("第"+str((i+1))+"个帖子" +
                  likeposts(tokenraw, devcode, postid, userid))
            wechattext = wechattext+"第" + \
                str((i+1))+"个帖子" + \
                str(likeposts(tokenraw, devcode, postid, userid))+"\n\n"
            time.sleep(3)
            i += 1
            if i > 4:
                break
        print("=====================================")

        # 转发帖子
        print("点赞完毕，开始转发帖子")
        wechattext = wechattext+"点赞完毕，开始转发帖子\n\n"
        print(shareposts(tokenraw, devcode))
        wechattext = wechattext+shareposts(tokenraw, devcode)+"\n\n"
        print("=====================================")

        # 获取金币数量
        gold = getTotalGold(tokenraw, devcode)
        goldnum = gold["data"]["goldNum"]
        print("现在剩余："+str(goldnum)+"金币")
        wechattext = wechattext+"现在剩余："+str(goldnum)+"金币\n\n"
        print(name+"签到完毕")

        # 发送微信通知
        print(sc_send(name+"签到", wechattext, key=serverKey))


sign_in()
