# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: login_page.py
@IDE: PyCharm
@time: 2024-03-28 14:21
@description: 登录页面操作封装
"""
# 第三方库导入
import allure
# 本地模块导入
from common.base_page import BasePage


class LoginPage(BasePage):
    """
    登录页面操作封装
    """
    @allure.step("输入用户名：{username}，输入密码：{password}，点击登录")
    def login(self, username, password):
        """
        输入用户名、输入密码、点击登录
        """
        self.input_by_placeholder("请输入用户名", username)
        self.input_by_placeholder("请输入密码", password)
        self.click_by_role_text("button", "立即登录")

    @allure.step("判断是否需要重新登录")
    def relogin(self, full_url, username, password):
        """
        判断是否需要重新登录
        :param password: 密码
        :param username: 用户名
        :param full_url: 登录url
        :return:
        """
        self.page.wait_for_timeout(2000)
        # 判断是否跳转到登录页面
        if self.page.url == full_url:
            # 输入用户名和密码，点击【立即登录】按钮
            self.login(username, password)

