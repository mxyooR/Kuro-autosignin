import os
import time
import json
import urllib

import execjs
import requests
from loguru import logger

from utils import pathUtils, pictureUtils

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

with open(os.path.join(pathUtils.STATIC_PATH, "geeTest.js"), "r") as f:
    jsText = f.read()

jsc = execjs.compile(jsText)


def get_w(captcha_id, datetime, lot_number, passtime, userresponse):
    return jsc.call("gen_w", captcha_id, datetime, lot_number, passtime, userresponse)


def getCurrentStampMs():
    return round(time.time() * 1000)


def _convertCallBack(callBackSign: str, context: str):
    return json.loads(context[len(callBackSign) + 1 : len(context) - 1])


def _download(url, name):
    response = requests.get(url=url, headers=headers)
    pngPath = os.path.join(pathUtils.STATIC_PATH, "pictures", f"{name}.png")
    pathUtils.mk_dir(pngPath)
    with open(pngPath, "wb") as f:
        f.write(response.content)


def download_pic(gee_info):
    geeHost = "https://static.geetest.com/"
    target_picture = gee_info["data"]["imgs"]
    target_picture_url = urllib.parse.urljoin(geeHost, target_picture)
    _download(target_picture_url, "target")
    ques_list = gee_info["data"]["ques"]
    for index in range(len(ques_list)):
        ques = ques_list[index]
        que_url = urllib.parse.urljoin(geeHost, ques)
        _download(que_url, f"que_{index}")


class GeeTest(object):
    def __init__(self, captcha_id: str):
        self.captcha_id = captcha_id

    def send_load(self):
        callBackSign = f"geetest_{getCurrentStampMs()}"
        url = "https://gcaptcha4.geetest.com/load"
        params = {
            "callback": callBackSign,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "pt": "1",
            "lang": "zho",
        }
        response = requests.get(url, headers=headers, params=params)
        return _convertCallBack(callBackSign=callBackSign, context=response.text)

    def verify(self, lot_number, payload, process_token, w):
        callbackSign = f"geetest_{getCurrentStampMs()}"
        url = "https://gcaptcha4.geetest.com/verify"
        params = {
            "callback": callbackSign,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "lot_number": lot_number,
            "payload": payload,
            "process_token": process_token,
            "payload_protocol": "1",
            "pt": "1",
            "w": w,
        }
        response = requests.get(url, headers=headers, params=params)
        data = _convertCallBack(callBackSign=callbackSign, context=response.text)
        result = data["data"]["result"]
        if result != "success":
            logger.error("验证码识别未通过,请重试")
            return None
        return json.dumps(data["data"]["seccode"])

    def run(self):
        geeInfo = self.send_load()
        lotNumber = geeInfo["data"]["lot_number"]
        datetime = geeInfo["data"]["pow_detail"]["datetime"]

        payload = geeInfo["data"]["payload"]
        processToekn = geeInfo["data"]["process_token"]
        download_pic(gee_info=geeInfo)
        pictureUtils.process_picture()
        points = pictureUtils.get_points()
        userresponse = [
            [
                int(round(i[0] / 301.8125 * 100 * 100)),
                int(round(i[1] / 201.296875 * 100 * 100)),
            ]
            for i in points
        ]
        passtime = 2098  # 检测不严格,干脆固定了
        w = get_w(self.captcha_id,datetime, lotNumber, passtime, userresponse)
        logger.debug(f"w => {w}")
        return self.verify(
            lot_number=lotNumber, payload=payload, process_token=processToekn, w=w
        )
