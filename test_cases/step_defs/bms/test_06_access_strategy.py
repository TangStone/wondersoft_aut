# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_06_access-strategy.py
@IDE: PyCharm
@time: 2024-04-23 9:48
@description:
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
# 本地模块导入
from pages.bms.access_strategy import AccessStrategyPage

scenarios("./bms/access_strategy.feature")


@when(parsers.parse("录入限制信息：\n{strategy_info}"))
def step_add_strategy_info(page: Page, strategy_info):
    AccessStrategyPage(page).add_strategy_info(json.loads(strategy_info))


@when(parsers.parse("全局控制：{control}"))
def step_set_global_controls(page: Page, control):
    AccessStrategyPage(page).set_global_controls(control)


@when(parsers.parse("根据查询条件进行限制策略列表查询：\n{query_conditions}"))
def step_search_strategy(page: Page, query_conditions):
    AccessStrategyPage(page).search_strategy(json.loads(query_conditions))


@when(parsers.parse("删除限制：{strategy_range}"))
def step_delete_strategy(page: Page, strategy_range):
    AccessStrategyPage(page).delete_strategy(strategy_range)