import requests
from log import log_info, log_debug, log_error
import time
import random
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个公共的服务器，这里使用 Google 的 DNS 服务器
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address




def getbbsheaders(token, devcode,distinct_id):
    bbsheaders = {
        "Host": "api.kurobbs.com",
        "source": "ios",
        "lang": "zh-Hans",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "Cookie": "user_token="+token,
        "Ip": get_ip_address(),
        "channelId": "1",
        "channel": "appstore",
        "distinct_id": distinct_id,
        "version": "2.2.0",
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
    return bbsheaders

#获取帖子列表
def getbbsforum(bbsheaders):
    """
    获取帖子列表
    :param bbsheaders: 库街区请求头
    :return: 帖子列表
    失败返回：获取帖子列表失败: {e}
    日志记录：info:成功获取帖子列表
            debug：帖子列表响应: {response.text}
            error：获取帖子列表失败: {e}    

    """
    try:
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
        response.raise_for_status()
        log_debug(f"帖子列表响应: {response.text}")
        log_info("成功获取帖子列表")
        return response.json()
    except Exception as e:
        error_message = f"获取帖子列表失败: {e}"
        log_error(error_message)
        return error_message

#获取帖子详情
def getpostdetail(postid, bbsheaders):
    """
    :param postid: 帖子ID
    :param bbsheaders: 库街区请求头
    :return: 帖子详情
    失败返回：获取帖子详情失败，帖子ID: {postid}, 错误: {e}
    日志记录：debug:成功获取帖子详情，帖子ID: {postid}
            debug：帖子详情响应: {response.text}
            error：获取帖子详情失败，帖子ID: {postid}, 错误: {e}
    """
    try:
        urlgetpostdetail = "https://api.kurobbs.com/forum/getPostDetail"
        headers = bbsheaders

        data = {
            "isOnlyPublisher": "0",
            "postId": postid,
            "showOrderTyper": "2"
        }
        response = requests.post(urlgetpostdetail, headers=headers, data=data)
        response.raise_for_status()
        log_debug(f"帖子详情响应: {response.text}")
        log_debug(f"成功获取帖子详情，帖子ID: {postid}")
        return response.json()
    except Exception as e:
        error_message = f"获取帖子详情失败，帖子ID: {postid}, 错误: {e}"
        log_error(error_message)
        return error_message

#点赞帖子
def likeposts(postid, userid,bbsheaders):
    """
    
    :param postid: 帖子ID
    :param userid: 用户ID
    :param bbsheaders: 库街区请求头
    :return: 点赞结果
    失败返回：点赞帖子失败，帖子ID: {postid}, 错误: {e}
    日志记录：info:不记录
            debug：点赞响应: {response.text}
            error：点赞帖子失败，帖子ID: {postid}, 错误: {response.text}
    """
    try:
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
        response.raise_for_status()
        log_debug(f"点赞响应: {response.text}")
        if response.json()["code"] == 200:
            log_debug(f"成功点赞帖子，帖子ID: {postid}")
            return "点赞成功"
        else:
            log_error(f"点赞帖子失败，帖子ID: {postid}, 错误: {response.text}")
            return response.text
    except Exception as e:
        error_message = f"点赞帖子失败，帖子ID: {postid}, 错误: {e}"
        log_error(error_message)
        return error_message

#分享贴子
def shareposts(bbsheaders):
    """
    :param bbsheaders: 库街区请求头
    :return: 分享结果
    失败返回：分享帖子失败: {e}
    日志记录：info:成功分享帖子
            debug：分享响应: {response.text}
            error：分享帖子失败: {e}
    """
    try:
        urlshare = "https://api.kurobbs.com/encourage/level/shareTask"
        headers = bbsheaders

        data = {
            "gameId": 3,
        }

        response = requests.post(urlshare, headers=headers, data=data)
        response.raise_for_status()
        log_debug(f"分享响应: {response.text}")
        if response.json()["code"] == 200:
            log_info("成功分享帖子")
            return "分享成功"
        else:
            log_error(f"分享帖子失败: {response.text}")
            return response.text
    except Exception as e:
        error_message = f"分享帖子失败: {e}"
        log_error(error_message)
        return error_message

#获取金币总数
def getTotalGold(totalgoldheaders):
    """
    :param totalgoldheaders: 库街区请求头
    :return: 金币总数
    失败返回：获取金币总数失败: {e}
    日志记录：info:成功获取金币总数
            debug：金币总数响应: {response.text}
            error：获取金币总数失败: {e}
    """
    try:
        urlgetTotalGold = "https://api.kurobbs.com/encourage/gold/getTotalGold"
        headers = totalgoldheaders

        response = requests.post(urlgetTotalGold, headers=headers)
        response.raise_for_status()
        log_debug(f"金币总数响应: {response.text}")
        log_info("成功获取金币总数")
        return response.json()
    except Exception as e:
        error_message = f"获取金币总数失败: {e}"
        log_error(error_message)
        return error_message

#bbs签到
def bbssignin(bbsheaders):
    """
    :param bbsheaders: 库街区请求头
    :return: 签到结果
    失败返回：签到失败: {response.text}
    日志记录：info:成功完成签到
            debug：库街区bbs签到响应: {response.text}
            error：签到失败: {response.text
    """
    try:
        urlbbssignin = "https://api.kurobbs.com/user/signIn"
        headers = bbsheaders

        databbs = {
            "gameId": "2",
        }
        response = requests.post(urlbbssignin, headers=headers, data=databbs)
        response.raise_for_status()
        log_debug(f"库街区bbs签到响应: {response.text}")
        if response.json()["code"] == 200:
            log_info("成功完成签到")
            return "签到成功"
        else:
            log_error(f"签到失败: {response.text}")
            return  "签到失败"
    except Exception as e:
        error_message = f"签到失败: {e}"
        log_error(error_message)
        return error_message
    

def get_total_task(bbsheaders):
    """
    :param bbsheaders: 库街区请求头
    :return: 任务列表
    失败返回：获取任务列表失败: {e}
    日志记录：info:成功获取任务列表
            debug：任务列表响应: {response.text}
            error：获取任务列表失败: {e}
    """
    try:
        urlgettask = "https://api.kurobbs.com/encourage/level/getTaskProcess"
        headers = bbsheaders

        response = requests.post(urlgettask, headers=headers)
        response.raise_for_status()
        log_debug(f"任务列表响应: {response.text}")
        log_info("成功获取任务列表")
        return response.json()
    except Exception as e:
        error_message = f"获取任务列表失败: {e}"
        log_error(error_message)
        return error_message
    

    
#库街区签到总函数
def KuroBBS_sign_in(token, devcode, distinct_id):
    """
    :param token: 用户token
    :param devcode: 设备码
    :param distinct_id: 用户ID
    :return: push用的msg
    失败返回：库街区签到流程失败: {e}
    日志记录：info:库街区签到流程完成
            error：库街区签到流程失败: {e}
    """
    try:
        bbsheaders = getbbsheaders(token, devcode, distinct_id)
        # 库街区签到
        msg = ""
        signin_result = bbssignin(bbsheaders)
        if signin_result is None:
            signin_result = "签到失败"
        msg += str(signin_result) + "\n\n"
        time.sleep(1)
        log_info("库街区签到完毕，开始点赞帖子")
        msg += "库街区签到完毕，开始点赞帖子\n\n"
        #获取帖子列表
        idlist = getbbsforum(bbsheaders)
        if isinstance(idlist, str):  # 如果返回的是错误信息
            msg +=str(idlist) + "\n\n"
        elif idlist:
            post_user_pairs = [(post["postId"], post["userId"]) for post in idlist["data"]["postList"]]
            i = 0
            # 点赞5个帖子
            for postid, userid in post_user_pairs:
                post_detail = getpostdetail(postid, bbsheaders)
                if isinstance(post_detail, str):  # 如果返回的是错误信息
                    log_error(post_detail)
                    msg += str(post_detail) + "\n\n"
                time.sleep(5)
                like_result = likeposts(postid, userid, bbsheaders)
                if like_result is None:
                    like_result = "点赞失败"
                log_info(f"第{i+1}个帖子 {like_result}")
                msg += (f"第{i+1}个帖子 {like_result}") + "\n\n"
                time.sleep(random.randint(1, 3))
                i += 1
                if i > 4:
                    break

        # 转发帖子
        log_info("点赞完毕，开始转发帖子")
        msg += "点赞完毕，开始转发帖子\n\n"
        share_result = shareposts(bbsheaders)
        msg += share_result + "\n\n"

        # 获取金币数量
        totalgoldheaders = getbbsheaders(token, devcode, distinct_id)
        gold = getTotalGold(totalgoldheaders)
        if isinstance(gold, str):  # 如果返回的是错误信息
            msg += log_error(gold) + "\n\n"
        elif gold:
            try:
                goldnum = gold["data"]["goldNum"]
                log_info(f"现在剩余：{goldnum}金币")
                msg += f"现在剩余：{goldnum}金币\n\n"
            except KeyError:
                log_error("获取金币失败")
                msg += "获取金币失败\n\n"
        else:
            log_error("获取金币失败")
            msg += "获取金币失败\n\n"

        log_info("库街区签到流程完成")
        return msg
    except Exception as e:
        error_message = f"库街区签到流程失败: {e}"
        log_error(error_message)
        return error_message