# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: log_backup.py
@IDE: PyCharm
@time: 2024-04-25 13:17
@description:
"""
# 标准库导入
# 第三方库导入
import allure
from loguru import logger
# 本地模块导入
from pages.common_page import CommonPage
from utils.ui_utils.base_page import BasePage
from utils.base_utils.exception_handle import ExceptionHandle


class LogBackupPage(BasePage):
    """
    日志备份配置页面操作封装
    """
    @allure.step("编辑备份配置【{business_type}】，修改信息：{business_info}")
    def update_business(self, business_type, business_info):
        """
        编辑备份配置
        :param business_type: 日志类型
        :param business_info: 编辑信息
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("编辑备份配置")
        # 定义各个参数配置类型
        para_conf_type_dict = {
            "定时备份": "checkbox_switch",  # 勾选框
            "执行时间": "input",   # 输入框
            "存储方式": "checkbox_group",
            "留存时间": "radio",  # radio点选
        }
        # 遍历传入的备份配置信息，进行数据输入
        for para, para_value in business_info.items():
            if para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
