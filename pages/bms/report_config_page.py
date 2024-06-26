# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: report_config_page.py
@IDE: PyCharm
@time: 2024-04-30 13:22
@description:
"""
# 标准库导入
# 第三方库导入
import allure
from common.logger_handle import ui_logger
# 本地模块导入
from common.base_page import BasePage
from common.exception_handle import ExceptionHandle
from pages import common_page


class ReportConfigPage(BasePage):
    """
    报告模板管理页面操作封装
    """
    @allure.step("根据查询条件查询报告模板列表，查询条件{query_conditions}")
    def search_report_config(self, query_conditions: dict):
        ui_logger.info("………………………………报告模板列表查询start………………………………")
        try:
            cond_type_dict = {
                "模板名称": "input",  # 输入框
                "模板分类": "input",
                "是否被引用": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………报告模板列表查询end………………………………")

    @allure.step("删除报告模板：{report_config_name}")
    def delete_report_config(self, report_config_name):
        ui_logger.info("………………………………删除报告模板start………………………………")
        try:
            ui_logger.info(f"删除报告模板：{report_config_name}")
            self.search_report_config({"模板名称": report_config_name})
            report_config_list = self.table_all_row_td(2)  # 获取查询的所有报告模板
            ui_logger.debug(f"报告模板查询列表：{report_config_list}")
            self.button_operate_with_line(report_config_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除报告模板end………………………………")

    @allure.step("输入新增报告模板信息：{report_config_info}")
    def input_report_config_info(self, report_config_info):
        """
        新增报告模板页面，输入报告模板信息
        :param report_config_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增报告模板")
        # 页面参数配置类型
        para_conf_type_dict = {
            "模板名称": "input",
            "模板分类": "input",
            "报告组件": ""
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in report_config_info.items():
            if para == '报告组件':
                for report_link in para_value:
                    # 节点链路列表
                    node_link_list = [i.strip() for i in report_link.split("->")]
                    # 定位到整个树
                    ui_logger.info("定位到报表树")
                    node_location = location.locator("xpath=//*[@role='tree']")
                    # 根据节点链路列表，逐级定位，获取最后一级
                    for n in range(len(node_link_list)):
                        # 定位到节点模块
                        ui_logger.info(f"定位到模块【{node_link_list[n]}】")
                        node_location = node_location.locator(
                            "xpath=/div/div[@class='el-tree-node__content']/span[text()='" + node_link_list[
                                n] + "']/../..")
                        # 去除元素的aria-disabled属性
                        ui_logger.info("去除节点的aria-disabled属性")
                        node_location.evaluate("(node_location) => { node_location.removeAttribute('aria-disabled'); }")
                        # ui_logger.info(node_location.evaluate('(node_location) => node_location.outerHTML'))
                        # 判断节点是否展开，若没有展开，展开节点
                        if node_location.get_attribute("aria-expanded") is None:
                            ui_logger.info(f"展开节点【{node_link_list[n]}】")
                            node_location.locator(
                                "xpath=/div[@class='el-tree-node__content']/span[contains(@class,'el-tree-node__expand-icon')]").click()
                        # 不是最底层节点，获取子节点模块
                        if n != len(node_link_list) - 1:
                            node_location = node_location.locator("xpath=/div[@role='group']")
                    # 勾选节点
                    node_location.locator(".el-tree-node__content label").check()
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
