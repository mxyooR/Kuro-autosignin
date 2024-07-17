"""
任务名称
name: 库街区签到任务
定时规则
cron: 1 9 * * *
"""
import time
import datetime
import json
from log import log_message
from game_check_in import ww_game_check_in,eee_game_check_in
from bbs_sgin_in import KuroBBS_sign_in
from push import push
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = FILE_PATH + '/config/data.json'

def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")

    # 从JSON文件中读取数据
    with open(DATA_PATH, 'r', encoding="utf-8-sig") as f:
        data = json.load(f)

    distinct_id = data['distinct_id']
    # 从数据中获取用户数据列表
    users = data['users']
    server_message = ""
    for user in users:
        name = user['name']
        wwroleId = user['wwroleId']
        eeeroleId = user['eeeroleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode = user['devCode']
        checkpush = user['push']

        log_message(name+"开始签到")
        # 鸣潮签到
        server_message = server_message+now.strftime("%Y-%m-%d")+" "+name+"签到\n\n"
        if wwroleId != "":
            server_message = server_message+"今天的奖励为："+ww_game_check_in(tokenraw, wwroleId, userId, month)+"\n\n"
        # 战双签到
        if eeeroleId != "":
            server_message = server_message+"今天的奖励为："+eee_game_check_in(tokenraw, eeeroleId, userId, month)+"\n\n"
        time.sleep(1)

        # 库街区签到
        server_message+=KuroBBS_sign_in(tokenraw, devcode,distinct_id)
        server_message+=name+"签到结束"
        log_message(name+"签到结束")
        log_message("=====================================")

    
    if checkpush:
        push(server_message)

if __name__ == "__main__":
    sign_in()