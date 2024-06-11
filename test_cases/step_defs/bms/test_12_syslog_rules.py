# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_12_syslog_rules.py
@IDE: PyCharm
@time: 2024-04-26 17:53
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
from pages.bms.syslog_rules_page import SyslogRulesPage

scenarios("./bms/syslog_rules.feature")


@when(parsers.parse("输入新增syslog规则信息：\n{syslog_rules_info}"))
def step_input_syslog_rules_info(page: Page, syslog_rules_info):
    SyslogRulesPage(page).input_syslog_rules_info(json.loads(syslog_rules_info))


@when(parsers.parse("根据查询条件进行syslog规则列表查询：\n{query_conditions}"))
def step_search_syslog_rules(page: Page, query_conditions):
    SyslogRulesPage(page).search_syslog_rules(json.loads(query_conditions))


@when(parsers.parse("删除syslog规则：{syslog_rule_name}"))
def step_delete_syslog_rule(page: Page, syslog_rule_name):
    SyslogRulesPage(page).delete_syslog_rule(syslog_rule_name)