# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_15_doc_finger.py
@IDE: PyCharm
@time: 2024-04-28 16:56
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
from pages.bms.doc_finger import DocFingerPage

scenarios("./bms/doc_finger.feature")


@when(parsers.parse("输入新增指纹库信息：\n{doc_finger_info}"))
def step_input_doc_finger_info(page: Page, doc_finger_info):
    DocFingerPage(page).input_doc_finger_info(json.loads(doc_finger_info))


@when(parsers.parse("根据查询条件进行文件指纹查询：{query_conditions}"))
def step_doc_finger_search(page: Page, query_conditions):
    DocFingerPage(page).search_doc_finger(json.loads(query_conditions))


@when(parsers.parse("删除文件指纹：{doc_finger_name}"))
def step_doc_finger_remove(page: Page, doc_finger_name):
    DocFingerPage(page).delete_doc_finger(doc_finger_name)
