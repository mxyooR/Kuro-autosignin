import uuid
import requests
from loguru import logger

from utils import geetestUtils


# send SMS Code
def sendSMSCode(phoneNumber: str, deviceCode: str, seccode):
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
    logger.debug(f"Get seccode ==> {seccode}")
    url = "https://api.kurobbs.com/user/getSmsCode"
    data = {"mobile": phoneNumber, "geeTestData": seccode}
    response = requests.post(url, headers=headers, data=data)
    return response.json()


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
    web_captcha = "ec4aa4174277d822d73f2442a165a2cd"
    android_captcha = "3f7e2d848ce0cb7e7d019d621e556ce2"
    deviceId = "9DE7B0405471B76E018AA599A3A7D9676DCB9D66"
    geetest = geetestUtils.GeeTest(android_captcha)
    seccode = geetest.run()
    if seccode is not None:
        phoneNumber = input("Enter your mobile number: ")
        status = sendSMSCode(
            phoneNumber=phoneNumber, deviceCode=deviceId, seccode=seccode
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
        random_uuid = uuid.uuid4()
        meta = {
            "token": token,
            "userId": userId,
            "roleId": dataResponse["roleId"],
            "roleName": dataResponse["roleName"],
            "serverId": dataResponse["serverId"],
            "deviceCode": random_uuid,
            "distinctId": uuid.uuid4(),
        }
        logger.info(f"Get login Info ==> \n{meta}")
