# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: excute.py
@IDE: PyCharm
@time: 2024-03-25 11:15
@description:
"""
# 标准库导入
import os
import argparse
# 第三方库导入
import pytest, time
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from config import *
from common import basefunc
from common import sendemail
from config.run_config import UI_LOG_LEVEL, RunConfig
from config.path_config import LOG_DIR, ALLURE_RESULTS_DIR, ALLURE_HTML_DIR
from config.env_config import ENV_VARS, BASE_VARS
from config.global_vars import GLOBAL_VARS
from utils.log_utils import log_handle
from utils.report_utils.allure_handle import generate_allure_report


def run(**kwargs):
    """
    运行测试用例
    :param kwargs: 传入的参数
    :return:
    """
    try:
        # 开启日志记录(默认logs目录)
        ui_logger.debug(f"\nrun方法的入参：{kwargs}\n")
        # 获取传入的环境参数
        env_key = kwargs.get("env", "") or None
        ui_logger.info(
            f"------------------------------------{ENV_VARS[env_key]['project_name']} web自动化测试 START------------------------------------")

        marks = kwargs.get("m", "") or None

        # 如果命令行没有传递browser， 默认使用RunConfig.browser的值
        browser = kwargs.get("browser", "") or None
        RunConfig.browser = browser if browser else RunConfig.browser

        # 如果命令行没有传递mode， 默认使用RunConfig.mode的值
        mode = kwargs.get("mode", "") or None
        RunConfig.mode = mode.lower() if mode else RunConfig.mode

        # 设置pytest参数
        arg_list = [f"--maxfail={RunConfig.max_fail}", f"--reruns={RunConfig.rerun}",
                    f"--reruns-delay={RunConfig.reruns_delay}", f'--alluredir={ALLURE_RESULTS_DIR}',
                    '--clean-alluredir']

        # ----------------通过传入参数配置pytest参数start----------------
        # 设置运行模式
        if RunConfig.mode == "headed":
            arg_list.append("--headed")
        # 设置浏览器驱动类型
        if isinstance(RunConfig.browser, list):
            for browser in RunConfig.browser:
                arg_list.append(f"--browser={browser.lower()}")
        if isinstance(RunConfig.browser, str):
            arg_list.append(f"--browser {RunConfig.browser.lower()}")
        # 设置慢速模式
        if int(kwargs.get("slowmo")) > 0:
            arg_list.append(f"--slowmo={kwargs.get('slowmo')}")
        # 设置标记
        if marks:
            arg_list.append(f"-m {marks}")

        ui_logger.debug(f"\npytest运行参数：{arg_list}\n")
        # ----------------通过传入参数配置pytest参数end----------------

        # 添加全局变量
        GLOBAL_VARS.update(ENV_VARS[env_key])
        GLOBAL_VARS.update(BASE_VARS)
        # ui_logger.info(f"全局变量：{GLOBAL_VARS}")

        # 执行用例前置处理操作
        basefunc.pre_process()
        # 执行测试用例
        pytest.main(args=arg_list)
        # 执行用例后置处理操作
        basefunc.post_process()

        # 生成测试报告
        if kwargs.get("report") == "yes":
            generate_allure_report(allure_results=ALLURE_RESULTS_DIR, allure_report=ALLURE_HTML_DIR)

        # 发送邮件
        if basefunc.config_dict["email"]["sendemail"]:
            times = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            sendemail.SendEmail("report_" + times).send_main()

        ui_logger.info(
            f"------------------------------------{ENV_VARS[env_key]['project_name']} web自动化测试 END------------------------------------")
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="框架主入口")
    parser.add_argument("-env", default="test", help="输入运行环境：test、dev、prod等")
    parser.add_argument("-m", help="选择需要运行的用例：python.ini配置的标签")
    parser.add_argument("-browser", nargs='*', help="浏览器驱动类型配置，支持如下类型：chromium, firefox, webkit")
    parser.add_argument("-mode", help="浏览器驱动类型配置，支持如下类型：headless, headed")
    parser.add_argument("-slowmo", default="0", help="慢速模式，单位毫秒")
    parser.add_argument("-report", default="yes",
                        help="是否生成allure html report，支持如下类型：yes, no")
    args = parser.parse_args()
    run(**vars(args))
