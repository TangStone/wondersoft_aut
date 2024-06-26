# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: exception_handle.py
@IDE: PyCharm
@time: 2024-04-11 17:59
@description: 异常处理
"""
import re
# 标准库导入
import traceback
# 第三方库导入
from common.logger_handle import ui_logger
import allure


class ExceptionHandle:
    """
    异常处理
    """
    # @staticmethod
    # def get_error_info(ex_type, ex_val, ex_stack):
    #     error_info = str(ex_type) + '\n' + str(ex_val) + '\n'
    #     for stack in traceback.extract_tb(ex_stack):
    #         error_info += str(stack)
    #     return error_info

    def handle_exception(self, exception, ex_type=""):
        """
        处理异常信息
        :param ex_type: 异常类型 assert: 在校验时发生的异常
        :param exception: 异常信息
        :return:
        """
        # 处理异常
        exception_type = type(exception).__name__
        if exception_type == "TimeoutError":
            err_msg = f"""元素定位超时"""
        elif exception_type == "AssertionError":
            err_msg = f"""校验失败"""
        else:
            if re.match("Error: strict mode violation:.*resolved to.*elements:", str(exception)):
                err_msg = f"""定位到多个元素"""
            else:
                err_msg = f"""未知异常"""
        trac = traceback.format_exc()
        # 处理allure报告
        attach_body = f"""
{err_msg}：{exception}
详细报错信息如下：
{trac}
"""
        ui_logger.error(trac)
        # 添加异常信息
        if ex_type == 'assert':    #校验时出现的异常
            allure.attach(name="测试用例校验失败：", body=attach_body)
            assert False
        else:
            allure.attach(name="测试用例运行失败：", body=attach_body)
            raise
