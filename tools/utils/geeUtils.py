import json
import urllib.parse

import execjs
import requests
import ddddocr
from loguru import logger

from utils import trackUtils

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

with open('./geeTest.js', 'r') as f:
    geeTestText = f.read()

def _convertCallBack(callBackSign:str, context:str):
    return json.loads(context[len(callBackSign) + 1: len(context) - 1])

def geeLoad(callBackSign: str, captcha_id: str):
    url = "https://gcaptcha4.geetest.com/load"
    params = {
        "callback": callBackSign , 
        "captcha_id": captcha_id,
        "client_type": "web",
        "pt": "1",
        "lang": "zho"
    }
    response = requests.get(url, headers=headers, params=params)
    return _convertCallBack(callBackSign=callBackSign, context=response.text)


def geeSlideAnalyse(bgPath:str, slicePath:str):
    # Get the geetest picture
    geeHost = 'https://static.geetest.com/'
    targetUrl = urllib.parse.urljoin(geeHost, slicePath)
    bgUrl = urllib.parse.urljoin(geeHost, bgPath)
    targetBytes = requests.get(url=targetUrl,headers=headers).content
    bgBytes = requests.get(url=bgUrl,headers=headers).content

    # Identify
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    target = det.slide_match(target_bytes=targetBytes,background_bytes=bgBytes,simple_target=True)['target']
    distance = target[0]
    logger.debug(f"Get target ==> {target}")
    sliceTime = trackUtils.GetSlideTrackTime(distance=distance)
    return {"distance": distance, "time":sliceTime}

def geeSecCode(callBackSign:str, captcha_id:str):
    geeLoadData = geeLoad(callBackSign=callBackSign, captcha_id=captcha_id)['data']
    geeDetectInfo = geeSlideAnalyse(bgPath=geeLoadData['bg'], slicePath=geeLoadData['slice'])
    logger.debug(f'Detect GeeTest Slice ==> {geeDetectInfo}')
    lotNumber = geeLoadData['lot_number']
    w = execjs.compile(geeTestText).call("geeTestW",geeDetectInfo['distance'], geeDetectInfo['time'], lotNumber, geeLoadData['pow_detail']['datetime'], captcha_id)
    logger.debug(f'Get W ==> {w}')
    url = "https://gcaptcha4.geetest.com/verify"
    params = {
        "callback": callBackSign,
        "captcha_id": captcha_id,
        "client_type": "web",
        "lot_number": lotNumber,
        "payload": geeLoadData['payload'],
        "process_token": geeLoadData['process_token'],
        "payload_protocol": "1",
        "pt": "1",
        "w":  w
    }
    response =requests.get(url=url, params=params, headers=headers)
    responseJson = _convertCallBack(callBackSign=callBackSign, context=response.text)
    result = responseJson['data']['result']
    if result != "success":
        logger.error("滑块请求失败,请重新尝试")
        return None
    return json.dumps(_convertCallBack(callBackSign=callBackSign, context=response.text)['data']['seccode'])