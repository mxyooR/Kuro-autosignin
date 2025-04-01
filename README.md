# Kuro-AutoSignin

自动化每日任务，轻松管理库街区论坛与游戏签到 

## 注意

仅供学习交流使用，请勿用于非法用途

## 使用说明

1. **替换个人信息**：请通过抓库街区的包替换`config/data.json`脚本中的 `token`、`devcode`、 `wwroleId`、`eeeroleId`、 `userId` 和 `distinct_id`。`wwroleId`、`eeeroleId`如只需要签到一个则另一个空着。
2. **获取 Token**：使用 `sms_send.py` 来获取你的 `token`（此方法用于不想折腾安卓抓包并且客户端不能再次登录，库街区的 token 如果新设备登陆了会刷新）；或者直接抓包。
3. **签到信息推送**：如需要开启请在`config/data.json`中设置`"push":1`,不开启为`0`,在 `/config/push.ini` 中填写信息，具体参照[配置文档](/config/README.md)，感谢https://github.com/Womsxd/MihoyoBBSTools 项目提供推送方式
4. **云函数支持**：入口为 `index.handler`。
5. **serverid设置**：战双serverid如果不对请自行抓包更正。

## 环境依赖

- NodeJS
  - 国内: <https://nodejs.cn/download/>
  - 官网: [Node.js — Download Node.js® (nodejs.org)](https://nodejs.org/en/download/package-manager)
- Python 环境
  - `pip install -r ./requirements.txt`

## 短信登录工具说明

现已将极验验证的接口转为图标点选，并重新编写参数加密部分。目前图片识别使用网上的模型以及`ddddocr`，成功率有点感人但凑活着用吧。若不通过可多尝试几次

**图片处理部分代码来自**[Bump-mann/simple_ocr: 一个简单的识别验证码的代码](https://github.com/Bump-mann/simple_ocr)

## 青龙面板运行方法

1. **拉取项目到本地**：将项目克隆到本地目录。
2. **获取个人信息**：捕获库街区的包，获取并填写好 `data.json` 中的 `token`、`devcode`、`wwroleId`、`eeeroleId`、`userId` 、`is_enable`和 `distinct_id`。
3. **创建订阅**：在青龙面板中创建新的订阅任务。
   - 名称：库街区签到
   - 类型：公开仓库
   - 链接：<https://github.com/mxyooR/Kuro-autosignin.git>
   - 定时类型：crontab
   - 定时规则：1 9 * * *
   - 白名单：main.py
   - 依赖文件：log|game_check_in|bbs_sgin_in|push|tools

4. **导入 `data.json`**：在青龙面板的脚本管理中，进入 `mxyooR_Kuro-autiosignin/config` 文件目录下，导入并替换修改好的 `data.json` 文件。
5. **添加依赖**：在青龙面板的依赖管理里面安装requests依赖。
6. **推送选项**：青龙面板可以使用青龙自带的推送，不必用本脚本自带的推送，如要使用，请填写push.ini放入/config目录下。

这样设置完成后，青龙面板将会每天按时自动运行库街区的签到任务。
