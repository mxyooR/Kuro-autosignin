"""
主程序入口（重构版）
"""

import os
import logging
import argparse
import configparser
from typing import Optional, Dict
from log import setup_logger, log_info, log_error
from config_manager import ConfigManager
from sign_in_manager import SignInManager


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数
    :return: 解析后的参数
    """
    parser = argparse.ArgumentParser(description="库街区签到任务")
    parser.add_argument("--debug", action="store_true", help="启用 DEBUG 日志级别")
    parser.add_argument("--error", action="store_true", help="启用 ERROR 日志级别")
    return parser.parse_args()


def get_config_dir() -> str:
    """
    获取配置目录路径
    :return: 配置目录路径
    """
    file_path = os.path.dirname(os.path.abspath(__file__))
    return os.environ.get("KuroBBS_config_path", os.path.join(file_path, "config"))


def get_push_config_path() -> str:
    """
    获取推送配置文件路径
    :return: 推送配置文件路径
    """
    push_dir = os.environ.get("KuroBBS_push_path")
    if push_dir:
        return os.path.join(push_dir, "push.ini")
    else:
        return os.path.join(get_config_dir(), "push.ini")


def load_push_config(config_path: str) -> Optional[Dict]:
    """
    加载推送配置
    :param config_path: 配置文件路径
    :return: 推送配置字典或None
    """
    if not os.path.exists(config_path):
        log_error(f"推送配置文件不存在: {config_path}")
        return None

    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")

        if "setting" not in config:
            log_error("推送配置文件中缺少 [setting] 部分")
            return None

        log_info("成功加载推送配置")
        return {
            "enable": config.getboolean("setting", "enable", fallback=False),
            "push_level": config.getint("setting", "push_level", fallback=1),
            "push_server": config.get("setting", "push_server", fallback=""),
        }
    except Exception as e:
        log_error(f"加载推送配置失败: {e}")
        return None


def send_push_notification(messages: list, push_config: Dict):
    """
    发送推送通知
    :param messages: 消息列表
    :param push_config: 推送配置
    """
    try:
        from push import push

        push_level = push_config.get("push_level", 1)

        if push_level == 1:
            # 只推送总结
            push(messages[-1])
        elif push_level == 2:
            # 推送所有消息的合集
            push("\n".join(messages))
        elif push_level == 3:
            # 分别推送每条消息
            for msg in messages:
                push(msg)
        else:
            log_error(f"未知的推送服务级别: {push_level}")

    except Exception as e:
        log_error(f"推送通知失败: {e}")


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()

    # 设置日志级别
    if args.debug:
        setup_logger(log_level=logging.DEBUG)
    elif args.error:
        setup_logger(log_level=logging.ERROR)
    else:
        setup_logger(log_level=logging.INFO)

    log_info("=" * 50)
    log_info("库街区自动签到程序启动")
    log_info("=" * 50)

    try:
        # 初始化配置管理器
        config_dir = get_config_dir()
        config_manager = ConfigManager(config_dir)

        # 初始化签到管理器
        sign_in_manager = SignInManager(config_manager)

        # 执行签到
        # summary, messages = sign_in_manager.run_all()
        _, messages = sign_in_manager.run_all()

        # 加载推送配置
        push_config_path = get_push_config_path()
        push_config = load_push_config(push_config_path)

        # 发送推送通知
        if push_config and push_config.get("enable"):
            log_info("推送服务已启用")
            send_push_notification(messages, push_config)
        else:
            log_info("推送服务未启用")

        log_info("=" * 50)
        log_info("签到任务执行完成")
        log_info("=" * 50)

    except Exception as e:
        log_error(f"程序执行出错: {e}")
        raise


if __name__ == "__main__":
    main()
