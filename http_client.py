"""
HTTP客户端封装
"""
import requests
from typing import Dict, Optional, Any
from log import log_debug, log_error, log_info
from models import ApiResponse, NetworkException
from constants import (
    BBS_HEADERS_TEMPLATE, 
    GAME_HEADERS_TEMPLATE, 
    USER_INFO_HEADERS_TEMPLATE
)
from tools import get_ip_address


class HttpClient:
    """HTTP客户端基类"""
    
    def __init__(self, timeout: int = 30):
        """
        初始化HTTP客户端
        :param timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = requests.Session()
    
    def _request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None,
        raise_on_error: bool = True
    ) -> ApiResponse:
        """
        统一的请求方法
        :param method: 请求方法（GET/POST）
        :param url: 请求URL
        :param headers: 请求头
        :param data: 请求数据
        :param raise_on_error: 是否在错误时抛出异常
        :return: API响应对象
        """
        try:
            log_debug(f"请求 {method} {url}")
            if data:
                log_debug(f"请求数据: {data}")
            
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            log_debug(f"响应: {response.text}")
            
            result = ApiResponse.from_dict(response.json())
            
            if not result.is_success() and raise_on_error:
                log_error(f"请求失败: {result.message}")
            
            return result
            
        except requests.RequestException as e:
            error_msg = f"网络请求失败: {str(e)}"
            log_error(error_msg)
            if raise_on_error:
                raise NetworkException(error_msg)
            return ApiResponse(
                success=False,
                code=-1,
                message=error_msg
            )
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            log_error(error_msg)
            if raise_on_error:
                raise NetworkException(error_msg)
            return ApiResponse(
                success=False,
                code=-1,
                message=error_msg
            )
    
    def post(
        self,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None,
        raise_on_error: bool = True
    ) -> ApiResponse:
        """POST请求"""
        return self._request("POST", url, headers, data, raise_on_error)
    
    def get(
        self,
        url: str,
        headers: Dict[str, str],
        raise_on_error: bool = True
    ) -> ApiResponse:
        """GET请求"""
        return self._request("GET", url, headers, raise_on_error=raise_on_error)


class KuroHttpClient(HttpClient):
    """库洛游戏HTTP客户端"""
    
    def __init__(self, token: str, devcode: Optional[str] = None, distinct_id: Optional[str] = None):
        """
        初始化库洛HTTP客户端
        :param token: 用户token
        :param devcode: 设备码
        :param distinct_id: 唯一标识
        """
        super().__init__()
        self.token = token
        self.devcode = devcode or ""
        self.distinct_id = distinct_id or ""
        self.ip = get_ip_address()
    
    def get_bbs_headers(self) -> Dict[str, str]:
        """生成论坛请求头"""
        headers = BBS_HEADERS_TEMPLATE.copy()
        headers.update({
            "Cookie": f"user_token={self.token}",
            "Ip": self.ip,
            "distinct_id": self.distinct_id,
            "devCode": self.devcode,
            "token": self.token,
        })
        return headers
    
    def get_game_headers(self) -> Dict[str, str]:
        """生成游戏签到请求头"""
        headers = GAME_HEADERS_TEMPLATE.copy()
        headers.update({
            "devCode": f"{self.ip}, Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
            "token": self.token,
        })
        return headers
    
    def get_user_info_headers(self) -> Dict[str, str]:
        """生成用户信息请求头"""
        headers = USER_INFO_HEADERS_TEMPLATE.copy()
        headers.update({
            "devcode": self.devcode,
            "distinct_id": self.distinct_id,
            "token": self.token,
        })
        return headers
    
    def bbs_post(self, url: str, data: Optional[Dict[str, Any]] = None, raise_on_error: bool = True) -> ApiResponse:
        """论坛POST请求"""
        return self.post(url, self.get_bbs_headers(), data, raise_on_error)
    
    def game_post(self, url: str, data: Optional[Dict[str, Any]] = None, raise_on_error: bool = True) -> ApiResponse:
        """游戏签到POST请求"""
        return self.post(url, self.get_game_headers(), data, raise_on_error)
    
    def user_info_post(self, url: str, data: Optional[Dict[str, Any]] = None, raise_on_error: bool = True) -> ApiResponse:
        """用户信息POST请求"""
        return self.post(url, self.get_user_info_headers(), data, raise_on_error)

