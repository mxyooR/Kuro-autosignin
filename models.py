"""
数据模型和响应类
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict, List
from enum import Enum


class ResponseStatus(Enum):
    """响应状态"""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ApiResponse:
    """统一的API响应模型"""

    success: bool
    code: int
    message: str
    data: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ApiResponse":
        """从字典创建响应对象"""
        code = data.get("code", 0)
        return cls(
            success=code == 200,
            code=code,
            message=data.get("msg", ""),
            data=data.get("data"),
        )

    def is_success(self) -> bool:
        """判断是否成功"""
        return self.success and self.code == 200


@dataclass
class SignInResult:
    """签到结果"""

    status: ResponseStatus
    message: str
    details: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        """格式化输出"""
        return self.message


@dataclass
class UserConfig:
    """用户配置"""

    name: str
    token: str
    enable: bool = True
    completed: bool = False
    auto_replenish_sign: bool = False
    game_info: Optional[Dict[str, str]] = None
    user_info: Optional[Dict[str, str]] = None
    retry_times: Optional[int] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.game_info is None:
            self.game_info = {}
        if self.user_info is None:
            self.user_info = {}
        if self.retry_times is None:
            self.retry_times = 3

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "UserConfig":
        """从字典创建用户配置"""
        return cls(
            name=name,
            token=data.get("token", ""),
            enable=data.get("enable", True),
            completed=data.get("completed", False),
            auto_replenish_sign=data.get("auto_reple_sign", False),
            game_info=data.get("game_info", {}),
            user_info=data.get("user_info", {}),
            retry_times=data.get("retry_times", 3),
        )

    def get_game_role_id(self, game_type: str) -> Optional[str]:
        """获取游戏角色ID"""
        if game_type == "3":  # 鸣潮
            return self.game_info.get("wwroleId")
        elif game_type == "2":  # 战双
            return self.game_info.get("eeeroleId")
        return None

    def get_user_id(self) -> Optional[str]:
        """获取用户ID"""
        return self.user_info.get("userId")

    def get_devcode(self) -> Optional[str]:
        """获取设备码"""
        return self.game_info.get("devcode")

    def get_distinct_id(self) -> Optional[str]:
        """获取唯一标识"""
        return self.game_info.get("distinct_id")

    def get_max_retries(self) -> int:
        """获取最大重试次数（默认3）"""
        try:
            value = int(self.retry_times) if self.retry_times is not None else 3
            return value if value >= 1 else 1
        except Exception:
            return 3


@dataclass
class TaskSummary:
    """任务总结"""

    date: str
    success_users: List[str]
    failed_users: List[str]
    disabled_users: List[str]

    def __str__(self) -> str:
        """格式化输出"""
        lines = [
            f"{self.date} 签到结果总结：",
            f"签到成功的用户: {', '.join(self.success_users) if self.success_users else '无'}",
            f"签到失败的用户: {', '.join(self.failed_users) if self.failed_users else '无'}",
        ]
        if self.disabled_users:
            lines.append(f"已自动禁用的用户: {', '.join(self.disabled_users)}")
        return "\n".join(lines)


class KuroException(Exception):
    """库洛游戏相关异常基类"""

    pass


class TokenExpiredException(KuroException):
    """Token过期异常"""

    pass


class UserInfoException(KuroException):
    """用户信息异常"""

    pass


class NetworkException(KuroException):
    """网络请求异常"""

    pass


class ConfigException(KuroException):
    """配置异常"""

    pass
