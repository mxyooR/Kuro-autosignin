"""
任务名称
name: 库街区签到任务
定时规则
cron: 1 9 * * *
"""
import time
import datetime
import json
import argparse
from log import setup_logger, log_info, log_error
from tools import update_config_from_old_version
import logging
from game_check_in import GameCheckIn
from bbs_sgin_in import KuroBBS
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = FILE_PATH + '/config/data.json'


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="库街区签到任务")
    parser.add_argument("--debug", action="store_true", help="启用 DEBUG 日志级别")
    parser.add_argument("--error", action="store_true", help="启用 ERROR 日志级别")
    return parser.parse_args()

def update_user_status(user_to_update):
    """更新指定用户状态到配置文件"""
    with open(DATA_PATH, 'r', encoding="utf-8-sig") as f:
        data = json.load(f)

    for user in data['users']:
        if user['name'] == user_to_update['name']:
            user.update(user_to_update)  # 更新指定用户的状态

    with open(DATA_PATH, 'w', encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")

    # 从JSON文件中读取数据
    with open(DATA_PATH, 'r', encoding="utf-8-sig") as f:
        data = json.load(f)

    distinct_id = data['distinct_id']
    users = data['users']
    checkpush = data['push']
    server_message = f"{now.strftime('%Y-%m-%d')} 开始签到\n"
    server_message += "=====================================\n"
    log_info(f"{now.strftime('%Y-%m-%d')} 开始签到")
    log_info("=====================================")
    success_users = []  # 记录签到成功的用户
    error_users = []    # 记录签到过程中发生错误的用户

    for user in users:
        if user["is_enable"] != True:
            log_info(f"{user['name']} 已禁用，跳过签到")
            log_info("=====================================")
            server_message += f"{user['name']} 已禁用，跳过签到\n"
            continue

        name = user['name']
        wwroleId = user['wwroleId']
        eeeroleId = user['eeeroleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode = user['devCode']

        log_info(f"{name} 开始签到")
        server_message += f" {name} 签到\n"
        try:
            # 实例化游戏签到类
            GameCheck = GameCheckIn(tokenraw)
            # 鸣潮签到
            if wwroleId:
                log_info(f"{name} 开始鸣潮签到")
                server_message += f"{name} 开始鸣潮签到\n"
                ww_msg = GameCheck.sign_in(
                    game_id=3,
                    server_id="76402e5b20be2c39f095a152090afddc",
                    role_id=wwroleId,
                    user_id=userId,
                    month=month
                )
                if "登录已过期" in ww_msg or "用户信息异常" in ww_msg:
                    log_error(f"{name} 用户登录信息已失效，禁用该用户")
                    server_message += f"{name} 用户登录信息已失效，禁用该用户\n"
                    user["is_enable"] = False
                    update_user_status(user)  # 更新该用户状态
                    error_users.append(name)
                    continue
                if "ERROR" in ww_msg:
                    error_users.append(name)
                server_message += f"{ww_msg}\n"

            # 战双签到
            if eeeroleId:
                log_info(f"{name} 开始战双签到")
                server_message += f"{name} 开始战双签到\n"
                ee_msg = GameCheck.sign_in(
                    game_id=2,
                    server_id=1000,
                    role_id=eeeroleId,
                    user_id=userId,
                    month=month
                )
                if "登录已过期" in ee_msg or "用户信息异常" in ee_msg:
                    log_error(f"{name} 用户登录信息已失效，禁用该用户")
                    server_message += f"{name} 用户登录信息已失效，禁用该用户\n"
                    user["is_enable"] = False
                    update_user_status(user)  # 更新该用户状态
                    error_users.append(name)
                    continue
                if "ERROR" in ee_msg:
                    error_users.append(name)
                server_message += f"{ee_msg}\n"

            time.sleep(1)

            # 库街区签到
            krbbs = KuroBBS(tokenraw, devcode, distinct_id)
            kuro_msg = krbbs.sign_in()
            if "登录已过期" in kuro_msg or "用户信息异常" in kuro_msg:
                log_error(f"{name} 用户登录信息已失效，禁用该用户")
                server_message += f"{name} 用户登录信息已失效，禁用该用户\n"
                user["is_enable"] = False
                update_user_status(user)  # 更新该用户状态
                error_users.append(name)
                continue
            if "ERROR" in kuro_msg:
                error_users.append(name)

            server_message += kuro_msg
            server_message += f"{name} 签到结束\n"
            server_message += "=====================================\n"
            log_info(f"{name} 签到结束")
            log_info("=====================================")
            if name not in error_users:
                success_users.append(name)

        except Exception as e:
            log_error(f"{name} 签到过程中发生错误: {e}")
            server_message += f"{name} 签到过程中发生错误: {e}\n"
            error_users.append(name)

    # 总结签到结果
    summary_message = "签到结果总结：\n"
    summary_message += f"签到成功的用户: {', '.join(success_users) if success_users else '无'}\n"
    summary_message += f"签到失败的用户: {', '.join(error_users) if error_users else '无'}\n"
    log_info(summary_message)
    server_message += summary_message

    # 推送签到结果
    if checkpush:
        from push import push
        push(server_message)



if __name__ == "__main__":
    args = parse_arguments()

    # 根据命令行参数设置日志级别
    if args.debug:
        setup_logger(log_level=logging.DEBUG)
    elif args.error:
        setup_logger(log_level=logging.ERROR)
    else:
        setup_logger(log_level=logging.INFO)
    update_config_from_old_version(DATA_PATH)
    sign_in()