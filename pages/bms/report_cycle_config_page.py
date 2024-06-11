# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: report_cycle_config_page.py
@IDE: PyCharm
@time: 2024-04-30 13:49
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
from pages import common_page


class ReportCycleConfigPage(BasePage):
    """
    智能报告管理页面操作封装
    """

    @allure.step("新增报告")
    def add_report(self, report_cycle_config):
        """
        新增报告全流程
        :param report_cycle_config: 新增报告信息
        :return:
        """
        logger.info("………………………………新增报告start………………………………")
        try:
            logger.debug(f"新增报告信息：{report_cycle_config}")
            # 判断是否存在同名报告
            report_name = report_cycle_config['报告名称']
            self.search_report({"报告名称": report_name})  # 根据报告名称查询报告
            report_list = self.table_all_row_td(2)    # 获取查询的所有报告名称
            logger.debug(f"报告查询列表：{report_list}")
            if report_name in report_list:  # 存在同名报告，删除报告
                self.delete_report(report_name)
            common_page.CommonPage(self.page).click_button("新增")  # 点击【新增】按钮
            self.input_report_cycle_config_info(report_cycle_config)  # 输入新增报告信息
            common_page.CommonPage(self.page).click_button("确认", "新增报告")  # 点击【新增报告】页面的【确认】按钮
            common_page.CommonPage(self.page).assert_prompt_information("新增成功")  # 弹出提示框，显示提示信息：新增成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………新增报告end………………………………")

    @allure.step("删除报告：{report_name}")
    def delete_report(self, report_name):
        logger.info("………………………………删除报告start………………………………")
        try:
            logger.info(f"删除报告：{report_name}")
            self.search_report({"报告名称": report_name})    # 根据报告名称查询报告
            report_list = self.table_all_row_td(2)  # 获取查询的所有报告名称
            logger.debug(f"报告查询列表：{report_list}")
            if report_name not in report_list:   # 报告不存在，新增报告
                report_base_info = {'报告名称': report_name, '报告类型': '快速报告', '报告格式': 'word',
                                    '报告模板': '终端全盘扫描',
                                    '报告时间范围': {'开始日期': '2024-04-29', '开始时间': '00:00:00',
                                                     '结束日期': '2024-04-29', '结束时间': '23:59:59'}}
                self.add_report(report_base_info)   # 新增报告
            self.button_operate_with_line(report_name, "删除")    # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")    # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………删除报告end………………………………")

    @allure.step("根据查询条件查询报告，查询条件：{query_conditions}")
    def search_report(self, query_conditions):
        logger.info("………………………………报告查询start………………………………")
        try:
            cond_type_dict = {
                "报告名称": "input",
                "报告类型": "dropdown",
                "报告模板": "dropdown",
                "状态": "dropdown"
            }
            self.icon_arrow_up()  # 若存在高级查询条件，展开高级查询条件
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………报告查询end………………………………")

    @allure.step("输入新增报告信息：{report_cycle_config}")
    def input_report_cycle_config_info(self, report_cycle_config):
        """
        新增报告页面，输入报告信息
        :param report_cycle_config:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增报告")
        # 页面参数配置类型
        para_conf_type_dict = {
            "报告名称": "input",
            "报告描述": "textarea",
            "报告类型": "radio",
            "报告周期": "dropdown",
            "执行时间": "time",
            "报告格式": "radio",
            "报告模板": "dropdown",
            "用户组": "dropdown",
            "报告时间范围": "date_range",
            "开启邮件发送": "checkbox_switch",
            "通知人邮箱": "input",
            "邮件内容": "textarea",
            "邮件主题": "input"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in report_cycle_config.items():
            if para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)

    # def search_report_cycle_config(self, query_conditions):
    #     """
    #     报告查询
    #     :param query_conditions: 查询条件
    #     :return:
    #     """
    #     cond_type_dict = {
    #         "报告名称": "input",
    #         "报告类型": "dropdown",
    #         "报告模板": "dropdown",
    #         "状态": "dropdown"
    #     }
    #     self.icon_arrow_up()   # 存在高级查询条件，展开
    #     # 遍历传入的用户信息，进行数据输入
    #     for para, para_value in query_conditions.items():
    #         if para in cond_type_dict.keys():
    #             self.para_config(para, cond_type_dict[para], para_value)

