# -*- coding: utf-8 -*-

"""
@author: tanglei
@File: exceptions.py
@IDE: PyCharm
@time: 2024-06-21 16:18
@description: 异常处理
"""

import traceback

def get_error_info(ex_type, ex_val, ex_stack):
    """
    获取异常信息
    :param ex_type: 异常类型
    :param ex_val: 异常实例
    :param ex_stack: traceback对象
    :return: 异常信息
    """
    error_info = str(ex_type) + '\n' + str(ex_val) + '\n'
    for stack in traceback.extract_tb(ex_stack):
        error_info += str(stack)
    return error_info
