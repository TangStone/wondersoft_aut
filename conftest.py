# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: conftest.py
@IDE: PyCharm
@time: 2024-03-27 18:03
@description:
"""
# 标准库导入
from typing import Dict
# 第三方库导入
import allure
import pytest
from loguru import logger
from playwright.sync_api import BrowserType
from _pytest.runner import runtestprotocol
# 本地模块导入
from config.global_vars import GLOBAL_VARS
from config.run_config import RunConfig
from utils.data_utils.data_handle import DataHandle
from utils.report_utils.allure_handle import allure_display

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    重写pytest_playwright夹具browser_context_args，
    :param browser_context_args:
    :return:
    """
    return {
        **browser_context_args,
        # 设置浏览器尺寸（browser_type_launch_args中参数"args": ["--start-maximized"]， 已开启全屏，则此处不需额外设置尺寸）
        # "viewport": RunConfig.window_size,
        "no_viewport": True,  # 与browser_type_launch_args中参数"args": ["--start-maximized"]配合使用。
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    重写pytest_playwright夹具browser_type_launch_args，增加browser自定义启动参数
    :param browser_type_launch_args:
    :return:
    """
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"],  # 浏览器窗口最大化
        "devtools": False,
        # "headless": False,
    }


@pytest.fixture(scope="session")
def context(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict
):
    """
    持久化上下文
    :param browser_type:
    :param browser_type_launch_args:
    :param browser_context_args:
    :return:
    """
    context = browser_type.launch_persistent_context("./data", **{
        **browser_type_launch_args,
        **browser_context_args,
        "locale": "de-DE",
    })

    yield context

    context.close()


@pytest.fixture(scope="session")
def page(context):
    """
    持久化页面
    :param context:
    :return:
    """
    page = context.new_page()
    page.set_default_timeout(RunConfig.timeout)   # 设置全局页面超时时间
    yield page
    page.close()


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    在执行场景之前调用。可以在此钩子中执行任何预处理操作。它接收 request 对象、feature 对象和 scenario 对象作为参数。
    :param request:
    :param feature:
    :param scenario:
    :return:
    """
    allure_par = {'feature_name': getattr(feature, "name", None), 'scenario_name': getattr(scenario, "name", None)}
    allure_display(allure_par)


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """在使用评估参数执行步骤函数之前调用"""

    step_name = getattr(step, "name", None)

    # 对步骤进行处理，将需要替换的关键字${},利用data_handle方法进行替换处理
    setattr(step, "lines", [])
    # new_step_name = data_handle(step_name, GLOBAL_VARS)
    new_step_name = DataHandle().data_handle(step_name, GLOBAL_VARS)
    setattr(step, "name", new_step_name)
    before = "\n" + "=" * 80 \
             + "\n-------------测试步骤--------------------\n" \
               f"BEFORE: {step_name}\n\n" \
               f"AFTER: {new_step_name}\n" \
             + "=" * 80
    logger.debug(before)


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    当步骤函数执行失败时调用。可以在此处理步骤失败的情况。它接收 request 对象、feature 对象、scenario 对象、step 对象、step_func 函数、step_func_args 参数和 exception 异常对象作为参数。
    :param request: 包含有关测试请求的信息。
    :param feature: 当前特性的元数据。
    :param scenario: 当前场景的元数据。
    :param step: 当前步骤的元数据。
    :param step_func: 当前步骤的函数对象。
    :param step_func_args: 当前步骤的函数参数。
    :param exception: 捕获到的异常对象。
    :return:
    """

    feature_name = getattr(feature, 'name', None)
    scenario_name = getattr(scenario, 'name', None)
    step_name = getattr(step, "name", None)

    logger.error("\n" + "=" * 80
                 + "\n-------------测试步骤出错了--------------------\n"
                   f"Feature: {feature_name}\n"
                   f"Scenario: {scenario_name}\n"
                   f"Step: {step_name}\n"
                   f"Exception:   {exception}\n"
                 + "=" * 80)


# # 定义自定义插件类
# class ExceptionCapturePlugin:
#
#     @pytest.hookimpl(tryfirst=True)
#     def pytest_runtest_makereport(self, item, call):
#         # Get the error code based on the exception type
#         if call.excinfo is not None:
#             exc_type = call.excinfo.typename
#             if exc_type == "AssertionError":
#                 error_code = 1001
#             elif exc_type == "TimeoutError":
#                 error_code = 1002
#             else:
#                 error_code = 1000  # Default error code
#             # self.error_codes[item.nodeid] = error_code
#             allure.attach(str(error_code), name="错误类型")
#
#
# # 在pytest配置中注册插件
# def pytest_configure(config):
#     plugin = ExceptionCapturePlugin()
#     config.pluginmanager.register(plugin)
