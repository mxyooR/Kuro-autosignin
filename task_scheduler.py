import os
import time
import datetime
from log import setup_logger, log_info
import logging

from crontab import CronTab

setup_logger(log_level=logging.INFO)
time_format = "%Y-%m-%d %H:%M:%S"

def main():
    log_info("DOCKER定时模式已启用")
    env = os.environ
    cron_signin = env["CRON_SIGNIN"]
    cron = CronTab(cron_signin, loop=True, random_seconds=True)

    def next_run_time():
        nt = datetime.datetime.now().strftime(time_format)
        delayt = cron.next(default_utc=False)
        nextrun = datetime.datetime.now() + datetime.timedelta(seconds=delayt)
        nextruntime = nextrun.strftime(time_format)
        log_info(f"当前时间: {nt}")
        log_info(f"下次运行时间: {nextruntime}")

    def sign():
        log_info("开始签到")
        os.system("python ./main.py")

    sign()
    next_run_time()
    while True:
        ct = cron.next(default_utc=False)
        time.sleep(ct)
        sign()
        next_run_time()


if __name__ == '__main__':
    main()