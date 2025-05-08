import os
import logging
from log import setup_logger, log_info, log_error
from main import SignInManager, load_push_config
import notify



def setup_ql_logger():
    """设置青龙环境下的日志"""
    # 设置日志级别
    log_level = os.environ.get('KuroBBS_log_level', 'INFO')
    if (log_level == 'DEBUG'):
        setup_logger(log_level=logging.DEBUG)
    elif (log_level == 'ERROR'):
        setup_logger(log_level=logging.ERROR)
    else:
        setup_logger(log_level=logging.INFO)

def ql_push(message):
    """青龙面板推送消息"""
    if use_project_push:
        push(message)
    else:
        try:
            notify.send("库街区签到", message)
            log_info("青龙推送发送成功")
        except Exception as e:
            log_error(f"青龙推送发送失败: {e}")   

if __name__ == "__main__":
    # 设置日志
    setup_ql_logger()
    log_info("库街区签到 - 青龙面板模式启动")

    
    # 创建签到管理器并执行

    #让config去找默认path
    manager = SignInManager()
    messages = manager.run()
    
    # 检查推送方式

    # | KuroBBS_push_project | 0/1 | 是否使用项目自带推送(1=是) |
    use_project_push = os.environ.get('KuroBBS_push_project', '0') == '1'
    if use_project_push:
        log_info("使用默认推送方式，不使用青龙推送")
    else:
        log_info("使用青龙自带推送")
    


    
    # 加载推送配置并发送
    push_settings = load_push_config()
    if push_settings and push_settings["enable"]:
        from push import push
        push_level = push_settings["push_level"]
        if push_level == 1:
            ql_push(messages[-1])
        elif push_level == 2:
            ql_push("\n".join(messages))
        elif push_level == 3:
            for msg in messages:
                ql_push(msg)
        else:
            ql_push(messages[-1])
    else:
        log_info("项目推送未启用或配置不正确")
