# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_07_user_admin.py
@IDE: PyCharm
@time: 2024-04-23 11:27
@description:
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.user_admin import UserAdminPage
from pages.bms.user_group_page import UserGroupPage


scenarios("./bms/user_admin.feature")


@when(parsers.parse("上传管理员文件：{user_admin_file}"))
def step_upload_role_file(page: Page, user_admin_file):
    UserAdminPage(page).import_user_admin(user_admin_file)


@then(parsers.parse("管理员列表中包含：{expect_user_admin}"))
def step_assert_role_list(page: Page, expect_user_admin):
    UserAdminPage(page).assert_user_admin_list(expect_user_admin)


@when(parsers.parse("根据查询条件进行管理员列表查询：\n{query_conditions}"))
def step_search_user_admin(page: Page, query_conditions):
    UserAdminPage(page).search_user_admin(json.loads(query_conditions))


@when(parsers.parse("删除管理员：{user_admin_name}"))
def step_delete_user_admin(page: Page, user_admin_name):
    UserAdminPage(page).delete_user_admin(user_admin_name)


@when(parsers.parse("删除用户：{username}"))
def step_delete_user(page: Page, username):
    UserGroupPage(page).delete_user(username)