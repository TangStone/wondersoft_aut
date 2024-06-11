# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_13_data_dict.py
@IDE: PyCharm
@time: 2024-04-28 16:13
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
from pages.bms.data_dict_page import DataDictPage

scenarios("./bms/data_dict.feature")


@when(parsers.parse("输入新增数据字典信息：\n{data_dict_info}"))
def step_input_data_dict_info(page: Page, data_dict_info):
    DataDictPage(page).input_data_dict_info(json.loads(data_dict_info))


@when(parsers.parse("选择数据字典：{data_dict_name}，点击操作：{operate}"))
def step_dlp_doc_rule_operate(page: Page, data_dict_name, operate):
    CommonPage(page).click_tr_oper(data_dict_name, operate)


@then(parsers.parse("数据字典详情中的信息为：\n{data_dict_expect_info}"))
def step_assert_data_dict_info(page: Page, data_dict_expect_info):
    DataDictPage(page).assert_data_dict_info(json.loads(data_dict_expect_info))


@when(parsers.parse("根据查询条件进行数据字典查询：{query_conditions}"))
def step_datadict_search(page: Page, query_conditions):
    DataDictPage(page).search_datadict(json.loads(query_conditions))


@when(parsers.parse("删除数据字典：{datadict_name}"))
def step_datadict_remove(page: Page, datadict_name):
    DataDictPage(page).delete_datadict(datadict_name)