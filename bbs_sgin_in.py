import requests
from log import log_info, log_debug, log_error
import time
from tools import get_ip_address

class KuroBBS:
    def __init__(self, token, devcode, distinct_id):
        """
        初始化 KuroBBS 类
        :param token: 用户 token
        :param devcode: 设备码
        :param distinct_id: 用户唯一标识
        """
        self.token = token
        self.devcode = devcode
        self.distinct_id = distinct_id
        self.bbsheaders = self.get_bbs_headers()




    def get_bbs_headers(self):
        """
        生成库街区请求头
        :return: 请求头字典
        日志记录：无
        """
        return {
            "Host": "api.kurobbs.com",
            "source": "ios",
            "lang": "zh-Hans",
            "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
            "Cookie": f"user_token={self.token}",
            "Ip": get_ip_address(),
            "channelId": "1",
            "channel": "appstore",
            "distinct_id": self.distinct_id,
            "version": "2.2.0",
            "devCode": self.devcode,
            "token": self.token,
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "model": "iPhone15,2",
            "osVersion": "17.3",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept-Encoding": "gzip, deflate, br"
        }

    def get_bbs_forum(self):
        """
        获取帖子列表
        :return: 帖子列表 JSON 数据或错误信息
        日志记录：
            - debug: 帖子列表响应
            - info: 成功获取帖子列表
            - error: 获取帖子列表失败
        """
        try:
            url = "https://api.kurobbs.com/forum/list"
            data = {
                "forumId": "9",
                "gameId": "3",
                "pageIndex": "1",
                "pageSize": "20",
                "searchType": "3",
                "timeType": "0"
            }
            response = requests.post(url, headers=self.bbsheaders, data=data)
            response.raise_for_status()
            log_debug(f"帖子列表响应: {response.text}")
            log_info("成功获取帖子列表")
            return response.json()
        except Exception as e:
            error_message = f"获取帖子列表失败: {e}"
            log_error(error_message)
            return "ERROR:"+error_message

    def get_post_detail(self, postid):
        """
        获取帖子详情
        :param postid: 帖子 ID
        :return: 帖子详情 JSON 数据或错误信息
        日志记录：
            - debug: 帖子详情响应
            - debug: 成功获取帖子详情
            - error: 获取帖子详情失败
        """
        try:
            url = "https://api.kurobbs.com/forum/getPostDetail"
            data = {
                "isOnlyPublisher": "0",
                "postId": postid,
                "showOrderTyper": "2"
            }
            response = requests.post(url, headers=self.bbsheaders, data=data)
            response.raise_for_status()
            log_debug(f"帖子详情响应: {response.text}")
            log_debug(f"成功获取帖子详情，帖子ID: {postid}")
            return response.json()
        except Exception as e:
            error_message = f"获取帖子详情失败，帖子ID: {postid}, 错误: {e}"
            log_error(error_message)
            return "ERROR:"+error_message

    def like_posts(self, postid, userid):
        """
        点赞帖子
        :param postid: 帖子 ID
        :param userid: 用户 ID
        :return: 点赞结果或错误信息
        日志记录：
            - debug: 点赞响应
            - debug: 成功点赞帖子
            - error: 点赞帖子失败
        """
        try:
            url = "https://api.kurobbs.com/forum/like"
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
            response = requests.post(url, headers=self.bbsheaders, data=data)
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
            return "ERROR:"+error_message

    def share_posts(self):
        """
        分享帖子
        :return: 分享结果或错误信息
        日志记录：
            - debug: 分享响应
            - info: 成功分享帖子
            - error: 分享帖子失败
        """
        try:
            url = "https://api.kurobbs.com/encourage/level/shareTask"
            data = {"gameId": 3}
            response = requests.post(url, headers=self.bbsheaders, data=data)
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
            return "ERROR:"+error_message

    def get_total_task(self):
        """
        获取任务列表
        :return: 任务列表 JSON 数据或错误信息
        日志记录：
            - debug: 任务列表响应
            - info: 成功获取任务列表
            - error: 获取任务列表失败
        """
        try:
            url = "https://api.kurobbs.com/encourage/level/getTaskProcess"
            data = {"gameId": "0"}
            response = requests.post(url, headers=self.bbsheaders, data=data)
            response.raise_for_status()
            log_debug(f"任务列表响应: {response.text}")
            log_info("成功获取任务列表")
            return response.json()
        except Exception as e:
            error_message = f"获取任务列表失败: {e}"
            log_error(error_message)
            return "ERROR:"+error_message

    def get_total_gold(self):
        """
        获取金币总数
        :return: 金币总数 JSON 数据或错误信息
        日志记录：
            - debug: 金币总数响应
            - info: 成功获取金币总数
            - error: 获取金币总数失败
        """
        try:
            url = "https://api.kurobbs.com/encourage/gold/getTotalGold"
            response = requests.post(url, headers=self.bbsheaders)
            response.raise_for_status()
            log_debug(f"金币总数响应: {response.text}")
            log_info("成功获取金币总数")
            return response.json()
        except Exception as e:
            error_message = f"获取金币总数失败: {e}"
            log_error(error_message)
            return "ERROR:"+error_message

    def bbssignin(self):
        """
        执行库街区签到
        :return: 签到结果或错误信息
        日志记录：
            - debug: 库街区签到响应
            - info: 成功完成签到
            - error: 签到失败
        """
        try:
            url = "https://api.kurobbs.com/user/signIn"
            data = {"gameId": "2"}
            response = requests.post(url, headers=self.bbsheaders, data=data)
            response.raise_for_status()
            log_debug(f"库街区签到响应: {response.text}")
            if response.json()["code"] == 200:
                log_info("成功完成签到")
                return "签到成功"
            else:
                log_error(f"签到失败: {response.text}")
                return "ERROR:签到失败"
        except Exception as e:
            error_message = f"签到失败: {e}"
            log_error(error_message)
            return "ERROR:"+error_message

    def sign_in(self):
        """
        执行库街区签到流程
        :return: 签到结果消息或错误信息
        日志记录：
            - info: 开始处理每日任务
            - info: 开始处理任务
            - info: 今日任务已完成，总计获取金币
            - error: 库街区签到流程失败
        """
        try:
            msg = ""

            # 获取任务列表
            task_data = self.get_total_task()
            if isinstance(task_data, str):  # 如果返回的是错误信息
                log_error(task_data)
                return task_data

            daily_tasks = task_data["data"]["dailyTask"]
            log_info("开始处理每日任务")

            # 遍历 dailyTask，处理未完成的任务
            for task in daily_tasks:
                if int(task["process"]) == 0:  # 仅处理未完成的任务
                    remark = task["remark"]
                    log_info(f"开始处理任务: {remark}")

                    if remark == "用户签到":
                        signin_result = self.bbssignin()  # 修复：调用 bbssignin 而不是递归调用 sign_in
                        msg += f"签到结果: {signin_result}\n"

                    elif remark == "浏览3篇帖子":
                        idlist = self.get_bbs_forum()
                        if isinstance(idlist, str):  # 如果返回的是错误信息
                            log_error(idlist)
                            msg += idlist + "\n"
                        elif idlist:
                            post_user_pairs = [(post["postId"], post["userId"]) for post in idlist["data"]["postList"]]
                            for i, (postid, userid) in enumerate(post_user_pairs[:3]):  # 浏览3篇帖子
                                post_detail = self.get_post_detail(postid)
                                if isinstance(post_detail, str):  # 如果返回的是错误信息
                                    log_error(post_detail)
                                    msg += post_detail + "\n"
                                time.sleep(1)

                    elif remark == "点赞5次":
                        idlist = self.get_bbs_forum()
                        if isinstance(idlist, str):  # 如果返回的是错误信息
                            log_error(idlist)
                            msg += idlist + "\n"
                        elif idlist:
                            post_user_pairs = [(post["postId"], post["userId"]) for post in idlist["data"]["postList"]]
                            for i, (postid, userid) in enumerate(post_user_pairs[:5]):  # 点赞5次
                                like_result = self.like_posts(postid, userid)
                                if like_result is None:
                                    like_result = "点赞失败"
                                log_info(f"第{i+1}次点赞结果: {like_result}")
                                msg += f"第{i+1}次点赞结果: {like_result}\n"
                                time.sleep(1)

                    elif remark == "分享1次帖子":
                        share_result = self.share_posts()
                        msg += f"分享结果: {share_result}\n"

                    time.sleep(1)

            # 再次获取任务列表，计算总金币
            task_data = self.get_total_task()
            if isinstance(task_data, str):  # 如果返回的是错误信息
                log_error(task_data)
                return task_data

            daily_tasks = task_data["data"]["dailyTask"]
            gain_gold = sum(task["gainGold"] for task in daily_tasks if task["process"] == 1)

            total_gold = self.get_total_gold()
            goldnum = total_gold["data"]["goldNum"]
            log_info(f"今日任务已完成，总计获取金币: {gain_gold};现在剩余：{goldnum}金币")
            msg += f"今日任务已完成，总计获取金币: {gain_gold};现在剩余：{goldnum}金币\n"

            log_info("库街区签到流程完成")
            return msg
        except Exception as e:
            error_message = f"库街区签到流程失败: {e}"
            log_error(error_message)
            return "ERROR:"+error_message