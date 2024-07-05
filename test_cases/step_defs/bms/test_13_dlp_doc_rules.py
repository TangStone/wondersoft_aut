# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_13_dlp_doc_rules.py
@IDE: PyCharm
@time: 2024-04-28 13:38
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
from pages.bms.dlp_doc_rules_page import DlpDocRulesPage

scenarios("./bms/dlp_doc_rules.feature")


@when(parsers.parse("输入新增规则信息：\n{dlp_doc_rules_info}"))
def step_input_dlp_doc_rules_info(page: Page, dlp_doc_rules_info):
    DlpDocRulesPage(page).input_dlp_doc_rules_info(json.loads(dlp_doc_rules_info))


@when(parsers.parse("选择规则：{dlp_doc_rule_name}，点击操作：{operate}"))
def step_dlp_doc_rule_operate(page: Page, dlp_doc_rule_name, operate):
    CommonPage(page).click_tr_oper(dlp_doc_rule_name, operate)


@then(parsers.parse("规则详情中的信息为：\n{dlp_doc_rule_expect_info}"))
def step_assert_dlp_doc_rule_info(page: Page, dlp_doc_rule_expect_info):
    DlpDocRulesPage(page).assert_dlp_doc_rule_info(json.loads(dlp_doc_rule_expect_info))


@when(parsers.parse("根据查询条件进行关键字/正则查询：{query_conditions}"))
def step_dlp_doc_rule_search(page: Page, query_conditions):
    DlpDocRulesPage(page).search_dlp_doc_rules(json.loads(query_conditions))


@when(parsers.parse("删除关键字/正则规则：{dlp_doc_rules_name}"))
def step_dlp_doc_rule_remove(page: Page, dlp_doc_rules_name):
    DlpDocRulesPage(page).delete_dlp_doc_rules(dlp_doc_rules_name)