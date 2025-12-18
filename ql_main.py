"""
青龙面板入口（适配重构版本）
"""

import os
import logging
from log import setup_logger, log_info, log_error
from config_manager import ConfigManager
from sign_in_manager import SignInManager
import notify


def setup_ql_logger():
    """设置青龙环境下的日志"""
    log_level = os.environ.get("KuroBBS_log_level", "INFO")
    if log_level == "DEBUG":
        setup_logger(log_level=logging.DEBUG)
    elif log_level == "ERROR":
        setup_logger(log_level=logging.ERROR)
    else:
        setup_logger(log_level=logging.INFO)


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


def load_push_config(config_path: str):
    """
    加载推送配置
    :param config_path: 配置文件路径
    :return: 推送配置字典或None
    """
    if not os.path.exists(config_path):
        log_error(f"推送配置文件不存在: {config_path}")
        return None

    try:
        import configparser

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


def ql_push(message: str, use_project_push: bool):
    """
    青龙面板推送消息
    :param message: 推送消息
    :param use_project_push: 是否使用项目自带推送
    """
    if use_project_push:
        try:
            from push import push

            push(message)
            log_info("项目推送发送成功")
        except Exception as e:
            log_error(f"项目推送发送失败: {e}")
    else:
        try:
            notify.send("库街区签到", message)
            log_info("青龙推送发送成功")
        except Exception as e:
            log_error(f"青龙推送发送失败: {e}")


def main():
    """主函数"""
    # 设置日志
    setup_ql_logger()
    log_info("=" * 50)
    log_info("库街区签到 - 青龙面板模式启动")
    log_info("=" * 50)

    # 检查是否设置了配置文件前缀
    config_prefix = os.environ.get("KuroBBS_config_prefix", "")
    if config_prefix:
        log_info(f"配置文件将使用前缀: {config_prefix}")

    try:
        # 初始化配置管理器
        config_dir = get_config_dir()
        config_manager = ConfigManager(config_dir)

        # 初始化签到管理器
        sign_in_manager = SignInManager(config_manager)

        # 执行签到
        # summary, messages = sign_in_manager.run_all()
        _, messages = sign_in_manager.run_all()

        # 检查推送方式
        # KuroBBS_push_project: 0/1, 是否使用项目自带推送(1=是)
        use_project_push = os.environ.get("KuroBBS_push_project", "0") == "1"
        if use_project_push:
            log_info("使用项目自带推送方式")
        else:
            log_info("使用青龙自带推送方式")

        # 加载推送配置并发送
        push_config_path = get_push_config_path()
        push_settings = load_push_config(push_config_path)

        if push_settings and push_settings["enable"]:
            push_level = push_settings["push_level"]
            if push_level == 1:
                ql_push(messages[-1], use_project_push)
            elif push_level == 2:
                ql_push("\n".join(messages), use_project_push)
            elif push_level == 3:
                for msg in messages:
                    ql_push(msg, use_project_push)
            else:
                ql_push(messages[-1], use_project_push)
        else:
            log_info("项目推送未启用或配置不正确")

        log_info("=" * 50)
        log_info("签到任务执行完成")
        log_info("=" * 50)

    except Exception as e:
        log_error(f"程序执行出错: {e}")
        raise


if __name__ == "__main__":
    main()
