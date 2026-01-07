# 参考https://github.com/Womsxd/MihoyoBBSTools


import os
import hmac
import time
import base64
import urllib
import hashlib
from datetime import datetime, timezone
import sys
from configparser import ConfigParser, NoOptionError
from log import (
    log_info,
    # log_debug,
    log_error,
)


FILE_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = os.environ.get("KuroBBS_config_path", os.path.join(FILE_PATH, "config"))
push_dir = os.environ.get("KuroBBS_push_path")
if push_dir:
    INI_PATH = os.path.join(push_dir, "push.ini")
else:
    INI_PATH = os.path.join(CONFIG_DIR, "push.ini")
cfg = ConfigParser()


# 网络部分


def get_openssl_version() -> int:
    """
    获取openssl版本号
    :return: OpenSSL 的版本号。
    """
    try:
        import ssl
    except ImportError:
        log_error("Openssl Lib Error !!")
        sys.exit("Openssl Lib Error !!")
    temp_list = ssl.OPENSSL_VERSION_INFO
    return int(f"{str(temp_list[0])}{str(temp_list[1])}{str(temp_list[2])}")


def get_new_session(**kwargs):
    try:
        # 优先使用httpx，在httpx无法使用的环境下使用requests
        import httpx

        http_client = httpx.Client(
            timeout=20,
            transport=httpx.HTTPTransport(retries=10),
            follow_redirects=True,
            **kwargs,
        )
        # 当openssl版本小于1.0.2的时候直接进行一个空请求让httpx报错
        # import tools

        if get_openssl_version() < 102:
            httpx.get()
    except (TypeError, ModuleNotFoundError) as e:
        import requests
        from requests.adapters import HTTPAdapter

        http_client = requests.Session()
        http_client.mount("http://", HTTPAdapter(max_retries=10))
        http_client.mount("https://", HTTPAdapter(max_retries=10))
        # 对于 requests，从 kwargs 中提取 proxies
        if "proxies" in kwargs:
            http_client.proxies.update(kwargs["proxies"])
    return http_client


def is_module_imported(module_name):
    return module_name in sys.modules


def get_new_session_use_proxy(http_proxy: str):
    try:
        # 优先使用httpx，在httpx无法使用的环境下使用requests
        import httpx

        proxies = {
            "http://": f"http://{http_proxy}",
            "https://": f"http://{http_proxy}",
        }
        http_client = httpx.Client(
            timeout=20,
            transport=httpx.HTTPTransport(retries=10),
            follow_redirects=True,
            proxies=proxies,
        )
        # 当openssl版本小于1.0.2的时候直接进行一个空请求让httpx报错
        if get_openssl_version() < 102:
            httpx.get()
        return http_client
    except (TypeError, ModuleNotFoundError) as e:
        import requests
        from requests.adapters import HTTPAdapter

        http_client = requests.Session()
        http_client.mount("http://", HTTPAdapter(max_retries=10))
        http_client.mount("https://", HTTPAdapter(max_retries=10))
        http_client.proxies = {
            "http": f"http://{http_proxy}",
            "https": f"http://{http_proxy}",
        }
        return http_client


http = get_new_session()


def load_config():
    config_path = INI_PATH
    if os.path.exists(config_path):
        cfg.read(config_path, encoding="utf-8-sig")
        return True
    else:
        log_error(f"当前预期目录为：{config_path}，配置文件不存在，请检查路径")
        return False


# telegram的推送
def telegram(send_title, push_message):
    try:
        http_proxy = cfg.get("telegram", "http_proxy", fallback=None)
        session = get_new_session_use_proxy(http_proxy) if http_proxy else http
        session.post(
            url="https://{}/bot{}/sendMessage".format(
                cfg.get("telegram", "api_url"), cfg.get("telegram", "bot_token")
            ),
            data={
                "chat_id": cfg.get("telegram", "chat_id"),
                "text": send_title + "\r\n" + push_message,
            },
        )
        log_info("Telegram 推送成功")
    except Exception as e:
        log_error(f"Telegram 推送失败: {e}")


