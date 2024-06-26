# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: sys_param.py
@IDE: PyCharm
@time: 2024-04-23 17:16
@description:
"""
# 标准库导入
# 第三方库导入
import allure
# 本地模块导入
from common.base_page import BasePage


class SysParamPage(BasePage):
    """
    系统参数管理页面操作封装
    """
    @allure.step("将系统参数：{para}的值修改为{para_value}")
    def update_para(self, para, para_value):
        """
        修改系统参数
        :param para: 参数名称
        :param para_value: 参数值
        :return:
        """
        # 根据参数名称定位到参数配置行
        para_line = self.table_row(para, table_type=2)
        # 点击编辑按钮
        para_line.get_by_role("button", name="编辑").click()
        # 输入参数值
        self.input_by_placeholder("请输入", para_value, para_line)
        # 点击提交按钮
        para_line.get_by_role("button", name="提交").click()



