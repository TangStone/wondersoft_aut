# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: conftest.py
@IDE: PyCharm
@time: 2024-03-27 18:09
@description:
"""
import json

# 第三方库导入
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page
import pytest
from loguru import logger
# 本地模块导入
from config.global_vars import GLOBAL_VARS
from pages.common_page import CommonPage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def host():
    """
    获取host
    :return:
    """
    logger.info("获取host:{}".format(GLOBAL_VARS.get("host")))
    return GLOBAL_VARS.get("host")


@given(parsers.parse("进入地址：{path}"))
def step_open_url(page: Page, host, path: str) -> None:
    # 拼接完整的URL
    full_url = host + path
    # 打开网站
    CommonPage(page).open_site(full_url)


@then(parsers.parse("进入页面：{page_name}"))
def step_assert_enter_page(page: Page, page_name):
    pass


@when(parsers.parse("输入用户名：{username}，密码：{password}，点击【立即登录】按钮"))
def step_input_username_password_and_login(page: Page, username, password) -> None:
    LoginPage(page).login(username, password)


@then(parsers.parse("弹出提示框，显示提示信息：{message}"))
def step_assert_message(page: Page, message) -> None:
    CommonPage(page).assert_prompt_information(message)


@given(parsers.parse("进入模块：{module}"))
@when(parsers.parse("进入模块：{module}"))
def step_click_module(page: Page, module: str) -> None:
    CommonPage(page).click_menu(module)


@when(parsers.parse("进入二级菜单：{sec_men} 下的三级菜单：{thi_men}"))
def step_click_thi_men(page: Page, sec_men: str, thi_men: str) -> None:
    CommonPage(page).click_thi_menu(sec_men, thi_men)


@given(parsers.parse("切换到标签页：{tab}"))
def step_switch_tab(page: Page, tab: str) -> None:
    CommonPage(page).switch_tab(tab)


@when(parsers.parse("如果跳转到登录页面：{path}, 使用用户名：{username}，密码：{password}重新登录"))
def step_relogin(page: Page, host, path: str, username, password):
    # 拼接完整的URL
    full_url = host + path
    LoginPage(page).relogin(full_url, username, password)


@given(parsers.parse("点击按钮：{button}"))
@when(parsers.parse("点击按钮：{button}"))
def step_click_button(page: Page, button: str) -> None:
    CommonPage(page).click_button(button)


@when(parsers.parse("点击【{page_name}】页面的【{button}】按钮"))
def step_page_button_click(page: Page, page_name: str, button: str):
    CommonPage(page).click_button(button, page_name)


@then(parsers.parse("退出当前账号,跳转到登录页面：{path}"))
@when(parsers.parse("退出当前账号,跳转到登录页面：{path}"))
def step_logout(page: Page, host, path):
    CommonPage(page).logout(host + path)


@when(parsers.parse("输入修改密码信息：\n{pwd_chg_info}"))
def step_input_pwd_chg_info(page: Page, pwd_chg_info):
    CommonPage(page).input_pwd_chg_info(json.loads(pwd_chg_info))


@then(parsers.parse("{para}输入框下显示错误信息：{error_msg}"))
def step_assert_para_error_msg(page: Page, para, error_msg):
    CommonPage(page).assert_para_error_msg(para, error_msg)


@then(parsers.parse("点击{button}按钮，无网络请求"))
def step_assert_click_norequest(page: Page, button):
    CommonPage(page).assert_click_norequest(button)


@then(parsers.parse("弹出对话提示框，显示提示信息：{dialog_msg}"))
def step_assert_dialog_msg(page: Page, dialog_msg):
    CommonPage(page).assert_dialog_msg(dialog_msg)


