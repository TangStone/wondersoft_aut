# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: access-strategy.py
@IDE: PyCharm
@time: 2024-04-23 9:53
@description:
"""
# 标准库导入
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from utils.base_utils.exception_handle import ExceptionHandle
from utils.ui_utils.base_page import BasePage
from pages import common_page


class AccessStrategyPage(BasePage):
    """
    管理员登录限制页面操作封装
    """
    @allure.step("根据查询条件查询限制列表，查询条件{query_conditions}")
    def search_strategy(self, query_conditions: dict):
        ui_logger.info("………………………………限制策略查询start………………………………")
        try:
            cond_type_dict = {
                "IP地址": "input"  # 输入框
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………限制策略查询end………………………………")

    @allure.step("删除限制：{strategy_range}")
    def delete_strategy(self, strategy_range):
        ui_logger.info("………………………………删除限制start………………………………")
        try:
            ui_logger.info(f"删除限制：{strategy_range}")
            self.search_strategy({"IP地址": strategy_range})
            strategy_list = self.table_all_row_td(2)  # 获取查询的所有职位
            ui_logger.debug(f"限制列表：{strategy_list}")
            self.button_operate_with_line(strategy_range, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除限制end………………………………")

    @allure.step("新增限制范围：{strategy_info}")
    def add_strategy_info(self, strategy_info):
        """
        录入
        :param strategy_info: 限制信息
        :return:
        """
        # 定位到录入页面
        location = self.get_label_locator("录入")
        # 页面参数配置类型
        para_conf_type = {
            "ip": "input",  # 输入框
            "类型": "radio",  # radio点选
        }
        # 遍历传入的信息，进行数据输入
        for para, para_value in strategy_info.items():
            if para in para_conf_type:
                if para_conf_type[para] == "input":  # input输入框
                    self.input_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "dropdown":  # 下拉框
                    self.dropdown_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "radio":  # 下拉框
                    self.radio_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "textarea":  # 文本框
                    self.textarea_locator_by_para(para_value, para, location)
            # 未定义的参数
            else:
                pass

    @allure.step("{control}全局控制")
    def set_global_controls(self, control):
        """
        开启/关闭全局控制
        :param control:
        :return:
        """
        # 全局控制勾选框
        control_checkbox = self.page.locator('[role="switch"]')
        if control == "开启":
            control_checkbox.check()
        else:
            control_checkbox.uncheck()

        # 等待提示框出现
        self.wait_for_selector('[role="dialog"][aria-label="提示"]')
        # 点击确定按钮
        self.click_by_role_text("button", "确定")

