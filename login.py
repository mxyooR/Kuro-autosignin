import requests

"""
在https://www.kurobbs.com/mc/home/9获取你的登录验证码
"""
devcode = ""
distinct_id = ""
code = "填入你在web端获取的验证码"
mobile = "手机号"

url = 'https://api.kurobbs.com/user/sdkLogin'
headers = {
    'osversion': 'Android',
    'devcode': devcode,
    'distinct_id': distinct_id,
    'countrycode': 'CN',
    'ip': '192.168.1.101',
    'model': '2211133C',
    'source': 'android',
    'lang': 'zh-Hans',
    'version': '1.0.9',
    'versioncode': '1090',
    'content-type': 'application/x-www-form-urlencoded',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/3.10.0',
}

data = {
    'code': code,
    'devCode': devcode,
    'gameList': '',
    'mobile': mobile
}

try:
    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        print(f'fetch error: {response.status_code}, {response.reason}')

    rsp = response.json()

    if rsp.get('code') == 200:
        print(f'api rsp: {rsp}')
    else:
        print(f'api error: {rsp}')

except Exception as error:
    print(f'fetch error: {error}')
