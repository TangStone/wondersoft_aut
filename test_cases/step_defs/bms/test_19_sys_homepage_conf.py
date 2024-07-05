# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_19_sys_homepage_conf.py
@IDE: PyCharm
@time: 2024-04-29 16:25
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
from pages.bms.sys_homepage_conf_page import SysHomePageConfPage

scenarios("./bms/sys_homepage_conf.feature")


@when(parsers.parse("输入新增主页信息：\n{homepage_info}"))
def step_input_homepage_info(page: Page, homepage_info):
    SysHomePageConfPage(page).input_homepage_info(json.loads(homepage_info))


@when(parsers.parse("根据查询条件进行系统首页配置列表查询：\n{query_conditions}"))
def step_search_homepages(page: Page, query_conditions):
    SysHomePageConfPage(page).search_homepages(json.loads(query_conditions))


@when(parsers.parse("删除系统首页配置：{homepages_name}"))
def step_delete_homepage(page: Page, homepages_name):
    SysHomePageConfPage(page).delete_homepage(homepages_name)