# server酱
def ftqq(send_title, push_message):
    try:
        http.post(
            url="https://sctapi.ftqq.com/{}.send".format(
                cfg.get("setting", "push_token")
            ),
            data={"title": send_title, "desp": push_message},
        )
        log_info("Server酱 推送成功")
    except Exception as e:
        log_error(f"Server酱 推送失败: {e}")


# pushplus
def pushplus(send_title, push_message):
    try:
        http.post(
            url="https://www.pushplus.plus/send",
            data={
                "token": cfg.get("setting", "push_token"),
                "title": send_title,
                "content": push_message,
            },
        )
        log_info("Pushplus 推送成功")
    except Exception as e:
        log_error(f"Pushplus 推送失败: {e}")

# pushme
def pushme(send_title, push_message):
    push_keys = cfg.get("pushme", "pushme_keys")
    push_keys = list(map(str.strip, push_keys.split(",")))

    for key in push_keys:
        try:
            http.post(
                url=cfg.get("pushme", "pushme_url"),
                data={
                    "push_key": key,
                    "title": send_title,
                    "content": push_message,
                },
            )
            log_info(f"Pushme 推送成功 (key: {key})")
        except Exception as e:
            log_error(f"Pushme 推送失败 (key: {key}): {e}")


# cq http协议的推送
def cqhttp(send_title, push_message):
    try:
        http.post(
            url=cfg.get("cqhttp", "cqhttp_url"),
            json={
                "user_id": cfg.getint("cqhttp", "cqhttp_qq"),
                "message": send_title + "\r\n" + push_message,
            },
        )
        log_info("CQHTTP 推送成功")
    except Exception as e:
        log_error(f"CQHTTP 推送失败: {e}")


# smtp mail(电子邮件)
# 感谢 @islandwind 提供的随机壁纸api 个人主页：https://space.bilibili.com/7600422
def smtp(send_title, push_message):
    try:
        import smtplib
        from email.mime.text import MIMEText

        IMAGE_API = "https://api.iw233.cn/api.php?sort=random&type=json"

        try:
            image_url = http.get(IMAGE_API).json()["pic"][0]
        except:
            image_url = "unable to get the image"
            log_error("获取随机背景图失败，请检查图片api")
        with open("assets/email_example.html", encoding="utf-8") as f:
            EMAIL_TEMPLATE = f.read()
        message = EMAIL_TEMPLATE.format(
            title=send_title,
            message=push_message.replace("\n", "<br/>"),
            image_url=image_url,
        )
        message = MIMEText(message, "html", "utf-8")
        message["Subject"] = cfg["smtp"]["subject"]
        message["To"] = cfg["smtp"]["toaddr"]
        message["From"] = f"{cfg['smtp']['subject']}<{cfg['smtp']['fromaddr']}>"
        if cfg.getboolean("smtp", "ssl_enable"):
            server = smtplib.SMTP_SSL(
                cfg["smtp"]["mailhost"], cfg.getint("smtp", "port")
            )
        else:
            server = smtplib.SMTP(cfg["smtp"]["mailhost"], cfg.getint("smtp", "port"))
        server.login(cfg["smtp"]["username"], cfg["smtp"]["password"])
        server.sendmail(
            cfg["smtp"]["fromaddr"], cfg["smtp"]["toaddr"], message.as_string()
        )
        server.close()
        log_info("邮件发送成功")
    except Exception as e:
        log_error(f"邮件发送失败: {e}")


