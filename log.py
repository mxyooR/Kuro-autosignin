import logging
import os
from datetime import datetime

# 使用当前工作目录并设置日志目录和文件路径
base_dir = os.getcwd()
log_dir = os.path.join(base_dir, "log")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

def setup_logger(log_level=logging.INFO):
    """设置自定义日志记录器"""
    logger = logging.getLogger("custom_logger")
    logger.setLevel(log_level)  # 设置日志级别

    # 检查日志记录器是否已经有处理程序，避免重复记录
    if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 文件处理程序，使用 UTF-8 编码写入文件
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 控制台处理程序
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        print(f"日志记录器已设置，日志文件: {log_path}")

def log_info(message):
    """记录 INFO 级别日志"""
    logging.getLogger("custom_logger").info(message)

def log_debug(message):
    """记录 DEBUG 级别日志"""
    logging.getLogger("custom_logger").debug(message)

def log_error(message):
    """记录 ERROR 级别日志"""
    logging.getLogger("custom_logger").error(message)



