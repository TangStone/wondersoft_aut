# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: user_group.py
@IDE: PyCharm
@time: 2024-03-28 16:21
@description: 用户及机构管理模块测试用例
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
import allure, pytest
from sttable import parse_str_table
# 本地模块导入
from pages.bms.user_group_page import UserGroupPage

scenarios("./bms/user_group.feature")


@given(parsers.parse("在{parent_group_name}下新增组织机构：{group_name}，点击确定"))
def step_click_add_child_node(page: Page, parent_group_name: str, group_name: str):
    UserGroupPage(page).group_add(parent_group_name, group_name)


@then(parsers.parse("在左侧组织机构栏中，展开: {parent_group_name}，存在新增的机构: {group_name}"))
def step_assert_group_name(page: Page, parent_group_name: str, group_name: str):
    UserGroupPage(page).assert_group_add(parent_group_name, group_name)


@then(parsers.parse("鼠标悬浮在机构：{organ}，显示机构全称：{hover_info}"))
def step_assert_hover(page, organ, hover_info):
    UserGroupPage(page).assert_hover(organ, hover_info)


@when(parsers.parse("输入新增用户信息：\n{user_table}"))
def step_input_user_info(page, user_table):
    users = parse_str_table(user_table)
    for user_info in users.rows:
        UserGroupPage(page).input_user_info(user_info)


@when(parsers.parse("输入新增用户注册信息：\n{user_info}"))
def step_input_user_info(page, user_info):
    UserGroupPage(page).input_user_info(json.loads(user_info))


@given(parsers.parse("输入搜索条件：\n{search_condition}"))
def step_input_search_condition(page: Page, search_condition):
    UserGroupPage(page).input_search_condition(json.loads(search_condition))


@then(parsers.parse("用户列表展示条数为：{user_list_totle}，数据量显示为：{data_volume_display}"))
def step_assert_user_list_display(page: Page, user_list_totle, data_volume_display):
    UserGroupPage(page).assert_user_list_display(user_list_totle, data_volume_display)


@when(parsers.parse("根据查询条件进行用户列表查询：\n{query_conditions}"))
def step_search_users(page: Page, query_conditions):
    UserGroupPage(page).search_users(json.loads(query_conditions))


@when(parsers.parse("删除用户组：{organ}"))
def step_delete_group(page: Page, organ):
    UserGroupPage(page).delete_group(organ)