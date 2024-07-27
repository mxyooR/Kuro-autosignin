import requests
from log import log_message
import time


def gettotalgoldheaders(token,devcode,distinct_id):
    totalgoldheaders = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": distinct_id,
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
    return totalgoldheaders
        

def getbbsheaders(token, devcode,distinct_id):
    bbsheaders = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": "127.0.0.1",
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": distinct_id,
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
        "Accept-Encoding": "gzip, deflate, br"}
    return bbsheaders

#获取帖子列表
def getbbsforum(bbsheaders):
    urletbbsforum = "https://api.kurobbs.com/forum/list"
    headers = bbsheaders
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

#获取帖子详情
def getpostdetail(postid, bbsheaders):
    urlgetpostdetail = "https://api.kurobbs.com/forum/getPostDetail"
    headers = bbsheaders

    data = {
        "isOnlyPublisher": "0",
        "postId": postid,
        "showOrderTyper": "2"
    }
    response = requests.post(urlgetpostdetail, headers=headers, data=data)
    return response.json()

#点赞帖子
def likeposts(postid, userid,bbsheaders):
    urllike = "https://api.kurobbs.com/forum/like"
    headers = bbsheaders

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

#分享贴子
def shareposts(bbsheaders):

    urlshare = "https://api.kurobbs.com/encourage/level/shareTask"
    headers = bbsheaders

    data = {
        "gameId": 3,
    }

    response = requests.post(urlshare, headers=headers, data=data)
    if response.json()["code"] == 200:
        return "分享成功"
    else:
        return response.text

#获取金币总数
def getTotalGold(totalgoldheaders):

    urlgetTotalGold = "https://api.kurobbs.com/encourage/gold/getTotalGold"
    headers = totalgoldheaders

    response = requests.post(urlgetTotalGold, headers=headers)
    return response.json()

#bbs签到
def bbssignin(bbsheaders):
    urlbbssignin = "https://api.kurobbs.com/user/signIn"
    headers = bbsheaders

    databbs = {
        "gameId": "2",
    }
    response = requests.post(urlbbssignin, headers=headers, data=databbs)
    if response.json()["code"] == 200:
        return "签到成功"
    else:
        return response.text
    



#库街区签到总函数
def KuroBBS_sign_in(token, devcode,distinct_id):
    bbsheaders = getbbsheaders(token, devcode,distinct_id)
    # 库街区签到
    msg = ""
    msg = msg+log_message(str(bbssignin(bbsheaders)))+"\n\n"
    time.sleep(1)
    log_message("库街区签到完毕，开始点赞帖子")
    msg = msg+"库街区签到完毕，开始点赞帖子\n\n"

    idlist = getbbsforum(bbsheaders)
    post_user_pairs = [(post["postId"], post["userId"])
                    for post in idlist["data"]["postList"]]
    i = 0
    #点赞5个帖子
    for postid, userid in post_user_pairs:
        getpostdetail(postid, bbsheaders)
        time.sleep(5)
        msg += log_message("第"+str((i+1))+"个帖子" +likeposts(postid, userid,bbsheaders))+"\n\n"
        time.sleep(3)
        i += 1
        if i > 4:
            break
    # 转发帖子
    log_message("点赞完毕，开始转发帖子")
    msg = msg+"点赞完毕，开始转发帖子\n\n"
    log_message(shareposts(bbsheaders))
    msg = msg+shareposts(bbsheaders)+"\n\n"

    # 获取金币数量
    totalgoldheaders = gettotalgoldheaders(token,devcode,distinct_id)
    gold = getTotalGold(totalgoldheaders)
    try:
        goldnum = gold["data"]["goldNum"]
        log_message("现在剩余："+str(goldnum)+"金币")
        msg = msg+"现在剩余："+str(goldnum)+"金币\n\n"
    except KeyError:
        gold = getTotalGold(totalgoldheaders)
        log_message("获取金币失败")
        msg = msg+"获取金币失败\n\n"
    

    
    return msg