# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_16_doc_md5.py
@IDE: PyCharm
@time: 2024-04-28 17:35
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
from pages.bms.doc_md5_page import DocMd5Page

scenarios("./bms/doc_md5.feature")


@when(parsers.parse("输入MD5规则导入信息：\n{doc_md5_info}"))
def step_input_doc_md5_info(page: Page, doc_md5_info):
    DocMd5Page(page).input_doc_md5_info(json.loads(doc_md5_info))


@when(parsers.parse("根据查询条件进行文件MD5查询：{query_conditions}"))
def step_docmd5_search(page: Page, query_conditions):
    DocMd5Page(page).search_docmd5(json.loads(query_conditions))


@when(parsers.parse("删除文件MD5：{docmd5_name}"))
def step_docmd5_remove(page: Page, docmd5_name):
    DocMd5Page(page).delete_docmd5(docmd5_name)