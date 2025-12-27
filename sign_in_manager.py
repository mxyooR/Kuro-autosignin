"""
签到管理模块（重构版）
"""

import time
import datetime
from typing import List, Tuple
from log import log_info, log_error
from config_manager import ConfigManager
from models import (
    # UserConfig,
    # SignInResult,
    ResponseStatus,
    TaskSummary,
    TokenExpiredException,
    UserInfoException,
)
from http_client import KuroHttpClient
from game_sign_in import GameSignIn
from forum_sign_in import ForumSignIn
from constants import GameType
from tools import random_delay


class SignInManager:
    """签到管理器"""

    def __init__(self, config_manager: ConfigManager):
        """
        初始化签到管理器
        :param config_manager: 配置管理器
        """
        self.config_manager = config_manager

    def sign_in_user(self, user_name: str) -> Tuple[ResponseStatus, List[str]]:
        """
        执行单个用户的签到，如果失败则随机延迟后重试
        :param user_name: 用户名
        :return: (状态, 消息列表)
        """
        # 先加载用户配置以获取重试次数
        config = self.config_manager.load_user_config(user_name)
        if not config:
            messages = []
            msg = f"{user_name} 配置加载失败，跳过签到"
            messages.append(msg)
            log_error(msg)
            return ResponseStatus.FAILED, messages

        # 从配置中读取重试次数（默认3）
        max_retries = config.get_max_retries()
        
        retry_count = 0
        
        while retry_count <= max_retries:
            messages = []
            if retry_count == 0:
                messages.append(f"{user_name} 签到开始")
                log_info(f"{user_name} 签到开始")
            else:
                messages.append(f"{user_name} 签到重试 (第 {retry_count}/{max_retries} 次)")
                log_info(f"{user_name} 签到重试 (第 {retry_count}/{max_retries} 次)")

            # 检查是否启用
            if not config.enable:
                msg = f"{user_name} 已禁用，跳过签到"
                messages.append(msg)
                log_info(msg)
                return ResponseStatus.SKIPPED, messages

            # 检查token
            if not config.token:
                msg = f"{user_name} 的 token 为空，跳过签到"
                messages.append(msg)
                log_error(msg)
                self.config_manager.disable_user(user_name)
                return ResponseStatus.FAILED, messages

            # 检查配置是否完整
            if not config.completed:
                log_info(f"{user_name} 配置文件不完整，开始执行填充流程")
                if not self.config_manager.fill_config(user_name, config.token):
                    msg = f"{user_name} 配置填充失败，跳过签到"
                    messages.append(msg)
                    log_error(msg)
                    return ResponseStatus.FAILED, messages
                # 重新加载配置
                config = self.config_manager.load_user_config(user_name)

            try:
                # 创建HTTP客户端
                client = KuroHttpClient(
                    token=config.token,
                    devcode=config.get_devcode(),
                    distinct_id=config.get_distinct_id(),
                )

                # 游戏签到
                game_signer = GameSignIn(client)
                current_month = datetime.datetime.now().strftime("%m")

                # 鸣潮签到
                wuwa_role_id = config.get_game_role_id("3")
                if wuwa_role_id:
                    result = game_signer.sign_in(
                        game_type=GameType.WUWA,
                        role_id=wuwa_role_id,
                        user_id=config.get_user_id(),
                        month=current_month,
                        auto_replenish=config.auto_replenish_sign,
                    )
                    messages.append(result.message)

                # 战双签到
                pgr_role_id = config.get_game_role_id("2")
                if pgr_role_id:
                    result = game_signer.sign_in(
                        game_type=GameType.PGR,
                        role_id=pgr_role_id,
                        user_id=config.get_user_id(),
                        month=current_month,
                        auto_replenish=config.auto_replenish_sign,
                    )
                    messages.append(result.message)

                # 论坛签到
                forum_signer = ForumSignIn(client)
                result = forum_signer.execute_tasks()
                messages.append(result.message)

                messages.append(f"{user_name} 签到结束")
                log_info(f"{user_name} 签到完成")

                return ResponseStatus.SUCCESS, messages

            except TokenExpiredException:
                msg = f"{user_name} 登录已过期，自动禁用该用户"
                messages.append(msg)
                log_error(msg)
                self.config_manager.disable_user(user_name)
                return ResponseStatus.FAILED, messages

            except UserInfoException:
                msg = f"{user_name} 用户信息异常，自动禁用该用户"
                messages.append(msg)
                log_error(msg)
                self.config_manager.disable_user(user_name)
                return ResponseStatus.FAILED, messages

            except Exception as e:
                msg = f"{user_name} 签到失败: {str(e)}"
                messages.append(msg)
                log_error(msg)
                
                # 如果还有重试次数，则随机延迟后重试
                retry_count += 1
                if retry_count <= max_retries:
                    log_info(f"{user_name} 将在随机延迟后进行第 {retry_count}/{max_retries} 次重试")
                    # 使用默认随机延迟（5-15秒），避免配置繁琐
                    random_delay()
                    continue
                else:
                    # 达到最大重试次数，返回失败
                    final_msg = f"{user_name} 重试 {max_retries} 次后仍然失败，放弃签到"
                    messages.append(final_msg)
                    log_error(final_msg)
                    return ResponseStatus.FAILED, messages

    def run_all(self) -> Tuple[TaskSummary, List[str]]:
        """
        执行所有用户的签到
        :return: (任务总结, 详细消息列表)
        """
        all_messages = []
        success_users = []
        failed_users = []
        disabled_users = []

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_msg = f"{current_date} 开始签到任务"
        all_messages.append(start_msg)
        log_info(start_msg)

        # 获取所有配置
        user_names = self.config_manager.list_all_configs()

        for user_name in user_names:
            # 等待避免请求过快
            time.sleep(1)

            status, messages = self.sign_in_user(user_name)
            all_messages.extend(messages)

            # 统计结果
            if status == ResponseStatus.SKIPPED:
                # 跳过的用户不计入统计
                continue
            elif status == ResponseStatus.FAILED:
                # 检查是否被禁用
                config = self.config_manager.load_user_config(user_name)
                if config and not config.enable:
                    disabled_users.append(user_name)
                else:
                    failed_users.append(user_name)
            else:
                success_users.append(user_name)

        # 创建任务总结
        summary = TaskSummary(
            date=current_date,
            success_users=success_users,
            failed_users=failed_users,
            disabled_users=disabled_users,
        )

        summary_msg = str(summary)
        log_info(summary_msg)
        all_messages.append(summary_msg)

        return summary, all_messages
