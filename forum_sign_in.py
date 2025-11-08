"""
论坛签到模块（重构版）
"""
import time
from typing import List, Tuple, Optional
from log import log_info, log_debug, log_error
from http_client import KuroHttpClient
from constants import API, TaskType
from models import SignInResult, ResponseStatus


class ForumSignIn:
    """论坛签到类"""
    
    def __init__(self, client: KuroHttpClient):
        """
        初始化论坛签到
        :param client: HTTP客户端
        """
        self.client = client
    
    def get_forum_list(self) -> Optional[List[dict]]:
        """
        获取论坛帖子列表
        :return: 帖子列表或None
        """
        try:
            data = {
                "forumId": "9",
                "gameId": "3",
                "pageIndex": "1",
                "pageSize": "20",
                "searchType": "3",
                "timeType": "0"
            }
            
            response = self.client.bbs_post(API.FORUM_LIST, data, raise_on_error=False)
            
            if response.is_success() and response.data:
                posts = response.data.get("postList", [])
                log_info(f"成功获取帖子列表，共 {len(posts)} 篇")
                return posts
            
            log_error(f"获取帖子列表失败: {response.message}")
            return None
            
        except Exception as e:
            log_error(f"获取帖子列表失败: {e}")
            return None
    
    def get_post_detail(self, post_id: str) -> bool:
        """
        获取帖子详情（浏览帖子）
        :param post_id: 帖子ID
        :return: 是否成功
        """
        try:
            data = {
                "isOnlyPublisher": "0",
                "postId": post_id,
                "showOrderTyper": "2"
            }
            
            response = self.client.bbs_post(API.FORUM_POST_DETAIL, data, raise_on_error=False)
            
            if response.is_success():
                log_debug(f"成功浏览帖子，帖子ID: {post_id}")
                return True
            
            log_error(f"浏览帖子失败，帖子ID: {post_id}, 错误: {response.message}")
            return False
            
        except Exception as e:
            log_error(f"浏览帖子失败，帖子ID: {post_id}, 错误: {e}")
            return False
    
    def like_post(self, post_id: str, user_id: str) -> bool:
        """
        点赞帖子
        :param post_id: 帖子ID
        :param user_id: 用户ID
        :return: 是否成功
        """
        try:
            data = {
                "forumId": 11,
                "gameId": 3,
                "likeType": 1,
                "operateType": 1,
                "postCommentId": "",
                "postCommentReplyId": "",
                "postId": post_id,
                "postType": 1,
                "toUserId": user_id
            }
            
            response = self.client.bbs_post(API.FORUM_LIKE, data, raise_on_error=False)
            
            if response.is_success():
                log_debug(f"成功点赞帖子，帖子ID: {post_id}")
                return True
            
            log_error(f"点赞帖子失败，帖子ID: {post_id}, 错误: {response.message}")
            return False
            
        except Exception as e:
            log_error(f"点赞帖子失败，帖子ID: {post_id}, 错误: {e}")
            return False
    
    def share_post(self) -> bool:
        """
        分享帖子
        :return: 是否成功
        """
        try:
            data = {"gameId": 3}
            response = self.client.bbs_post(API.TASK_SHARE, data, raise_on_error=False)
            
            if response.is_success():
                log_info("成功分享帖子")
                return True
            
            log_error(f"分享帖子失败: {response.message}")
            return False
            
        except Exception as e:
            log_error(f"分享帖子失败: {e}")
            return False
    
    def forum_sign_in(self) -> bool:
        """
        论坛签到
        :return: 是否成功
        """
        try:
            data = {"gameId": "2"}
            response = self.client.bbs_post(API.USER_SIGN_IN, data, raise_on_error=False)
            
            if response.is_success():
                log_info("论坛签到成功")
                return True
            
            log_error(f"论坛签到失败: {response.message}")
            return False
            
        except Exception as e:
            log_error(f"论坛签到失败: {e}")
            return False
    
    def get_task_list(self) -> Optional[List[dict]]:
        """
        获取每日任务列表
        :return: 任务列表或None
        """
        try:
            data = {"gameId": "0"}
            response = self.client.bbs_post(API.TASK_PROCESS, data, raise_on_error=False)
            
            if response.is_success() and response.data:
                tasks = response.data.get("dailyTask", [])
                log_info(f"成功获取任务列表，共 {len(tasks)} 个任务")
                return tasks
            
            log_error(f"获取任务列表失败: {response.message}")
            return None
            
        except Exception as e:
            log_error(f"获取任务列表失败: {e}")
            return None
    
    def get_total_gold(self) -> Optional[int]:
        """
        获取金币总数
        :return: 金币数量或None
        """
        try:
            response = self.client.bbs_post(API.GOLD_TOTAL, raise_on_error=False)
            
            if response.is_success() and response.data:
                gold = response.data.get("goldNum", 0)
                log_debug(f"当前金币数量: {gold}")
                return gold
            
            log_error(f"获取金币总数失败: {response.message}")
            return None
            
        except Exception as e:
            log_error(f"获取金币总数失败: {e}")
            return None
    
    def do_task_sign_in(self) -> str:
        """执行签到任务"""
        result = self.forum_sign_in()
        return "签到成功" if result else "签到失败"
    
    def do_task_view_posts(self) -> str:
        """执行浏览帖子任务"""
        posts = self.get_forum_list()
        if not posts:
            return "获取帖子列表失败"
        
        view_count = 0
        for post in posts[:3]:
            if self.get_post_detail(post["postId"]):
                view_count += 1
            time.sleep(1)
        
        return f"已浏览 {view_count}/3 篇帖子"
    
    def do_task_like_posts(self) -> str:
        """执行点赞任务"""
        posts = self.get_forum_list()
        if not posts:
            return "获取帖子列表失败"
        
        like_count = 0
        for i, post in enumerate(posts[:5], 1):
            if self.like_post(post["postId"], post["userId"]):
                like_count += 1
                log_info(f"第 {i} 次点赞成功")
            time.sleep(1)
        
        return f"已点赞 {like_count}/5 次"
    
    def do_task_share_post(self) -> str:
        """执行分享任务"""
        result = self.share_post()
        return "分享成功" if result else "分享失败"
    
    def execute_tasks(self) -> SignInResult:
        """
        执行论坛每日任务
        :return: 签到结果
        """
        try:
            log_info("开始执行论坛每日任务")
            messages = []
            
            # 获取任务列表
            tasks = self.get_task_list()
            if not tasks:
                return SignInResult(
                    status=ResponseStatus.FAILED,
                    message="获取任务列表失败"
                )
            
            # 遍历未完成的任务
            for task in tasks:
                if int(task.get("process", 0)) == 1:
                    # 任务已完成，跳过
                    continue
                
                remark = task.get("remark", "")
                log_info(f"开始处理任务: {remark}")
                
                task_result = ""
                if remark == TaskType.SIGN_IN.value:
                    task_result = self.do_task_sign_in()
                elif remark == TaskType.VIEW_POSTS.value:
                    task_result = self.do_task_view_posts()
                elif remark == TaskType.LIKE_POSTS.value:
                    task_result = self.do_task_like_posts()
                elif remark == TaskType.SHARE_POST.value:
                    task_result = self.do_task_share_post()
                
                if task_result:
                    messages.append(f"{remark}: {task_result}")
                
                time.sleep(1)
            
            # 获取任务完成情况
            tasks = self.get_task_list()
            if tasks:
                gain_gold = sum(
                    task.get("gainGold", 0) 
                    for task in tasks 
                    if task.get("process") == 1
                )
                total_gold = self.get_total_gold()
                
                summary = f"今日任务已完成，总计获取金币: {gain_gold}"
                if total_gold is not None:
                    summary += f"；现在剩余：{total_gold} 金币"
                messages.append(summary)
                log_info(summary)
            
            result_message = "\n".join(messages)
            log_info("论坛签到流程完成")
            
            return SignInResult(
                status=ResponseStatus.SUCCESS,
                message=result_message
            )
            
        except Exception as e:
            message = f"论坛签到流程失败: {str(e)}"
            log_error(message)
            return SignInResult(
                status=ResponseStatus.FAILED,
                message=message
            )

