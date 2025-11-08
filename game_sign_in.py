"""
游戏签到模块（重构版）
"""
from typing import Optional
from log import log_info, log_debug, log_error
from http_client import KuroHttpClient
from constants import API, GameType, ErrorCode
from models import SignInResult, ResponseStatus, TokenExpiredException, UserInfoException


class GameSignIn:
    """游戏签到类"""
    
    def __init__(self, client: KuroHttpClient):
        """
        初始化游戏签到
        :param client: HTTP客户端
        """
        self.client = client
    
    def get_sign_reward(
        self,
        game_type: GameType,
        role_id: str,
        user_id: str
    ) -> Optional[str]:
        """
        获取签到奖励信息
        :param game_type: 游戏类型
        :param role_id: 角色ID
        :param user_id: 用户ID
        :return: 奖励名称或None
        """
        try:
            data = {
                "gameId": game_type.value,
                "serverId": game_type.server_id,
                "roleId": role_id,
                "userId": user_id
            }
            
            response = self.client.game_post(API.GAME_SIGN_RECORD, data, raise_on_error=False)
            log_debug(f"获取签到奖励响应: {response.message}")
            
            if response.is_success() and response.data:
                if isinstance(response.data, list) and len(response.data) > 0:
                    reward_name = response.data[0].get("goodsName", "未知奖励")
                    log_debug(f"成功获取签到奖励: {reward_name}")
                    return reward_name
            
            log_error(f"获取签到奖励失败: {response.message}")
            return None
            
        except Exception as e:
            log_error(f"获取签到奖励失败: {e}")
            return None
    
    def check_replenish_count(
        self,
        game_type: GameType,
        role_id: str,
        user_id: str
    ) -> int:
        """
        检查可补签次数
        :param game_type: 游戏类型
        :param role_id: 角色ID
        :param user_id: 用户ID
        :return: 可补签次数
        """
        try:
            data = {
                "gameId": game_type.value,
                "serverId": game_type.server_id,
                "roleId": role_id,
                "userId": user_id
            }
            
            response = self.client.game_post(API.GAME_SIGN_INIT, data, raise_on_error=False)
            log_debug(f"检查补签响应: {response.message}")
            
            if response.is_success() and response.data:
                omission_num = response.data.get("omissionNum", 0)
                log_info(f"{game_type.name_zh} 可补签天数: {omission_num}")
                return omission_num
            
            log_error(f"检查补签失败: {response.message}")
            return 0
            
        except Exception as e:
            log_error(f"检查补签失败: {e}")
            return 0
    
    def replenish_sign(
        self,
        game_type: GameType,
        role_id: str,
        user_id: str,
        month: str
    ) -> SignInResult:
        """
        执行补签
        :param game_type: 游戏类型
        :param role_id: 角色ID
        :param user_id: 用户ID
        :param month: 月份
        :return: 签到结果
        """
        try:
            data = {
                "gameId": game_type.value,
                "serverId": game_type.server_id,
                "roleId": role_id,
                "userId": user_id,
                "reqMonth": month
            }
            
            log_info(f"{game_type.name_zh} 开始补签")
            response = self.client.game_post(API.GAME_REPLENISH_SIGN, data, raise_on_error=False)
            
            if response.code == ErrorCode.SUCCESS.value:
                reward = self.get_sign_reward(game_type, role_id, user_id)
                message = f"{game_type.name_zh} 补签成功"
                if reward:
                    message += f"，补签奖励: {reward}"
                log_info(message)
                return SignInResult(
                    status=ResponseStatus.SUCCESS,
                    message=message,
                    details={"reward": reward}
                )
            else:
                message = f"{game_type.name_zh} 补签失败: {response.message}"
                log_error(message)
                return SignInResult(
                    status=ResponseStatus.FAILED,
                    message=message
                )
                
        except Exception as e:
            message = f"{game_type.name_zh} 补签失败: {str(e)}"
            log_error(message)
            return SignInResult(
                status=ResponseStatus.FAILED,
                message=message
            )
    
    def sign_in(
        self,
        game_type: GameType,
        role_id: str,
        user_id: str,
        month: str,
        auto_replenish: bool = False
    ) -> SignInResult:
        """
        执行游戏签到
        :param game_type: 游戏类型
        :param role_id: 角色ID
        :param user_id: 用户ID
        :param month: 月份
        :param auto_replenish: 是否自动补签
        :return: 签到结果
        """
        try:
            data = {
                "gameId": game_type.value,
                "serverId": game_type.server_id,
                "roleId": role_id,
                "userId": user_id,
                "reqMonth": month
            }
            
            log_info(f"{game_type.name_zh} 开始签到")
            response = self.client.game_post(API.GAME_SIGN_IN, data, raise_on_error=False)
            
            # 处理签到结果
            if response.code == ErrorCode.SUCCESS.value:
                reward = self.get_sign_reward(game_type, role_id, user_id)
                message = f"{game_type.name_zh} 签到成功"
                if reward:
                    message += f"，签到奖励: {reward}"
                log_info(message)
                result = SignInResult(
                    status=ResponseStatus.SUCCESS,
                    message=message,
                    details={"reward": reward}
                )
                
            elif response.code == ErrorCode.ALREADY_SIGNED.value:
                reward = self.get_sign_reward(game_type, role_id, user_id)
                message = f"{game_type.name_zh} 今天已签到"
                if reward:
                    message += f"，签到奖励: {reward}"
                log_info(message)
                result = SignInResult(
                    status=ResponseStatus.SUCCESS,
                    message=message,
                    details={"reward": reward}
                )
                
            elif response.code == ErrorCode.USER_INFO_ERROR.value:
                message = f"{game_type.name_zh} 签到报错：用户信息异常"
                log_error(message)
                raise UserInfoException(message)
                
            elif response.code == ErrorCode.LOGIN_EXPIRED.value:
                message = f"{game_type.name_zh} 签到报错：登录已过期，请重新登录"
                log_error(message)
                raise TokenExpiredException(message)
                
            else:
                message = f"{game_type.name_zh} 签到失败: {response.message} (代码: {response.code})"
                log_error(message)
                return SignInResult(
                    status=ResponseStatus.FAILED,
                    message=message
                )
            
            # 自动补签
            if auto_replenish and result.status == ResponseStatus.SUCCESS:
                omission_count = self.check_replenish_count(game_type, role_id, user_id)
                if omission_count > 0:
                    replenish_result = self.replenish_sign(game_type, role_id, user_id, month)
                    result.message += f"\n{replenish_result.message}"
            
            return result
            
        except (TokenExpiredException, UserInfoException):
            # 重新抛出这些异常，让上层处理
            raise
        except Exception as e:
            message = f"{game_type.name_zh} 签到失败: {str(e)}"
            log_error(message)
            return SignInResult(
                status=ResponseStatus.FAILED,
                message=message
            )

