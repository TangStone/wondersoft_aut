# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: sys_homepage_conf_page.py
@IDE: PyCharm
@time: 2024-04-29 16:26
@description:
"""
# 标准库导入
# 第三方库导入
import allure

# 本地模块导入
from common.logger_handle import ui_logger
from common.base_page import BasePage
from common.exception_handle import ExceptionHandle
from pages import common_page

class SysHomePageConfPage(BasePage):
    """
    系统首页配置页面操作封装
    """
    @allure.step("根据查询条件查询系统首页配置列表，查询条件{query_conditions}")
    def search_homepages(self, query_conditions: dict):
        ui_logger.info("………………………………系统首页配置列表查询start………………………………")
        try:
            cond_type_dict = {
                "主页名称": "input",  # 输入框
                "是否大屏": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………系统首页配置列表查询end………………………………")

    @allure.step("删除系统首页配置：{homepage_name}")
    def delete_homepage(self, homepage_name):
        ui_logger.info("………………………………删除系统首页配置start………………………………")
        try:
            ui_logger.info(f"删除系统首页配置：{homepage_name}")
            self.search_homepages({"主页名称": homepage_name})
            homepage_list = self.table_all_row_td(1)  # 获取查询的所有管理员
            ui_logger.debug(f"系统首页配置查询列表：{homepage_list}")
            self.button_operate_with_line(homepage_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除系统首页配置end………………………………")

    @allure.step("输入新增主页信息：{homepage_info}")
    def input_homepage_info(self, homepage_info):
        """
        新增主页页面，输入主页信息
        :param homepage_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增主页")
        # 页面参数配置类型
        para_conf_type_dict = {
            "主页名称": "input",
            "是否大屏": "dropdown",
            "主页描述": "input",
            "报表": ""
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in homepage_info.items():
            if para == '报表':
                # 展开报表
                self.click_by_role_text("button", "报表", location)
                # 获取报表下拉框id
                tooltip_id = location.locator(".report-list-container button").get_attribute("aria-describedby")
                # 定位到下拉模块
                ui_logger.info(f"根据报表下拉框id：{tooltip_id}定位到下拉框")
                report_tooltip = self.page.locator("#" + tooltip_id)
                # # 定位到搜索框
                # select_location = report_tooltip.get_by_placeholder("请输入内容")
                for report_link in para_value:
                    # 节点链路列表
                    node_link_list = [i.strip() for i in report_link.split("->")]
                    # ui_logger.info(f"搜索报表{node_link_list[-1]}")
                    # select_location.clear()
                    # select_location.fill(node_link_list[-1])
                    # 定位到整个树
                    ui_logger.info("定位到报表树")
                    node_location = report_tooltip.locator("xpath=//*[@role='tree']")
                    # ui_logger.info(f"勾选报表：{node_link_list[-1]}")
                    # node_location.locator("//span[text()='" + node_link_list[-1] + "']/../label").check()

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
