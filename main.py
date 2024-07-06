"""
任务名称
name: 库街区签到任务
定时规则
cron: 1 9 * * *
"""
import time
import datetime
import json
import requests
from log import log_message
from game_check_in import game_check_in
from bbs_sgin_in import KuroBBS_sign_in


def sc_send(text, desp, key=''):
    if key == '':
        print("请填写server酱的KEY")
        return
    url = f'https://sctapi.ftqq.com/{key}.send'
    data = {'text': text, 'desp': desp}
    response = requests.post(url, data=data)
    result = response.text
    return result


def sign_in():
    now = datetime.datetime.now()
    month = now.strftime("%m")

    # 从JSON文件中读取数据
    with open('data.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    serverKey = data['serverKey']
    distinct_id = data['distinct_id']
    # 从数据中获取用户数据列表
    users = data['users']

    for user in users:
        server_message = ""
        name = user['name']
        roleId = user['roleId']
        tokenraw = user['tokenraw']
        userId = user['userId']
        devcode = user['devCode']

        log_message(name+"开始签到")
        # 鸣潮签到
        
        server_message = server_message+now.strftime("%Y-%m-%d")+" "+name+"签到\n\n"
        server_message = server_message+"今天的奖励为："+game_check_in(tokenraw, roleId, userId, month)+"\n\n"
        time.sleep(1)

        # 库街区签到
        server_message=server_message+KuroBBS_sign_in(tokenraw, devcode,distinct_id)
        log_message(name+"签到成功")
        # 发送server酱通知
        log_message(sc_send(name+"签到", server_message, key=serverKey))
        log_message("=====================================")


if __name__ == "__main__":
    sign_in()