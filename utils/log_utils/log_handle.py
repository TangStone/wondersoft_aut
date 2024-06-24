# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: loguru_log.py
@IDE: PyCharm
@time: 2024-03-27 16:14
@description: 日志处理
"""
# 标准库导入
import sys
# 第三方库导入
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from config.path_config import LOG_DIR
from utils.base_utils.basefuc import clean_dir



def capture_ui_logs(filename, level="TRACE", filter_type=None):
    """
    日志处理
    :param filename: 日志文件名
    :param filter_type: 日志过滤，如：将日志级别为ERROR的单独记录到一个文件中
    :param level: 日志级别设置
    """
    if level.upper() in ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]:
        level = level
    else:
        ui_logger.error(f"level={level}, 值错误\n"
                     f"level的可选值是：TRACE DEBUG INFO SUCCESS WARNING ERROR  CRITICAL\n"
                     f"将默认level=trace收集日志")
        level = "TRACE"

    clean_dir(LOG_DIR)    # 清空日志目录
    dic = dict(sink=filename,  # 日志保存路径
               rotation='10 MB',
               retention='3 days',
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | From {module}.{function}.{line} : {message}",  # 日志输出格式
               encoding='utf-8',
               level=level,  # 日志级别设置
               enqueue=True
               )
    if filter_type:
        dic["filter"] = lambda x: filter_type in str(x['level']).upper()

    ui_logger.add(**dic)
    # 添加控制台输出
    ui_logger.add(sink=sys.stderr,
               level=level,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | From {module}.{function}.{line} : {message}")

    ui_logger.add(
        "uitest_error.log",
        level="ERROR",
        format=log_format,
        rotation="10 MB",  # 文件大小达到 10MB 时轮换
        retention=20,  # 保留最多 20 个备份
        encoding="utf8",
        filter=lambda record: "UI" in record["extra"]
    )

    ui_logger = ui_logger.bind(UI=True)

def clear_configuration():
    ui_logger.remove()


