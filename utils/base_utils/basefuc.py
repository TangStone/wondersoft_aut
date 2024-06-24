# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: basefuc.py
@IDE: PyCharm
@time: 2024-03-28 13:49
@description: 基础函数封装
"""
# 标准库导入
import os
# 第三方库导入
from utils.log_utils.logger_handle import api_logger,ui_logger


def eval_data(data):
    """
    执行一个字符串表达式，并返回其表达式的值
    """
    try:
        if hasattr(eval(data), "__call__"):
            return data
        else:
            return eval(data)
    except Exception as e:
        ui_logger.trace(f"{data} --> 该数据不能被eval\n报错：{e}")
        return data


def clean_dir(path):
    """清空目录下所有文件，保留文件夹"""
    for i in os.listdir(path):
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clean_dir(c_path)
        else:
            os.remove(c_path)
    for i in os.listdir(path):
        dir_path = os.path.join(path, i)
        if os.listdir(dir_path):
            clean_dir(path)
        else:
            os.rmdir(dir_path)