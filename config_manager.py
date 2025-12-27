"""
配置管理模块（重构版）
"""

import os
import uuid
from typing import Optional, List
import yaml
from log import log_info, log_error, log_debug
from models import (
    UserConfig,
    # ConfigException
)
from tools import get_user_info_by_token, get_game_user_id


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器
        :param config_dir: 配置目录路径
        """
        # 确定配置目录
        if config_dir:
            self.config_dir = config_dir
        elif os.environ.get("KuroBBS_config_path"):
            self.config_dir = os.environ.get("KuroBBS_config_path")
            log_info(f"使用环境变量配置路径: {self.config_dir}")
        else:
            self.config_dir = os.path.join(os.getcwd(), "config")
            log_info(f"使用默认配置路径: {self.config_dir}")

        # 确保配置目录存在
        os.makedirs(self.config_dir, exist_ok=True)

        # 获取配置文件前缀
        self.config_prefix = os.environ.get("KuroBBS_config_prefix", "")
        if self.config_prefix:
            log_info(f"配置文件将使用前缀: {self.config_prefix}")

    def get_config_path(self, user_name: str) -> str:
        """
        获取配置文件路径
        :param user_name: 用户名
        :return: 配置文件路径
        """
        return os.path.join(self.config_dir, f"{user_name}.yaml")

    def load_user_config(self, user_name: str) -> Optional[UserConfig]:
        """
        加载用户配置
        :param user_name: 用户名
        :return: 用户配置对象或None
        """
        config_path = self.get_config_path(user_name)

        if not os.path.exists(config_path):
            log_error(f"配置文件不存在: {config_path}")
            return None

        try:
            with open(config_path, "r", encoding="utf-8-sig") as f:
                data = yaml.safe_load(f)

            if not data:
                log_error(f"配置文件为空: {config_path}")
                return None

            # 检查是否缺少 retry_times 字段，如果缺少则补充默认值并保存
            if "retry_times" not in data:
                data["retry_times"] = 3
                log_info(f"{user_name} 配置缺少 retry_times 字段，已自动补充默认值 3")
                with open(config_path, "w", encoding="utf-8") as f:
                    yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)

            config = UserConfig.from_dict(user_name, data)
            log_debug(f"成功加载配置: {user_name}")
            return config

        except Exception as e:
            log_error(f"加载配置文件失败: {e}")
            return None

    def save_user_config(self, config: UserConfig) -> bool:
        """
        保存用户配置
        :param config: 用户配置对象
        :return: 是否成功
        """
        config_path = self.get_config_path(config.name)

        try:
            data = {
                "token": config.token,
                "enable": config.enable,
                "completed": config.completed,
                "auto_reple_sign": config.auto_replenish_sign,
                "retry_times": config.retry_times,
                "game_info": config.game_info,
                "user_info": config.user_info,
            }

            with open(config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)

            log_debug(f"成功保存配置: {config.name}")
            return True

        except Exception as e:
            log_error(f"保存配置文件失败: {e}")
            return False

    def update_user_config(self, user_name: str, key: str, value) -> bool:
        """
        更新用户配置的某个字段
        :param user_name: 用户名
        :param key: 配置键
        :param value: 配置值
        :return: 是否成功
        """
        config = self.load_user_config(user_name)
        if not config:
            return False

        # 使用setattr更新属性
        if hasattr(config, key):
            setattr(config, key, value)
            result = self.save_user_config(config)
            if result:
                log_info(f"已更新 {user_name} 的配置: {key} = {value}")
            return result
        else:
            log_error(f"配置键不存在: {key}")
            return False

    def disable_user(self, user_name: str) -> bool:
        """
        禁用用户
        :param user_name: 用户名
        :return: 是否成功
        """
        # 检查是否应该禁用该配置文件（避免误禁用其他工具的配置）
        if self.config_prefix and not user_name.startswith(self.config_prefix):
            log_info(f"未禁用非前缀配置文件: {user_name}.yaml (保留其他工具配置)")
            return False

        result = self.update_user_config(user_name, "enable", False)
        if result:
            log_info(f"已禁用用户: {user_name}")
        return result

    def enable_user(self, user_name: str) -> bool:
        """
        启用用户
        :param user_name: 用户名
        :return: 是否成功
        """
        result = self.update_user_config(user_name, "enable", True)
        if result:
            log_info(f"已启用用户: {user_name}")
        return result

    def fill_config(
        self,
        user_name: str,
        token: str,
        devcode: Optional[str] = None,
        distinct_id: Optional[str] = None,
    ) -> bool:
        """
        填充配置文件（自动获取用户信息和游戏角色ID）
        :param user_name: 用户名
        :param token: 用户token
        :param devcode: 设备码（可选）
        :param distinct_id: 唯一标识（可选）
        :return: 是否成功
        """
        config = self.load_user_config(user_name)
        if not config:
            log_error(f"配置文件不存在: {user_name}")
            return False

        try:
            # 生成或使用提供的设备信息
            devcode = devcode or str(uuid.uuid4())
            distinct_id = distinct_id or str(uuid.uuid4())

            # 更新设备信息
            config.game_info["devcode"] = devcode
            config.game_info["distinct_id"] = distinct_id

            # 获取用户ID
            user_id = get_user_info_by_token(token, devcode, distinct_id)
            if user_id:
                config.user_info["userId"] = user_id
            else:
                log_error(f"获取用户ID失败: {user_name}")
                return False

            # 获取游戏角色ID
            wuwa_role_id = get_game_user_id(token, 3, devcode, distinct_id)  # 鸣潮
            pgr_role_id = get_game_user_id(token, 2, devcode, distinct_id)  # 战双

            if wuwa_role_id:
                config.game_info["wwroleId"] = wuwa_role_id
            if pgr_role_id:
                config.game_info["eeeroleId"] = pgr_role_id

            # 标记为已完成
            config.completed = True

            # 保存配置
            if self.save_user_config(config):
                log_info(f"{user_name} 的配置文件已成功填充")
                return True

            return False

        except Exception as e:
            log_error(f"填充配置文件失败: {e}")
            return False

    def list_all_configs(self) -> List[str]:
        """
        列出所有配置文件
        :return: 用户名列表
        """
        try:
            files = os.listdir(self.config_dir)
            user_names = []

            for file in files:
                if file.endswith(".yaml"):
                    user_name = os.path.splitext(file)[0]

                    # 如果设置了前缀，只返回匹配前缀的文件
                    if self.config_prefix and not user_name.startswith(
                        self.config_prefix
                    ):
                        continue

                    user_names.append(user_name)

            log_debug(f"找到 {len(user_names)} 个配置文件")
            return user_names

        except Exception as e:
            log_error(f"列出配置文件失败: {e}")
            return []

    def list_enabled_configs(self) -> List[str]:
        """
        列出所有已启用的配置
        :return: 已启用的用户名列表
        """
        all_configs = self.list_all_configs()
        enabled = []

        for user_name in all_configs:
            config = self.load_user_config(user_name)
            if config and config.enable:
                enabled.append(user_name)

        return enabled
