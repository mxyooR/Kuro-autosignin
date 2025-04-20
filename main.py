"""
任务名称
name: 库街区签到任务
定时规则
cron: 1 9 * * *
"""
import configparser
import time
import datetime
import json
import argparse
from log import setup_logger, log_info, log_error
from tools import fill_raw_config
import logging
from game_check_in import GameCheckIn
from bbs_sign_in import KuroBBS
import os
import yaml  # 新增 YAML 导入


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = FILE_PATH + '/config'  
PUSH_PATH = FILE_PATH + '/config/push.ini'



def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="库街区签到任务")
    parser.add_argument("--debug", action="store_true", help="启用 DEBUG 日志级别")
    parser.add_argument("--error", action="store_true", help="启用 ERROR 日志级别")
    return parser.parse_args()

def update_user_status(user_to_update):
    """更新指定用户状态到配置文件"""
    with open(DATA_PATH+user_to_update+".yaml", 'r', encoding="utf-8-sig") as f:
        data = yaml.safe_load(f)

    data["enable"] = False  # 将 enable 设置为 False

    with open(DATA_PATH+user_to_update+".yaml", 'w', encoding="utf-8-sig") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")
    msglist= []
    success_users = []  # 记录签到成功的用户
    error_users = []    # 记录签到过程中发生错误的用户
    # 从YAML文件中读取数据
    for file in os.listdir(DATA_PATH):
        print(file)
        if file.endswith(".yaml"):
            msg= ""
            with open(DATA_PATH+ "/"+file, 'r', encoding="utf-8-sig") as f:
                data = yaml.safe_load(f)

            fill_raw_config(DATA_PATH+ "/"+file, data["token"])
            name = data.get("name", "unknown")
            token= data.get("token")
            enable = data.get("enable")
            if not enable:
                    log_info(f"{name} 已禁用，跳过签到")
                    msglist.append(f"{name} 已禁用，跳过签到")
                    continue
            if token is None:
                    log_error(f"{name} 的 token 为空，跳过签到")
                    msglist.append(f"{name} 的 token 为空，跳过签到")
                    continue

            wwroleId = data.get("game_info", {}).get("wwroleId")
            eeeroleId = data.get("game_info", {}).get("eeeroleId")
            devcode = data.get("game_info", {}).get("devcode")
            distinct_id = data.get("game_info", {}).get("distinct_id")
            userId = data.get("user_info", {}).get("userId")
            log_info(f"{name} 开始签到")
            msg += f" {name} 签到\n"


        
            try:
                    # 实例化游戏签到类
                    GameCheck = GameCheckIn(token)
                    # 鸣潮签到
                    if wwroleId:
                        log_info(f"{name} 开始鸣潮签到")
                        msg += f"{name} 开始鸣潮签到\n"
                        ww_msg = GameCheck.sign_in(
                            game_id=3,
                            server_id="76402e5b20be2c39f095a152090afddc",
                            role_id=wwroleId,
                            user_id=userId,
                            month=month
                        )
                        if "登录已过期" in ww_msg or "用户信息异常" in ww_msg:
                            log_error(f"{name} 用户登录信息已失效，禁用该用户")
                            msg += f"{name} 用户登录信息已失效，禁用该用户\n"
                            enable = False
                            update_user_status(name)  # 更新该用户状态 
                            error_users.append(name)
                            msglist.append(msg)
                            continue
                        if "ERROR" in ww_msg:
                            error_users.append(name)
                        msg += f"{ww_msg}\n"

                    # 战双签到
                    if eeeroleId:
                        log_info(f"{name} 开始战双签到")
                        msg += f"{name} 开始战双签到\n"
                        ee_msg = GameCheck.sign_in(
                            game_id=2,
                            server_id=1000,
                            role_id=eeeroleId,
                            user_id=userId,
                            month=month
                        )
                        if "登录已过期" in ee_msg or "用户信息异常" in ee_msg:
                            log_error(f"{name} 用户登录信息已失效，禁用该用户")
                            msg += f"{name} 用户登录信息已失效，禁用该用户\n"
                            enable = False
                            update_user_status(name)
                            error_users.append(name)
                            msglist.append(msg)
                            continue
                        if "ERROR" in ee_msg:
                            error_users.append(name)
                        msg += f"{ee_msg}\n"

                    time.sleep(1)

                    # 库街区签到
                    krbbs = KuroBBS(token, devcode, distinct_id)
                    kuro_msg = krbbs.sign_in()
                    if "登录已过期" in kuro_msg or "用户信息异常" in kuro_msg:
                        log_error(f"{name} 用户登录信息已失效，禁用该用户")
                        msg += f"{name} 用户登录信息已失效，禁用该用户\n"
                        enable = False
                        update_user_status(name)
                        error_users.append(name)
                        msglist.append(msg)
                        continue
                    if "ERROR" in kuro_msg:
                        error_users.append(name)

                    msg += kuro_msg
                    msg += f"{name} 签到结束\n"
                    msg += "=====================================\n"
                    log_info(f"{name} 签到结束")
                    log_info("=====================================")
                    if name not in error_users:
                        success_users.append(name)

            except Exception as e:
                    log_error(f"{name} 签到过程中发生错误: {e}")
                    msg += f"{name} 签到过程中发生错误: {e}\n"
                    error_users.append(name)

    # 总结签到结果
    summary_message = "签到结果总结：\n"
    summary_message += f"签到成功的用户: {', '.join(success_users) if success_users else '无'}\n"
    summary_message += f"签到失败的用户: {', '.join(error_users) if error_users else '无'}\n"
    log_info(summary_message)
    msglist.append(summary_message)
    return msglist


def get_push_settings():
    """获取推送设置"""
    if not os.path.exists(PUSH_PATH):
        log_info(f"推送配置文件不存在: {PUSH_PATH}")
        return None

    config = configparser.ConfigParser()
    config.read(PUSH_PATH, encoding="utf-8-sig")

    if 'setting' not in config:
        log_error("推送配置文件中缺少 [setting] 部分")
        return None

    enable = config.getboolean('setting', 'enable', fallback=False)
    push_level = config.getint('setting', 'push_level', fallback=1)
    push_server = config.get('setting', 'push_server', fallback='')


    return {
        "enable": enable,
        "push_level": push_level,
        "push_server": push_server,
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

        msglist = sign_in()
        push_settings = get_push_settings()
        if push_settings is not None:
            enable = push_settings["enable"]
            push_level = push_settings["push_level"]
            push_server = push_settings["push_server"]

            if enable:
                log_info("推送服务已启用")
                from push import push
                if push_level == 1:
                    log_info("推送服务级别为 1")
                    # 只推送总结信息
                    push(msglist[-1], push_server)
                elif push_level == 2:
                    log_info("推送服务级别为 2")
                    # 推送所有人的详细信息合并为一条
                    push("\n".join(msglist), push_server)
                elif push_level == 3:
                    log_info("推送服务级别为 3")
                    # 推送所有人的详细信息逐条发送
                    for msg in msglist:
                        push(msg, push_server)
                else:
                    log_error("未知的推送服务级别")
            else:
                log_info("推送服务未启用")

if __name__ == "__main__":
    main()