# -*- coding: utf-8 -*-

"""
@author: tanglei
@File: logger_handle.py
@IDE: PyCharm
@time: 2023-06-24 18:53
@description: 日志设置
"""

import os
from config.path_config import LOG_DIR
from loguru import logger
import sys

# 删除默认的 loguru 处理器
logger.remove()

# 定义日志格式
log_format = "{level}[{time:YYYY-MM-DD HH:mm:ss}][{thread}][{file} {module} {function} {line}]：{message}"

# 添加一个日志处理器用于写入一般接口日志文件
logger.add(
    os.path.join(LOG_DIR, "apitest.log"),
    level="DEBUG",
    format=log_format,
    rotation="10 MB",  # 文件大小达到 10MB 时轮换
    retention='3 days',
    encoding="utf8",
    filter=lambda record: "API" in record["extra"]
)

# 添加一个日志处理器用于写入接口错误日志文件
logger.add(
    os.path.join(LOG_DIR, "apitest_error.log"),
    level="ERROR",
    format=log_format,
    rotation="10 MB",  # 文件大小达到 10MB 时轮换
    retention='3 days',
    encoding="utf8",
    filter=lambda record: "API" in record["extra"]
)

# 添加一个日志处理器用于写入一般UI日志文件
logger.add(
    os.path.join(LOG_DIR, "uitest.log"),
    level="INFO",
    format=log_format,
    rotation="10 MB",  # 文件大小达到 10MB 时轮换
    retention='3 days',
    encoding="utf8",
    filter=lambda record: "UI" in record["extra"]
)

# 添加一个日志处理器用于写入UI错误日志文件
logger.add(
    os.path.join(LOG_DIR, "uitest_error.log"),
    level="ERROR",
    format=log_format,
    rotation="10 MB",  # 文件大小达到 10MB 时轮换
    retention='3 days',
    encoding="utf8",
    filter=lambda record: "UI" in record["extra"]
)

# 添加一个日志处理器用于控制台输出
logger.add(
    sink=sys.stderr,
    level="DEBUG",  # 这里将级别设置为 DEBUG
    format=log_format
)

# 使用不同的 logger 记录接口和UI日志
api_logger = logger.bind(API=True)
ui_logger = logger.bind(UI=True)
