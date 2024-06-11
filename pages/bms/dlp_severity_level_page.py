# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: dlp_severity_level_page.py
@IDE: PyCharm
@time: 2024-04-29 14:45
@description:
"""
# 标准库导入
import re
# 第三方库导入
import allure
from loguru import logger
# 本地模块导入
from utils.ui_utils.base_page import BasePage
from utils.base_utils.exception_handle import ExceptionHandle


class DlpSeverityLevelPage(BasePage):
    """
    严重性等级页面操作封装
    """

    @allure.step("输入新增严重性等级信息：{severity_level_info}")
    def input_severity_level_info(self, severity_level_info):
        """
        新增严重性等级页面，输入严重性等级信息
        :param severity_level_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增严重性等级")
        # 页面参数配置类型
        para_conf_type_dict = {
            "严重性等级名称": "input",
            "对应严重性等级": "input",
            "严重性等级颜色": "",
            "说明": "textarea"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in severity_level_info.items():
            if para == '严重性等级颜色':
                # 根据参数名称定位到参数模块
                para_location = self.locate_by_para_name(para, location)
                # 点击出现颜色选择模块
                para_location.locator(".el-color-picker__color").click()
                # 定位到颜色选择模块
                color_select_location = self.page.locator(".el-color-dropdown")
                # 在颜色输入框红输入颜色
                color_select_location.locator("input").clear()
                color_select_location.locator("input").fill(para_value)
                # 点击确定按钮
                self.click_by_role_text("button", "确定", color_select_location)
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
