# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: user_syncManager.py
@IDE: PyCharm
@time: 2024-04-15 14:33
@description: 用户推送页面操作封装
"""
# 标准库导入
import re
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from utils.ui_utils.base_page import BasePage


class UseSyncManagerPage(BasePage):
    """
    用户推送页面操作封装
    """

    @allure.step("点击系统{system_name}的{operate}操作按钮")
    def system_operate(self, system_name, operate):
        """
        业务系统相关操作
        :param system_name: 系统名称
        :param operate:操作
        :return:
        """
        # # 定位到需要进行操作的行
        # selem = self.page.get_by_role("cell", name=system_name, exact=True).locator("../..")
        # # selem = self.page.get_by_role("cell", name=system_name, exact=True).locator('../..//button[@title="' + operate + '"]')
        # ui_logger.info("f==========")
        # ui_logger.info(selem.inner_html())
        # # 定位到对应的操作按钮，点击按钮
        # selem.locator('//*[@title="' + operate + '"]').click()




