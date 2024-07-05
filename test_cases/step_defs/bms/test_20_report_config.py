# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_20_report_config.py
@IDE: PyCharm
@time: 2024-04-30 13:21
@description:
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from sttable import parse_str_table
from loguru import logger
# 本地模块导入
from pages.common_page import CommonPage
from pages.bms.report_config_page import ReportConfigPage

scenarios("./bms/report_config.feature")


@when(parsers.parse("输入新增报告模板信息：\n{report_config_info}"))
def step_input_report_config_info(page: Page, report_config_info):
   ReportConfigPage(page).input_report_config_info(json.loads(report_config_info))
