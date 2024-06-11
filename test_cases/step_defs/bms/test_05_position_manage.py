# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_04_role.py
@IDE: PyCharm
@time: 2024-04-22 18:21
@description:
"""
import json

# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.position_manage import PositionManagePage

scenarios("./bms/position_manage.feature")


@when(parsers.parse("上传职位文件：{position_file}"))
def step_upload_position_file(page: Page, position_file):
    PositionManagePage(page).import_position(position_file)


@then(parsers.parse("职位列表中包含：{expect_positions}"))
def step_assert_position_list(page: Page, expect_positions):
    PositionManagePage(page).assert_position_list(expect_positions)


@when(parsers.parse("根据查询条件进行职位列表查询：\n{query_conditions}"))
def step_search_positions(page: Page, query_conditions):
    PositionManagePage(page).search_positions(json.loads(query_conditions))


@when(parsers.parse("删除职位：{position_name}"))
def step_delete_position(page: Page, position_name):
    PositionManagePage(page).delete_position(position_name)
