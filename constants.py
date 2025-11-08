"""
常量和枚举定义
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict


class GameType(Enum):
    """游戏类型枚举"""
    PGR = "2"  # 战双帕弥什
    WUWA = "3"  # 鸣潮

    @property
    def name_zh(self) -> str:
        """获取中文名称"""
        return {
            GameType.PGR: "战双",
            GameType.WUWA: "鸣潮"
        }[self]

    @property
    def server_id(self) -> str:
        """获取服务器ID"""
        return {
            GameType.PGR: "1000",
            GameType.WUWA: "76402e5b20be2c39f095a152090afddc"
        }[self]


class TaskType(Enum):
    """任务类型枚举"""
    SIGN_IN = "用户签到"
    VIEW_POSTS = "浏览3篇帖子"
    LIKE_POSTS = "点赞5次"
    SHARE_POST = "分享1次帖子"


class ErrorCode(Enum):
    """错误代码枚举"""
    SUCCESS = 200
    ALREADY_SIGNED = 1511
    USER_INFO_ERROR = 1513
    LOGIN_EXPIRED = 220


@dataclass
class ApiEndpoint:
    """API端点配置"""
    # 用户相关
    USER_MINE: str = "https://api.kurobbs.com/user/mineV2"
    USER_SIGN_IN: str = "https://api.kurobbs.com/user/signIn"
    USER_ROLE_LIST: str = "https://api.kurobbs.com/user/role/findRoleList"
    
    # 论坛相关
    FORUM_LIST: str = "https://api.kurobbs.com/forum/list"
    FORUM_POST_DETAIL: str = "https://api.kurobbs.com/forum/getPostDetail"
    FORUM_LIKE: str = "https://api.kurobbs.com/forum/like"
    
    # 任务相关
    TASK_PROCESS: str = "https://api.kurobbs.com/encourage/level/getTaskProcess"
    TASK_SHARE: str = "https://api.kurobbs.com/encourage/level/shareTask"
    
    # 金币相关
    GOLD_TOTAL: str = "https://api.kurobbs.com/encourage/gold/getTotalGold"
    
    # 游戏签到相关
    GAME_SIGN_IN: str = "https://api.kurobbs.com/encourage/signIn/v2"
    GAME_SIGN_RECORD: str = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
    GAME_SIGN_INIT: str = "https://api.kurobbs.com/encourage/signIn/initSignInV2"
    GAME_REPLENISH_SIGN: str = "https://api.kurobbs.com/encourage/signIn/repleSigInV2"


# API端点实例
API = ApiEndpoint()


# 请求头模板
COMMON_HEADERS: Dict[str, str] = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

BBS_HEADERS_TEMPLATE: Dict[str, str] = {
    **COMMON_HEADERS,
    "Host": "api.kurobbs.com",
    "source": "ios",
    "lang": "zh-Hans",
    "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
    "channelId": "1",
    "channel": "appstore",
    "version": "2.2.0",
    "model": "iPhone15,2",
    "osVersion": "17.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
}

GAME_HEADERS_TEMPLATE: Dict[str, str] = {
    **COMMON_HEADERS,
    "Host": "api.kurobbs.com",
    "Accept": "application/json, text/plain, */*",
    "Sec-Fetch-Site": "same-site",
    "source": "ios",
    "Sec-Fetch-Mode": "cors",
    "Origin": "https://web-static.kurobbs.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
}

USER_INFO_HEADERS_TEMPLATE: Dict[str, str] = {
    "osversion": "Android",
    "countrycode": "CN",
    "ip": "10.0.2.233",
    "model": "2211133C",
    "source": "android",
    "lang": "zh-Hans",
    "version": "1.0.9",
    "versioncode": "1090",
    "content-type": "application/x-www-form-urlencoded",
    "accept-encoding": "gzip",
    "user-agent": "okhttp/3.10.0",
}

