import requests




# Step 3: Perform login with the SMS code
def login(mobile, sms_code):
    url = "https://api.kurobbs.com/user/sdkLogin"
    headers = {
        "Host": "api.kurobbs.com",
        "distinct_id": "id",
        "version": "2.2.0",
        "channelId": "1",
        "channel": "appstore",
        "Accept": "*/*",
        "devCode": "dc",
        "source": "ios",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "KuroGameBox/48 CFNetwork/1492.0.1 Darwin/23.3.0",
        "lang": "zh-Hans",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "model": "iPhone15,2",
        "osVersion": "17.3"
    }
    data = {
        "code": sms_code,
        "devCode": "dc",
        "mobile": mobile
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


mobile_number = input("Enter your mobile number: ")


sms_code = input("Enter the SMS code: ")

login_response = login(mobile_number, sms_code)
print("Login Response:", login_response)
