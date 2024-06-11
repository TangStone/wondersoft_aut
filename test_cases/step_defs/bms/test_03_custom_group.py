# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: custom_group.py
@IDE: PyCharm
@time: 2024-04-01 14:16
@description:
"""
import json

# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.custom_group_page import CustomGroupPage

scenarios("./bms/custom_group.feature")


@when(parsers.parse("输入用户组名称：{group_name}，备注：{remark}"))
def step_input_group_name(page: Page, group_name, remark):
    CustomGroupPage(page).input_group_name(group_name, remark)


@when(parsers.parse("选择用户：{user}"))
def step_check_user(page: Page, user):
    CustomGroupPage(page).check_user(user)


@when(parsers.parse("根据查询条件进行自定义用户组查询：\n{query_conditions}"))
def step_search_custom_group(page: Page, query_conditions):
    CustomGroupPage(page).search_custom_group(json.loads(query_conditions))


@when(parsers.parse("删除自定义用户组：{custom_group_name}"))
def step_delete_custom_group(page: Page, custom_group_name):
    CustomGroupPage(page).delete_custom_group(custom_group_name)