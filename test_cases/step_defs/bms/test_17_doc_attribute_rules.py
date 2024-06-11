# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_17_doc_attribute_rules.py
@IDE: PyCharm
@time: 2024-04-28 18:24
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
from pages.bms.doc_attribute_rules_page import DocAttributeRulesPage

scenarios("./bms/doc_attribute_rules.feature")


@when(parsers.parse("输入新增属性规则信息：\n{attribute_rule_info}"))
def step_input_attribute_rule_info(page: Page, attribute_rule_info):
    DocAttributeRulesPage(page).input_attribute_rule_info(json.loads(attribute_rule_info))


@when(parsers.parse("根据查询条件进行文件属性规则查询：{query_conditions}"))
def step_doc_attribute_rules_search(page: Page, query_conditions):
    DocAttributeRulesPage(page).search_doc_attribute_rules(json.loads(query_conditions))


@when(parsers.parse("删除文件属性规则：{doc_attribute_rules_name}"))
def step_doc_attribute_rules_remove(page: Page, doc_attribute_rules_name):
    DocAttributeRulesPage(page).delete_doc_attribute_rules(doc_attribute_rules_name)