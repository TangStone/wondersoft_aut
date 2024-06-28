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

from common import handleyaml
from common.logger_handle import ui_logger
# 本地模块导入
from pages.common_page import CommonPage
from pages.login_page import LoginPage
from config import *
from common.readcase import ReadCase
from common.runcase import RunCase
@pytest.fixture(scope='session', autouse=True)
def login_init():
    """
    登录获取token值
    :return:
    """
    api_path = API_DIR + '/bms/login/login.yaml'  # 接口用例路径
    api = 'login'  # 接口用例
    api_caseid = 'login_01'  # 接口用例id
    # 获取接口用例数据
    api_casedata = ReadCase().get_api_casedata(api_path, api, api_caseid)
    # 执行接口用例
    RunCase().excute_apicase(api, api_casedata)

@pytest.fixture(scope="session")
def host():
    """
    获取host
    :return:
    """
    ui_logger.info("获取host:{}".format(GLOBAL_VARS.get("host")))
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
    handleyaml.YamlHandle(EXTRACT_DIR).clear_yaml()
    def handle_response(response):
        extract_value = {}
        if '/login' in response.url:  # 根据具体的登录请求 URL 进行判断
            response_body = response.json()
            token = response_body['data']['token']  # 根据响应体结构获取 token
            extract_value['token'] = token
            handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()
    page.on('response', handle_response)

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


@when(parsers.parse("调用接口：{api},接口用例id：{api_caseid},接口用例路径：{api_path}"))
def step_execute_api(api,api_caseid,api_path):
    # 执行接口用例
    api_path = API_DIR + api_path
    RunCase().excute_apicase_by_ui(api_path, api,api_caseid)