# 企业微信 感谢linjie5492@github
def wecom(send_title, push_message):
    try:
        secret = cfg.get("wecom", "secret")
        corpid = cfg.get("wecom", "wechat_id")
        try:
            touser = cfg.get("wecom", "touser")
        except NoOptionError:
            # 没有配置时赋默认值
            touser = "@all"

        push_token = http.post(
            url=f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}",
            data="",
        ).json()["access_token"]
        push_data = {
            "agentid": cfg.get("wecom", "agentid"),
            "msgtype": "text",
            "touser": touser,
            "text": {"content": send_title + "\r\n" + push_message},
            "safe": 0,
        }
        http.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={push_token}",
            json=push_data,
        )
        log_info("企业微信推送成功")
    except Exception as e:
        log_error(f"企业微信推送失败: {e}")


# 企业微信机器人
def wecomrobot(send_title, push_message):
    try:
        rep = http.post(
            url=f'{cfg.get("wecomrobot", "url")}',
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "msgtype": "text",
                "text": {
                    "content": send_title + "\r\n" + push_message,
                    "mentioned_mobile_list": [f'{cfg.get("wecomrobot", "mobile")}'],
                },
            },
        ).json()
        log_info(f"企业微信机器人推送结果：{rep.get('errmsg')}")
    except Exception as e:
        log_error(f"企业微信机器人推送失败: {e}")


# pushdeer
def pushdeer(send_title, push_message):
    try:
        http.get(
            url=f'{cfg.get("pushdeer", "api_url")}/message/push',
            params={
                "pushkey": cfg.get("pushdeer", "token"),
                "text": send_title,
                "desp": str(push_message).replace("\r\n", "\r\n\r\n"),
                "type": "markdown",
            },
        )
        log_info("Pushdeer 推送成功")
    except Exception as e:
        log_error(f"Pushdeer 推送失败: {e}")


# 钉钉群机器人
def dingrobot(send_title, push_message):
    try:
        api_url = cfg.get(
            "dingrobot", "webhook"
        )  # https://oapi.dingtalk.com/robot/send?access_token=XXX
        secret = cfg.get("dingrobot", "secret")  # 安全设置 -> 加签 -> 密钥 -> SEC*
        if secret:
            timestamp = str(round(time.time() * 1000))
            sign_string = f"{timestamp}\n{secret}"
            hmac_code = hmac.new(
                key=secret.encode("utf-8"),
                msg=sign_string.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
            sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
            api_url = f"{api_url}&timestamp={timestamp}&sign={sign}"

        rep = http.post(
            url=api_url,
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "msgtype": "text",
                "text": {"content": send_title + "\r\n" + push_message},
            },
        ).json()
        log_info(f"钉钉群机器人推送结果：{rep.get('errmsg')}")
    except Exception as e:
        log_error(f"钉钉群机器人推送失败: {e}")


# 飞书机器人
def feishubot(send_title, push_message):
    try:
        api_url = cfg.get(
            "feishubot", "webhook"
        )  # https://open.feishu.cn/open-apis/bot/v2/hook/XXX
        rep = http.post(
            url=api_url,
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "msg_type": "text",
                "content": {"text": send_title + "\r\n" + push_message},
            },
        ).json()
        log_info(f"飞书机器人推送结果：{rep.get('msg')}")
    except Exception as e:
        log_error(f"飞书机器人推送失败: {e}")


# Bark
def bark(send_title, push_message):
    try:
        # make send_title and push_message to url encode
        send_title = urllib.parse.quote_plus(send_title)
        push_message = urllib.parse.quote_plus(push_message)
        rep = http.get(
            url=f'{cfg.get("bark", "api_url")}/{cfg.get("bark", "token")}/{send_title}/{push_message}?icon=https://web-static.kurobbs.com/resource/prod/assets/main-img-Bp08JrXL.png'
        ).json()
        log_info(f"Bark 推送结果：{rep.get('message')}")
    except Exception as e:
        log_error(f"Bark 推送失败: {e}")


# gotify
def gotify(send_title, push_message):
    try:
        rep = http.post(
            url=f'{cfg.get("gotify", "api_url")}/message?token={cfg.get("gotify", "token")}',
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "title": send_title,
                "message": push_message,
                "priority": cfg.getint("gotify", "priority"),
            },
        ).json()
        log_info(f"Gotify 推送结果：{rep.get('errmsg')}")
    except Exception as e:
        log_error(f"Gotify 推送失败: {e}")


