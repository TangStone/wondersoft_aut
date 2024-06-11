# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: allure_handle.py
@IDE: PyCharm
@time: 2024-03-27 17:44
@description: allure报告处理
"""
# 标准库导入
import os
# 第三方库导入
import allure
# 本地模块导入
from config.path_config import LIB_DIR


def allure_display(casedata):
    """
    处理allure显示
    :param casedata: 用例信息
    :return:
    """
    # allure.dynamic.epic(casedata['epic'])
    allure.dynamic.feature(casedata['feature_name'])
    # allure.dynamic.story(casedata['story'])
    allure.dynamic.title(casedata['scenario_name'])
    # allure.dynamic.description(casedata['description'])


def generate_allure_report(**kwargs):
    """
    通过allure生成html测试报告
    """
    allure_results_dir = kwargs.get("allure_results")
    allure_report_dir = kwargs.get("allure_report")
    # allure命令
    allure_bin = os.path.join(LIB_DIR, [i for i in os.listdir(LIB_DIR) if i.startswith("allure")][0], "bin")
    allure_path = os.path.join(allure_bin, "allure.bat")
    cmd = f"{allure_path} generate {allure_results_dir} -o {allure_report_dir} --clean"
    os.popen(cmd).read()
