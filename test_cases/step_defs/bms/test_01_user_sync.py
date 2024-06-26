# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_03_user_sync.py
@IDE: PyCharm
@time: 2024-04-03 10:34
@description:
"""
# 标准库导入
import json
# 第三方库导入
from pytest_bdd import scenarios, when, parsers
from playwright.sync_api import Page
from sttable import parse_str_table
# 本地模块导入
from pages.bms.user_sync_page import UseSyncPage

scenarios("./bms/user_sync.feature")


@when(parsers.parse("选择数据源类型：{data_source_type}"))
def step_select_data_source_type(page: Page, data_source_type: str) -> None:
    UseSyncPage(page).select_data_source_type(data_source_type)


@when(parsers.parse("AD域参数配置: {domain}"), target_fixture="domain")
def step_ad_domain_config(page, domain):
    # 获取AD域配置参数
    domain = eval(domain)
    # domain_config = eval(domain).get("config")
    UseSyncPage(page).ad_domain_config(domain.get("config"))
    return domain


@when(parsers.parse("AD域参数配置(基础配置+其它配置): {domain}\n{other_config}"), target_fixture="domain")
def step_ad_domain_config(page, domain, other_config):
    # 获取AD域配置参数
    domain = eval(domain)
    domain_config = {**domain.get("config"), **json.loads(other_config)}
    UseSyncPage(page).ad_domain_config(domain_config)
    return domain


@when("AD域数据关联")
def step_ad_domain_relation(page, domain):
    UseSyncPage(page).ad_domain_relation(domain.get("relations"))


@when(parsers.parse("AD域数据关联(基础配置+其它配置):\n{other_relations}"))
def step_ad_domain_relation(page, domain, other_relations):
    domain_relations = {**domain.get("relations"), **json.loads(other_relations)}
    UseSyncPage(page).ad_domain_relation(domain_relations)


@when(parsers.parse("设置同步配置参数：\n{sync_config}"))
def step_sync_config(page, sync_config):
    sync_config_params = parse_str_table(sync_config)
    for sync_config_param in sync_config_params.rows:
        UseSyncPage(page).set_sync_config(sync_config_param)


@when(parsers.parse("选择同步配置名称：{sync_name}"))
def step_check_sync_name(page, sync_name):
    UseSyncPage(page).check_sync_name(sync_name)


@when(parsers.parse("根据查询条件进行查询：\n{query_conditions}"))
def step_search_datasource(page: Page, query_conditions):
    UseSyncPage(page).search_datasource(json.loads(query_conditions))


@when(parsers.parse("删除同步配置：{datasource_name}"))
@when(parsers.parse("删除数据源配置：{datasource_name}"))
def step_remove_datasource(page: Page, datasource_name):
    UseSyncPage(page).delete_datasource(datasource_name)

