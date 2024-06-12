# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: run_config.py
@IDE: PyCharm
@time: 2024-03-27 16:17
@description: 运行配置信息
"""
# ------------------------------------ 基础配置信息 ----------------------------------------------------#
LOG_LEVEL = "DEBUG"  # 可选值：TRACE DEBUG INFO SUCCESS WARNING ERROR  CRITICAL
"""
支持的日志级别：
    TRACE: 最低级别的日志级别，用于详细追踪程序的执行。
    DEBUG: 用于调试和开发过程中打印详细的调试信息。
    INFO: 提供程序执行过程中的关键信息。
    SUCCESS: 用于标记成功或重要的里程碑事件。
    WARNING: 表示潜在的问题或不符合预期的情况，但不会导致程序失败。
    ERROR: 表示错误和异常情况，但程序仍然可以继续运行。
    CRITICAL: 表示严重的错误和异常情况，可能导致程序崩溃或无法正常运行。
"""


# ------------------------------------ pytest相关配置 ----------------------------------------------------#
class RunConfig:
    """
    运行测试配置
    """
    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = ["chromium"]

    # 运行模式（headless, headed）
    mode = "headless"

    # 当达到最大失败数，停止执行
    max_fail = "15"

    # 失败重跑次数
    rerun = 0

    # 失败重跑间隔时间
    reruns_delay = 5

    # 全局超时时间
    timeout = 30000

