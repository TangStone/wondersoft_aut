# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_08_sys_param.py
@IDE: PyCharm
@time: 2024-04-23 17:09
@description:
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.sys_param import SysParamPage
from pages.bms.user_admin import UserAdminPage
from pages.bms.user_group_page import UserGroupPage

scenarios("./bms/sys_param.feature")


@when(parsers.parse("修改系统参数：{para}的值为：{para_value}"))
def step_update_para(page: Page, para, para_value):
    SysParamPage(page).update_para(para, para_value)


@when(parsers.parse("删除用户：{username}"))
def step_delete_user(page: Page, username):
    UserGroupPage(page).delete_user(username)


@when(parsers.parse("删除管理员：{user_admin_name}"))
def step_delete_user_admin(page: Page, user_admin_name):
    UserAdminPage(page).delete_user_admin(user_admin_name)