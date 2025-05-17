import os
import logging
import argparse
from log import setup_logger, log_info, log_error
from config import ConfigManager
from game_check_in import GameCheckIn
from bbs_sign_in import KuroBBS
import datetime
import time

# 使用环境变量或默认路径
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.environ.get('KuroBBS_config_path', os.path.join(FILE_PATH, 'config'))
# 在 main.py 和 push.py 中修改
push_dir = os.environ.get('KuroBBS_push_path')
if push_dir:
    # 如果设置了KuroBBS_push_path，将其视为目录
    PUSH_CONFIG_PATH = os.path.join(push_dir, 'push.ini')
else:
    # 否则使用默认配置目录
    PUSH_CONFIG_PATH = os.path.join(CONFIG_DIR, 'push.ini')

class SignInManager(ConfigManager):
    def __init__(self, config_dir=None):
        super().__init__(config_dir)


    def sign_in_user(self, user_name):
        """
        执行单个用户的签到
        :param user_name: 用户名（文件名，不含扩展名）
        :return: 签到结果消息
        """
        msg = ""
        user_config = self.load_user_config(user_name)
        msg += f"{user_name} 签到开始\n"
        log_info(f"{user_name} 签到开始")
        if not user_config:
            msg = f"{user_name} 配置加载失败，跳过签到\n"
            log_error(f"{user_name} 配置加载失败，跳过签到")
            return msg

        if not user_config.get("enable", True):
            msg += f"{user_name} 已禁用，跳过签到\n"
            log_info(f"{user_name} 已禁用，跳过签到")
            return msg

        token = user_config.get("token")
        if not token:
            msg += f"{user_name} 的 token 为空，跳过签到\n"
            log_error(f"{user_name} 的 token 为空，跳过签到")
            self.disable_user(user_name)
            log_info(f"禁用{user_name}")
            return msg

        if not user_config.get("completed", False):
            log_info(f"{user_name} 配置文件不完整，开始执行填充流程")
            self.fill_raw_config(user_name, token)
            user_config = self.load_user_config(user_name)

        msg = f"{user_name} 签到开始\n"
        try:
            # 游戏签到
            game_check = GameCheckIn(token)
            for game_id, role_id in [("3", user_config.get("game_info", {}).get("wwroleId")),
                                     ("2", user_config.get("game_info", {}).get("eeeroleId"))]:
                if role_id:
                    msg += self.sign_in_game(game_check, game_id, role_id, user_config.get("user_info", {}).get("userId"), user_config.get("auto_reple_sign", False))

            # 库街区签到
            bbs = KuroBBS(token, user_config.get("game_info", {}).get("devcode"), user_config.get("game_info", {}).get("distinct_id"))
            msg += bbs.sign_in()

            msg += f"{user_name} 签到结束\n"
            log_info(f"{user_name} 签到完成")
        except Exception as e:
            log_error(f"{user_name} 签到失败: {e}")
            msg += f"{user_name} 签到失败: {e}\n"
        
        # 如果返回信息中包含用户信息异常，则禁用该用户
        if "用户信息异常" in msg:
            log_error(f"{user_name} 返回‘用户信息异常’，系统将自动禁用该用户")
            self.disable_user(user_name)
        
        return msg

    def sign_in_game(self, game_check, game_id, role_id, user_id, auto_reple_sign):
        """
        执行游戏签到
        """
        try:
            msg = game_check.sign_in(game_id, role_id, user_id, datetime.datetime.now().strftime("%m"), auto_reple_sign)
            return msg + "\n"
        except Exception as e:
            log_error(f"游戏签到失败: {e}")
            return f"游戏签到失败: {e}\n"

    def run(self):
        """
        执行所有用户的签到
        """
        messages = []
        success_users = []
        error_users = []
        log_info(datetime.datetime.now().strftime("%Y-%m-%d") + " 开始签到")
        messages.append(datetime.datetime.now().strftime("%Y-%m-%d") + " 开始签到任务\n")

        for file in os.listdir(self.config_dir):
            if file.endswith(".yaml"):
                # 检查配置文件是否符合前缀要求
                user_name = os.path.splitext(file)[0]
                
                # 如果设置了前缀，检查文件是否匹配前缀
                if self.config_prefix and not user_name.startswith(self.config_prefix):
                    log_info(f"跳过不匹配前缀的文件: {file}")
                    continue
                
                time.sleep(1)  # 避免请求过快
                msg = self.sign_in_user(user_name)
                messages.append(msg)

                if "ERROR" in msg or "跳过签到" in msg:
                    error_users.append(user_name)
                else:
                    success_users.append(user_name)

                # 如果消息中包含"用户信息异常"，禁用该用户
                if "用户信息异常" in msg:
                    log_error(f"{user_name} 返回'用户信息异常'，系统将自动禁用该用户")
                    self.disable_user(user_name)

        # 总结签到结果
        summary_message = datetime.datetime.now().strftime("%Y-%m-%d") + " 签到结果总结：\n"
        summary_message += f"签到成功的用户: {', '.join(success_users) if success_users else '无'}\n"
        summary_message += f"签到失败的用户: {', '.join(error_users) if error_users else '无'}\n"
        log_info(summary_message)
        messages.append(summary_message)

        return messages

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="库街区签到任务")
    parser.add_argument("--debug", action="store_true", help="启用 DEBUG 日志级别")
    parser.add_argument("--error", action="store_true", help="启用 ERROR 日志级别")
    return parser.parse_args()


def load_push_config():
    """
    加载推送配置
    :return: 推送配置数据
    """
    if not os.path.exists(PUSH_CONFIG_PATH):
        log_error(f"推送配置文件不存在: {PUSH_CONFIG_PATH}")
        return None
    import configparser
    config = configparser.ConfigParser()
    config.read(PUSH_CONFIG_PATH, encoding="utf-8-sig")
    if 'setting' not in config:
        log_error("推送配置文件中缺少 [setting] 部分")
        return None
    log_info("成功加载推送配置")
    return {
        "enable": config.getboolean('setting', 'enable', fallback=False),
        "push_level": config.getint('setting', 'push_level', fallback=1),
        "push_server": config.get('setting', 'push_server', fallback=''),
    }


def main():
    args = parse_arguments()

    # 根据命令行参数设置日志级别
    if args.debug:
        setup_logger(log_level=logging.DEBUG)
    elif args.error:
        setup_logger(log_level=logging.ERROR)
    else:
        setup_logger(log_level=logging.INFO)

    manager = SignInManager(CONFIG_DIR)
    messages = manager.run()

    # 推送签到结果
    push_settings = load_push_config()
    if push_settings and push_settings["enable"]:
        log_info("推送服务已启用")
        from push import push
        if push_settings["push_level"] == 1:
            push(messages[-1])
        elif push_settings["push_level"] == 2:
            push("\n".join(messages))
        elif push_settings["push_level"] == 3:
            for msg in messages:
                push(msg)
        else:
            log_error("未知的推送服务级别")
    else:
        log_info("推送服务未启用")

if __name__ == "__main__":
    main()
