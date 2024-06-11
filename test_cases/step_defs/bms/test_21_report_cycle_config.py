# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_21_report_cycle_config.py
@IDE: PyCharm
@time: 2024-04-30 13:48
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
from pages.bms.report_cycle_config_page import ReportCycleConfigPage
from pages.bms.report_config_page import ReportConfigPage


scenarios("./bms/report_cycle_config.feature")


@when(parsers.parse("输入新增报告信息：\n{report_cycle_config_info}"))
def step_input_report_cycle_config_info(page: Page, report_cycle_config_info):
    ReportCycleConfigPage(page).input_report_cycle_config_info(json.loads(report_cycle_config_info))


@when(parsers.parse("新增报告：\n{report_info}"))
def step_add_report(page: Page, report_info):
    ReportCycleConfigPage(page).add_report(json.loads(report_info))


@when(parsers.parse("根据查询条件进行报告查询：\n{query_conditions}"))
def step_search_report_cycle_config(page: Page, query_conditions):
    ReportCycleConfigPage(page).search_report(json.loads(query_conditions))


@when(parsers.parse("删除报告：{report_name}"))
def step_delete_report(page: Page, report_name):
    ReportCycleConfigPage(page).delete_report(report_name)


@when(parsers.parse("删除模板：{report_config_name}"))
def step_delete_report_config(page: Page, report_config_name):
    ReportConfigPage(page).delete_report_config(report_config_name)