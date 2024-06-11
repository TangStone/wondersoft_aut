# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_11_alarm_rules.py
@IDE: PyCharm
@time: 2024-04-26 10:03
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
from pages.bms.alarm_rules_page import AlarmRulesPage

scenarios("./bms/alarm_rules.feature")


@then(parsers.parse("告警任务中包含：\n{expect_alarm_rules_table}"))
def step_assert_alarm_rules(page: Page, expect_alarm_rules_table):
    expect_alarm_rules = parse_str_table(expect_alarm_rules_table)
    AlarmRulesPage(page).assert_alarm_rules(expect_alarm_rules)


@when(parsers.parse("输入新增告警任务信息：\n{alarm_rules_info}"))
def step_input_alarm_rules_info(page: Page, alarm_rules_info):
    AlarmRulesPage(page).input_alarm_rules_info(json.loads(alarm_rules_info))


@when(parsers.parse("根据查询条件进行告警任务列表查询：\n{query_conditions}"))
def step_delete_alarm_rules(page: Page, query_conditions):
    AlarmRulesPage(page).search_alarm_rules(json.loads(query_conditions))


@when(parsers.parse("删除告警任务：{alarm_rule_name}"))
def step_delete_alarm_rule(page: Page, alarm_rule_name):
    AlarmRulesPage(page).delete_alarm_rule(alarm_rule_name)