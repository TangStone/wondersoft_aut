# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_18_dlp_severity_level.py
@IDE: PyCharm
@time: 2024-04-29 14:44
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
from pages.bms.dlp_severity_level_page import DlpSeverityLevelPage

scenarios("./bms/dlp_severity_level.feature")


@when(parsers.parse("输入新增严重性等级信息：\n{severity_level_info}"))
def step_input_severity_level_info(page: Page, severity_level_info):
    DlpSeverityLevelPage(page).input_severity_level_info(json.loads(severity_level_info))
