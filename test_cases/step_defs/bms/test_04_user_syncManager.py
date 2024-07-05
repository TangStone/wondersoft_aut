# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_04_user_syncManager.py
@IDE: PyCharm
@time: 2024-04-15 14:14
@description:  用户推送模块测试用例
"""
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.user_syncManager import UseSyncManagerPage
from pages.common_page import CommonPage

scenarios("./bms/user_syncManage.feature")


@given(parsers.parse("选择系统名称：{system_name}，点击操作：{operate}"))
def step_system_operate(page, system_name, operate):
    CommonPage(page).click_tr_oper(system_name, operate)
