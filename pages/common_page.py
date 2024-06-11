# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: common_page.py
@IDE: PyCharm
@time: 2024-03-27 18:44
@description: 公共页面操作封装
"""
# 标准库导入
from typing import Union
import re
# 第三方库导入
import allure
from loguru import logger
from playwright.sync_api import expect
# 本地模块导入
from utils.base_utils.exception_handle import ExceptionHandle
from utils.ui_utils.base_page import BasePage


class CommonPage(BasePage):
    """
    公共页面操作封装
    """

    @allure.step("打开网站：{url}")
    def open_site(self, url):
        """
        打开网站
        :param url:
        :return:
        """
        self.visit(url)

    # ---------------- 页面公共操作 ----------------
    @allure.step("退出当前账号")
    def logout(self, login_url):
        # 获取下拉框id
        dropdown_id = self.page.locator(".avatar-wrapper").get_attribute("aria-controls")
        # 定位到下拉框是否可见
        dropdown_location = self.page.locator("#" + dropdown_id)
        # 若下拉框不可见，点击按钮
        if not dropdown_location.is_visible():
            self.page.locator(".avatar-wrapper > i").click()
        dropdown_location.locator('xpath=/li[text()="退出登录"]').click()
        self.page.wait_for_url(login_url)

    @allure.step("管理员修改密码：{pwd_chg_info}")
    def input_pwd_chg_info(self, pwd_chg_info):
        """
        修改密码
        :param pwd_chg_info: 修改密码参数信息
        :return:
        """
        # 页面参数配置类型
        para_conf_type_dict = {
            "原密码": "input",  # 输入框
            "新密码": "input",
            "确认密码": "input",
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in pwd_chg_info.items():
            if para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value)

    @allure.step("校验--参数:{para}输入框中的错误信息：{error_msg}")
    def assert_para_error_msg(self, para, error_msg):
        """
        输入框输入数据不符合标准时，校验参数的错误提示信息
        :param para: 参数名称
        :param error_msg: 错误提示
        :return:
        """
        # 根据参数名称定位到参数错误提示
        para_error_location = self.page.locator("form div label", has_text=re.compile("^" + para + ".*：$")).locator(
            "..//div[@class='el-form-item__error']")
        expect(para_error_location).to_have_text(error_msg)

    @allure.step("校验--弹出对话提示框，显示提示信息：{dialog_expect_msg}")
    def assert_dialog_msg(self, dialog_expect_msg=""):
        """
        校验是否弹出对话提示框，提示框
        :param dialog_expect_msg: 预期提示信息
        :return:
        """
        logger.info(f"校验是否弹出对话提示框，对话提示框提示信息为：{dialog_expect_msg}，提示信息为空表示不校验提示信息")
        try:
            # 等待提示框出现
            dialog_location = self.wait_for_selector('[role="dialog"][aria-label="提示"]')
            # 校验提示信息
            if dialog_location:
                if dialog_expect_msg:
                    dialog_msg = self.page.locator('[role="dialog"][aria-label="提示"] p').inner_text()
                    assert dialog_msg == dialog_expect_msg
                else:  # 提示框出现
                    assert True
            else:  # 提示框没有出现
                assert False
        except Exception as e:
            ExceptionHandle().handle_exception(e, "assert")

    @allure.step("校验--点击按钮：{button}，无网络请求")
    def assert_click_norequest(self, button):
        """
        点击按钮，校验无网络请求
        :param button:
        :return:
        """
        logger.info(f"校验当前无网络请求")
        try:
            password_request_received = True

            # 监听请求，如果请求url中包含“password”，则设置password_request_received为True
            def on_request(request):
                logger.info(request.url)
                if "password" in request.url:
                    nonlocal password_request_received
                    password_request_received = False
                    logger.info("Password request received. Stopping listening.")

            self.page.on("request", on_request)
            self.click_by_role_text("button", button)
            self.page.wait_for_timeout(3000)
            self.page.remove_listener("request", on_request)
            assert password_request_received
        except Exception as e:
            ExceptionHandle().handle_exception(e, "assert")

    # ---------------- 列表相关操作 ----------------
    @allure.step("选中行：{uniq_iden}， 执行操作：{operate}")
    def click_tr_oper(self, uniq_iden: str, operate: str):
        """
        根据唯一标识选中需要进行操作的行，点击对应的操作按钮执行操作
        :param uniq_iden: 唯一标记，用来获取操作行
        :param operate: 执行的操作
        :return:
        """
        # 点击操作
        self.button_operate_with_line(uniq_iden, operate)

    @allure.step("点击按钮：{button}")
    def click_button(self, button: str, page_name=None) -> None:
        """
        点击按钮
        :param page_name: 页面名称
        :param button: 按钮名称
        """
        location = None
        if page_name:
            location = self.get_label_locator(page_name)
        self.click_by_role_text("button", button, location)
        # logger.info(f"____点击按钮：{button}")
        # self.page.get_by_role("button", name=button).click()

    @allure.step("点击一级菜单：{men}")
    def click_menu(self, men: str) -> None:
        """
        点击一级菜单
        :param men: 一级菜单名称
        """
        logger.info(f"____点击一级模块：{men}")
        # self.page.get_by_text(men).click()
        # self.page.get_by_role("tab", name=men).click()
        self.page.locator(".portal-navbar").get_by_role("tab", name=men).click()

    @allure.step("点击二级菜单：{sec_men}下的三级菜单：{thi_men}")
    def click_thi_menu(self, sec_men: str, thi_men: str) -> None:
        """
        点击二级菜单下的三级菜单
        :param thi_men: 二级菜单名称
        :param sec_men: 三级菜单名称
        """
        logger.info(f"____点击二级菜单：{sec_men}下的三级菜单：{thi_men}")
        # 判断当前页面是否存在二级模块
        if not self.page.get_by_role("menuitem", name=sec_men).locator("i").nth(1).is_visible():
            self.page.locator(".hamburger-container > .iconfont").click()
        # 判断当前页面是否存在三级模块
        if not self.page.get_by_role("link", name=thi_men).is_visible():
            self.page.get_by_role("menuitem", name=sec_men).locator("i").nth(1).click()
        self.page.get_by_role("link", name=thi_men).click()

    @allure.step("切换标签页：{tab}")
    def switch_tab(self, tab: str) -> None:
        """
        切换标签页
        :param tab: 标签页名称
        """
        logger.info(f"____切换标签页：{tab}")
        self.page.get_by_role("tab", name=tab).click()

    @allure.step("____页面路径是 = {url}")
    def have_url(self, url: Union[str]) -> None:
        """
        断言：检查页面是否存在指定的 URL；存在则通过，不存在则失败；
        :param url: 页面标题，接受一个字符串参数或正则表达式参数
        """
        logger.info(f"____页面路径是 = {url}")
        expect(self.page).to_have_url(url)

    @allure.step("断言 --> 显示提示信息：{message}")
    def assert_prompt_information(self, message, locator="[role=alert]"):
        """
        断言：等待提示信息出现，并验证提示信息
        :param locator:
        :param message:
        :return:
        """
        logger.info(f"____元素 - {locator} 包含 - {message}")
        try:
            self.page.locator(locator).wait_for()
            expect(self.page.locator(locator)).to_have_text(message)
            # 等待提示信息消失
            self.page.wait_for_selector(locator, state="detached")
        except Exception as e:
            ExceptionHandle().handle_exception(e, "assert")

    @allure.step("校验--进入页面{page_name}")
    def assert_enter_page(self, page_name):
        """
        校验系统是否进入指定的页面
        :param page_name:
        :return:
        """
        logger.info(f"校验系统是否进入页面：{page_name}")
        try:
            # 获取当前页面标题
            currect_page_name = self.page.locator(".tags-view-item.active").inner_text()
            assert currect_page_name == page_name
        except Exception as e:
            ExceptionHandle().handle_exception(e, "assert")
