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
import logging
from game_check_in import ww_game_check_in, eee_game_check_in
from bbs_sgin_in import KuroBBS_sign_in
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
    server_message = ""

    for user in users:
        if not user.get("is_enable", True):
            log_info(f"{user['name']} 已禁用，跳过签到")
            continue

        name = user['name']
        wwroleId = user['wwroleId']
        eeeroleId = user['eeeroleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode = user['devCode']

        log_info(f"{name} 开始签到")
        server_message += f"{now.strftime('%Y-%m-%d')} {name} 签到\n\n"

        # 鸣潮签到
        if wwroleId:
            ww_msg = ww_game_check_in(tokenraw, wwroleId, userId, month)
            if "登录已过期" in ww_msg:
                log_error(f"{name} 鸣潮签到失败，禁用该用户")
                push(f"{name} 库街区用户信息失效，请重新获取token，已禁用该用户")
                user["is_enable"] = False
                update_user_status(user)  # 更新该用户状态
                continue
            server_message += f"鸣潮签到奖励：{ww_msg}\n\n"

        # 战双签到
        if eeeroleId:
            ee_msg = eee_game_check_in(tokenraw, eeeroleId, userId, month)
            if "登录已过期" in ee_msg:
                log_error(f"{name} 战双签到失败，禁用该用户")
                push(f"{name} 库街区用户信息失效，请重新获取token，已禁用该用户")
                user["is_enable"] = False
                update_user_status(user)  # 更新该用户状态
                continue
            server_message += f"战双签到奖励：{ee_msg}\n\n"

        time.sleep(1)

        # 库街区签到
        kuro_msg = KuroBBS_sign_in(tokenraw, devcode, distinct_id)
        if "登录已过期" in kuro_msg:
            log_error(f"{name} 库街区签到失败，禁用该用户")
            push(f"{name} 库街区用户信息失效，请重新获取token，已禁用该用户")
            user["is_enable"] = False
            update_user_status(user)  # 更新该用户状态
            continue
        server_message += kuro_msg + "\n\n"
        server_message += f"{name} 签到结束\n\n"
        server_message += "=====================================\n\n"
        log_info(f"{name} 签到结束")
        log_info("=====================================")

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

    sign_in()