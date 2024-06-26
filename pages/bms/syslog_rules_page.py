# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: syslog_rules_page.py
@IDE: PyCharm
@time: 2024-04-26 17:54
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

class SyslogRulesPage(BasePage):
    """
    Syslog规则配置页面操作封装
    """
    @allure.step("根据查询条件查询syslog规则列表，查询条件{query_conditions}")
    def search_syslog_rules(self, query_conditions: dict):
        ui_logger.info("………………………………syslog规则列表查询start………………………………")
        try:
            cond_type_dict = {
                "查询时间": "date_range",  # 输入框
                "规则名称": "input"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………syslog规则列表查询end………………………………")

    @allure.step("删除syslog规则：{syslog_rule_name}")
    def delete_syslog_rule(self, syslog_rule_name):
        ui_logger.info("………………………………删除syslog规则start………………………………")
        try:
            ui_logger.info(f"删除syslog规则：{syslog_rule_name}")
            self.search_syslog_rules({"规则名称": syslog_rule_name})
            syslog_rules_list = self.table_all_row_td(2)  # 获取查询的所有管理员
            ui_logger.debug(f"syslog规则查询列表：{syslog_rules_list}")
            self.button_operate_with_line(syslog_rule_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除syslog规则end………………………………")

    @allure.step("输入新增告警任务信息：{syslog_rules_info}")
    def input_syslog_rules_info(self, syslog_rules_info):
        """
        新增告警任务页面，输入告警任务信息
        :param syslog_rules_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增规则配置")
        # 页面参数配置类型
        para_conf_type_dict = {
            "规则名称": "input",
            "Syslog地址": "textarea",
            "传输协议": "dropdown",
            "Syslog等级": "dropdown",
            "Syslog类型": "dropdown",
            "字符编码": "dropdown",
            "自定义分隔符": "input",
            "日志前缀": "input",
            "时间格式": "dropdown",
            "Syslog应用": "",
            "Syslog字段": ""
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in syslog_rules_info.items():
            if not para_conf_type_dict[para]:    # 没有定义类型的参数
                # 根据参数名称定位到参数模块
                para_location = self.locate_by_para_name(para, location)
                if para == "Syslog应用":
                    # 定位到下拉按钮
                    server_dropdown_button = para_location.locator("//input")
                    # 点击输入框
                    server_dropdown_button.click()
                    # 定位到下拉框
                    dropdown_location = self.page.locator("//div[@class='el-popper el-cascader__dropdown']")
                    # 选择一级应用
                    dropdown_location.locator(
                        "xpath=/div[@class='el-cascader-panel']/div[1]//span[text()='" + para_value[0] + "']").click()
                    # 选择二级应用
                    dropdown_location.locator(
                        "xpath=/div[@class='el-cascader-panel']/div[2]//span[text()='" + para_value[1] + "']").click()
                    server_dropdown_button.click()
                elif para == "Syslog字段":
                    # 点击下拉按钮
                    para_location.locator("//i").click()
                    # 定位到下拉框并选择值
                    self.dropdown_checkbox_group_check_value(para_value)
            elif para in para_conf_type_dict.keys():
                # 定位到下拉按钮
                self.para_config(para, para_conf_type_dict[para], para_value, location)
