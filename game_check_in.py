import requests
from log import log_info, log_debug, log_error
from tools import get_ip_address

class GameCheckIn:
    def __init__(self, token):
        """
        初始化 GameCheckIn 类
        :param token: 用户 token
        """
        self.token = token
        self.headers = self.get_game_headers()

    def get_game_headers(self):
        """
        生成游戏签到请求头
        :return: 请求头字典
        日志记录：无
        """
        headers = {
            "Host": "api.kurobbs.com",
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Site": "same-site",
            "devCode": f"{get_ip_address()}, Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
            "source": "ios",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "cors",
            "token": self.token,
            "Origin": "https://web-static.kurobbs.com",
            "Content-Length": "83",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KuroGameBox/2.2.0",
            "Connection": "keep-alive"
        }
        log_debug(f"生成游戏签到请求头: {headers}")
        return headers

    def get_sign_prize(self, game_id, server_id, role_id, user_id):
        """
        获取签到奖品
        :param game_id: 游戏 ID
        :param server_id: 服务器 ID
        :param role_id: 角色 ID
        :param user_id: 用户 ID
        :return: 奖品名称或错误信息
        日志记录：
            - debug: 签到奖品响应
            - debug: 成功获取签到奖品
            - error: 获取签到奖品失败
        """
        try:
            url = "https://api.kurobbs.com/encourage/signIn/queryRecordV2"
            data = {
                "gameId": game_id,
                "serverId": server_id,
                "roleId": role_id,
                "userId": user_id
            }
            response = requests.post(url, headers=self.headers, data=data)
            response.raise_for_status()
            log_debug(f"签到奖品响应: {response.text}")
            response_data = response.json()
            if response_data.get("code") != 200:
                error_message = f"获取签到奖品失败，响应代码: {response_data.get('code')}, 消息: {response_data.get('msg')}"
                log_error(error_message)
                return error_message
            data = response_data["data"]
            if isinstance(data, list) and len(data) > 0:
                first_goods_name = data[0]["goodsName"]
                log_debug(f"成功获取签到奖品: {first_goods_name}")
                return first_goods_name
            error_message = "签到奖品数据格式不正确或数据为空"
            log_error(error_message)
            return error_message
        except Exception as e:
            error_message = f"ERROR:获取签到奖品失败: {e}"
            log_error(error_message)
            return error_message

    def sign_in(self, game_id, server_id, role_id, user_id, month):
        """
        执行游戏签到
        :param game_id: 游戏 ID
        :param server_id: 服务器 ID
        :param role_id: 角色 ID
        :param user_id: 用户 ID
        :param month: 当前月份
        :return: 签到结果或错误信息
        日志记录：
            - debug: 游戏签到响应
            - info: 签到成功或已签到
            - error: 签到失败
        """
        try:
            url = "https://api.kurobbs.com/encourage/signIn/v2"
            data = {
                "gameId": game_id,
                "serverId": server_id,
                "roleId": role_id,
                "userId": user_id,
                "reqMonth": month
            }
            if game_id == 2:
                game_name = "战双"
            else:
                game_name = "鸣潮"
            response = requests.post(url, headers=self.headers, data=data)
            response.raise_for_status()
            log_debug(f"游戏签到响应: {response.text}")
            response_data = response.json()
            code = response_data.get("code")
            if code == 200:
                # 如果成功，调用 get_sign_prize 获取奖品列表
                goods_names = self.get_sign_prize(game_id, server_id, role_id, user_id)
                log_info(f"{game_name}签到成功，签到奖品: {goods_names}")
                return f"{game_name}签到成功，签到奖品: {goods_names}"
            elif code == 1511:
                goods_names = self.get_sign_prize(game_id, server_id, role_id, user_id)
                log_info(f"{game_name}今天已签到，签到奖品: {goods_names}")
                return f"{game_name}今天已签到，签到奖品: {goods_names}"
            elif code == 1513:
                log_error(f"{game_name}签到报错：用户信息异常")
                return f"{game_name}签到报错：用户信息异常"
            elif code == 220:
                log_error(f"{game_name}签到报错：登录已过期，请重新登录")
                return f"{game_name}签到报错：登录已过期，请重新登录"
            else:
                error_message = f"{game_name}签到失败，响应代码: {code}, 消息: {response_data.get('msg')}"
                log_error(error_message)
                return error_message
        except Exception as e:
            error_message = f"签到失败: {e}"
            log_error(error_message)
            return error_message