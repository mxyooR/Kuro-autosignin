# Kuro-AutoSignin

自动化每日任务，轻松管理库街区论坛与游戏签到

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

## 使用说明

1. **获取登录信息**：使用 tools.py 来获取 登录信息。
2. **替换个人信息**：替换脚本中的 `token`、`devcode`、 `roleId`和 `userId`
3. **已对接server酱**:在 serverKey 字段中填入Server酱 Key，激活即时通知服务。
