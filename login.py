import requests
import uuid

"""
在https://www.kurobbs.com/mc/home/获取你的登录验证码
"""
def get_token():
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

if __name__ == "__main__":
    # 用户信息
    devcode = uuid.uuid4().hex
    distinct_id = uuid.uuid4().hex
    mobile = input('请输入你的手机号：')
    code = input('请输入你的验证码：')
    
    get_token()