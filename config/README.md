
## push.ini配置教程
##### 参考https://github.com/Womsxd/MihoyoBBSTools
* push_server 可选范围 cqhttp ftqq(sever酱) pushplus telegram dingrobot bark

### Wecom

企业微信

**wechat_id**填写**企业ID**，见:  我的企业 -> 企业设置 -> 企业ID

**agentid**填写**AgentId**，见:  应用管理 -> 自建 -> 「你自己的应用」 -> 复制数字
**secret**填写**Secret**，见:  应用管理 -> 自建 -> 「你自己的应用」->  点<u>查看</u>链接

**touser**填写**接收人**，默认 @all 通知企业内所有人，指定接收人时使用大驼峰拼音，多个可用｜隔开

填写示例

```ini
[setting]
push_server=wecom

[wecom]
#企业微信的corpid
wechat_id=
#企业微信的应用配置
agentid=
secret=
touser=@all
```

### dingrobot

钉钉群机器人

**webhook**填写**Webhook**地址

**secret**填写**安全设置**中**加签**的密钥，此选项为可选项

填写示例

```ini
[setting]
enable=true
push_server=dingrobot

[dingrobot]
webhook=https://oapi.dingtalk.com/robot/send?access_token=XXX
secret=
```

### bark

一款开源的消息推送工具 [Bark](https://github.com/Finb/Bark)

手机安装bark客户端获得托管在api.day.app的Token，也可以自己搭建私有服务端。

**api_url**一般不用改，自己搭建私有服务端的需要改掉

**token**填写**APP**内**URL**中的密钥，此选项必填

> `https://api.day.app/` `token部分` `/Title/NotificationContent`

填写示例

```ini
[setting]
enable=true
push_server=bark

[bark]
api_url=https://api.day.app
token=XXX
```

### Discord

Discord Channel Webhook

**webhook** 填写 Discord webhook 地址

**username** 为可选项；如果填写，则覆盖 Discord webhook 默认昵称。不填写时使用 webhook 后台配置的昵称

**avatar_url** 为可选项；如果填写，则覆盖 Discord webhook 默认头像。不填写时使用 webhook 后台配置的头像

**http_proxy** 为可选项；如需代理推送可填写，例如 `127.0.0.1:1080`

**verify_ssl** 为可选项；默认为 `true`，如需跳过 SSL 校验可设置为 `false`

填写示例

```ini
[setting]
enable=true
push_server=discord

[discord]
webhook=https://discord.com/api/webhooks/your_channel_id_xxxxxx/your_webhook_token_xxxxxx
#username=Kuro-autosignin
#avatar_url=https://web-static.kurobbs.com/resource/prod/assets/main-img-Bp08JrXL.png
#http_proxy=127.0.0.1:1080
verify_ssl=false
```
