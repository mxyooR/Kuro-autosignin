"""
云函数入口（适配重构版本）
"""
import os
from log import setup_logger, log_info, log_error
import logging
from config_manager import ConfigManager
from sign_in_manager import SignInManager
from main import get_config_dir, get_push_config_path, load_push_config
import push


def handler(event: dict, context: dict):
    """
    云函数处理入口
    :param event: 事件参数
    :param context: 上下文参数
    :return: 执行结果
    """
    try:
        # 设置日志
        setup_logger(log_level=logging.INFO)
        log_info("云函数签到任务启动")
        
        # 初始化配置管理器
        config_dir = get_config_dir()
        config_manager = ConfigManager(config_dir)
        
        # 初始化签到管理器
        sign_in_manager = SignInManager(config_manager)
        
        # 执行签到任务
        summary, messages = sign_in_manager.run_all()
        log_info("签到任务执行完成")
        
        # 根据 push 配置发送推送通知
        push_config_path = get_push_config_path()
        push_settings = load_push_config(push_config_path)
        
        if push_settings and push_settings["enable"]:
            push_level = push_settings["push_level"]
            final_message = ""
            
            if push_level == 1:
                # 只推送总结
                final_message = messages[-1]
            elif push_level == 2:
                # 推送所有消息的合集
                final_message = "\n".join(messages)
            elif push_level == 3:
                # 分条推送，每条分别发送
                for msg in messages:
                    push.push(msg)
                log_info("分条推送完成")
                return {"status": 200, "message": "签到任务完成"}
            else:
                final_message = "\n".join(messages)
            
            if final_message:
                push.push(final_message)
                log_info("推送通知发送成功")
        else:
            log_info("推送服务未启用")
        
        return {"status": 200, "message": "签到任务完成"}
        
    except Exception as e:
        error_msg = f"签到任务执行失败: {e}"
        log_error(error_msg)
        return {"status": 500, "message": str(e)}


if __name__ == "__main__":
    # 测试代码
    event = {}
    context = {}
    result = handler(event, context)
    print(result)