# ifttt
def ifttt(send_title, push_message):
    try:
        ifttt_event = cfg.get("ifttt", "event")
        ifttt_key = cfg.get("ifttt", "key")
        rep = http.post(
            url=f"https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"value1": send_title, "value2": push_message},
        )
        if "errors" in rep.text:
            log_error(f"IFTTT 推送执行错误：{rep.json()['errors']}")
            return 0
        else:
            log_info("IFTTT 推送完毕......")
        return 1
    except Exception as e:
        log_error(f"IFTTT 推送失败: {e}")
        return 0


# webhook
def webhook(send_title, push_message):
    try:
        rep = http.post(
            url=f'{cfg.get("webhook", "webhook_url")}',
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"title": send_title, "message": push_message},
        ).json()
        log_info(f"Webhook 推送结果：{rep.get('errmsg')}")
    except Exception as e:
        log_error(f"Webhook 推送失败: {e}")


# qmsg
def qmsg(send_title, push_message):
    try:
        rep = http.post(
            url=f'https://qmsg.zendee.cn/send/{cfg.get("qmsg", "key")}',
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"msg": send_title + "\n" + push_message},
        ).json()
        log_info(f"Qmsg 推送结果：{rep['reason']}")
    except Exception as e:
        log_error(f"Qmsg 推送失败: {e}")


def discord(send_title, push_message):
    try:
        import pytz

        http_proxy = cfg.get("discord", "http_proxy", fallback=None)
        session = get_new_session_use_proxy(http_proxy) if http_proxy else http
        verify_ssl = cfg.getboolean("discord", "verify_ssl", fallback=True)
        rep = session.post(
            verify=verify_ssl,
            url=f'{cfg.get("discord", "webhook")}',
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={
                "content": None,
                "embeds": [
                    {
                        "title": send_title,
                        "description": push_message,
                        "color": 1926125,
                        "author": {
                            "name": "Kuro-autosigin",
                            "url": "https://github.com/mxyooR/Kuro-autosignin",
                            "icon_url": "https://web-static.kurobbs.com/resource/prod/assets/main-img-Bp08JrXL.png",
                        },
                        "timestamp": datetime.now(timezone.utc)
                        .astimezone(pytz.timezone("Asia/Shanghai"))
                        .isoformat(),
                    }
                ],
                "username": "Kuro-autosigin",
                "avatar_url": "https://web-static.kurobbs.com/resource/prod/assets/main-img-Bp08JrXL.png",
                "attachments": [],
            },
        )
        if rep.status_code != 204:
            log_error(f"Discord 推送执行错误：{rep.text}")
        else:
            log_info(f"Discord 推送结果：HTTP {rep.status_code} Success")
    except Exception as e:
        log_error(f"Discord 推送失败: {e}")


def wintoast(send_title, push_message):
    try:
        from win11toast import toast

        toast(app_id="Kuro-autosigin", title=send_title, body=push_message, icon="")
        log_info("Windows Toast 推送成功")
    except Exception as e:
        log_error(f"Windows Toast 推送失败: {e}")


def push(push_message):
    if not load_config():
        log_error("加载配置失败，推送终止")
        return 1
    log_info("正在执行推送......")
    func_names = cfg.get("setting", "push_server").lower()
    for func_name in func_names.split(","):
        func = globals().get(func_name)
        if not func:
            log_error(
                "推送服务名称错误：请检查config/push.ini -> [setting] -> push_server"
            )
            continue
        log_info(f"推送所用的服务为: {func_name}")
        try:
            func("库街区签到", push_message)
        except Exception as r:
            log_error(f"推送执行错误：{str(r)}")
            return 1
        log_info(f"{func_name} - 推送完毕......")
    return 0

if __name__ == "__main__":
    push(f"推送验证{int(time.time())}")

