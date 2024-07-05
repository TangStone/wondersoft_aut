# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_09_sys_email.py
@IDE: PyCharm
@time: 2024-04-25 9:49
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
from pages.bms.sys_email import SysEmailPage

scenarios("./bms/sys_email.feature")


@when(parsers.parse("输入系统邮箱配置信息：\n{email_info}"))
def step_input_email_info(page: Page, email_info):
    SysEmailPage(page).input_email_info(json.loads(email_info))


@when(parsers.parse("依次点击提交按钮，弹出提示框，显示提示信息：{pro_msg}\n{email_para_table}"))
def step_assert_email_info_submit(page: Page, pro_msg, email_para_table):
    params = parse_str_table(email_para_table)
    for row in params.rows:
        SysEmailPage(page).assert_email_info_submit(row["邮箱配置参数"], pro_msg)
