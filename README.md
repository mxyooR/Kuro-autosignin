# Kuro-AutoSignin

自动化每日任务，轻松管理库街区论坛与游戏签到

## 使用说明

1. **替换个人信息**：请通过抓库街区的包替换脚本中的 `token`、`devcode`、 `roleId`、 `userId`和`distinct_id`。
2. **获取 Token**：使用 `tools.py` 来获取你的 `token`(此方法用于不想折腾安卓抓包并且客户端不能再次登录，库街区的token如果新设备登陆了会刷新)；或者直接抓包
3. **已对接server酱**:在 data.json中的serverKey 字段中填入Server酱 Key，激活即时通知服务。
4. **云函数支持**:入口为index.handler

## 环境依赖

- NodeJS
  - 国内:<https://nodejs.cn/download/>
  - 官网:[Node.js — Download Node.js® (nodejs.org)](https://nodejs.org/en/download/package-manager)
- Python环境
  - `pip install -r ./requirements.txt`

若使用 `pip install -r ./requirements.txt`安装失败，则按以下顺序进行单独安装依赖

1. `pip install ddddocr`
2. `pip install numpy==1.26.2`请勿使用numpy2，会报错
3. `pip install PyExecJS`
4. `pip install loguru`
5. `pip install requests`
