# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_10_log_backup.py
@IDE: PyCharm
@time: 2024-04-25 13:13
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
from pages.bms.log_backup import LogBackupPage

scenarios("./bms/log_backup.feature")


@given(parsers.parse("选择日志类型：{business_type}，点击操作：{operate}"))
@when(parsers.parse("选择日志类型：{business_type}，点击操作：{operate}"))
def step_logback_operate(page: Page, business_type, operate):
    CommonPage(page).click_tr_oper(business_type, operate)


@when(parsers.parse("编辑备份任务：{business_type}\n{business_info}"))
def step_update_business(page: Page, business_type, business_info):
    LogBackupPage(page).update_business(business_type, json.loads(business_info))
