import time

import requests
from loguru import logger

from utils import geeUtils


def getCurrentStampMs():
    return round(time.time() * 1000)


# send SMS Code


def sendSMSCode(phoneNumber: str, deviceCode: str, captcha_id: str):
    headers = {
        "Host": "api.kurobbs.com",
        "osversion": "Android",
        "devcode": deviceCode,
        "countrycode": "CN",
        "model": "MIX 2",
        "source": "android",
        "lang": "zh-Hans",
        "version": "2.2.0",
        "versioncode": "2200",
        "channelid": "4",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "okhttp/3.11.0",
    }
    callBackSign = f"geetest_{getCurrentStampMs()}"
    seccode = geeUtils.geeSecCode(callBackSign=callBackSign, captcha_id=captcha_id)
    logger.debug(f"Get seccode ==> {seccode}")
    url = "https://api.kurobbs.com/user/getSmsCode"
    data = {"mobile": phoneNumber, "geeTestData": seccode}
    response = requests.post(url, headers=headers, data=data)
    return response.json()


# Step 3: Perform login with the SMS code


def sdkLogin(phoneNumber: str, smsCode: str, deviceCode: str):
    headers = {
        "Host": "api.kurobbs.com",
        "osversion": "Android",
        "devcode": deviceCode,
        "countrycode": "CN",
        "model": "MIX 2",
        "source": "android",
        "lang": "zh-Hans",
        "version": "2.2.0",
        "versioncode": "2200",
        "channelid": "4",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "okhttp/3.11.0",
    }
    url = "https://api.kurobbs.com/user/sdkLogin"
    data = {
        "code": smsCode,
        "devCode": deviceCode,
        "gameList": "",
        "mobile": phoneNumber,
    }
    response = requests.post(url=url, data=data, headers=headers)
    jsonResult = response.json()
    if jsonResult["code"] != 200:
        logger.error(jsonResult["msg"])
        return False
    return jsonResult["data"]


def getData(token: str, deviceCode: str, refresh: bool = False):
    headers = {
        "Host": "api.kurobbs.com",
        "devcode": deviceCode,
        "source": "android",
        "version": "2.2.0",
        "versioncode": "2200",
        "token": token,
        "osversion": "Android",
        "countrycode": "CN",
        "model": "MIX 2",
        "lang": "zh-Hans",
        "channelid": "4",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "okhttp/3.11.0",
    }
    cookies = {"user_token": token}
    if refresh:
        url = "https://api.kurobbs.com/gamer/widget/game3/refresh"
    else:
        url = "https://api.kurobbs.com/gamer/widget/game3/getData"
    data = {"type": "1", "sizeType": "2"}
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    jsonResult = response.json()
    if jsonResult["code"] != 200:
        return logger.error(jsonResult["msg"])
    return jsonResult["data"]


if __name__ == "__main__":
    # Geetest Id of wuthering waves (android)
    captcha_id = "3f7e2d848ce0cb7e7d019d621e556ce2"
    deviceId = "9DE7B0405471B76E018AA599A3A7D9676DCB9D66"
    phoneNumber = input("Enter your mobile number: ")
    status = sendSMSCode(
        phoneNumber=phoneNumber, deviceCode=deviceId, captcha_id=captcha_id
    )
    logger.info(status["msg"])
    smsCode = input("Enter the SMS code: ")
    loginResponse = sdkLogin(
        phoneNumber=phoneNumber, smsCode=smsCode, deviceCode=deviceId
    )
    logger.debug(f"Login Response ==> \n{loginResponse}")
    token = loginResponse["token"]
    userId = loginResponse["userId"]
    dataResponse = getData(token=token, deviceCode=deviceId)
    meta = {
        "token": token,
        "userId": userId,
        "roleId": dataResponse["roleId"],
        "roleName": dataResponse["roleName"],
        "serverId": dataResponse["serverId"],
    }
    logger.info(f"Get login Info ==> \n{meta}")
