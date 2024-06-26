# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: alarm_rules_page.py
@IDE: PyCharm
@time: 2024-04-26 10:15
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


class AlarmRulesPage(BasePage):
    """
    告警任务页面操作封装
    """

    @allure.step("根据查询条件查询告警任务列表，查询条件{query_conditions}")
    def search_alarm_rules(self, query_conditions: dict):
        ui_logger.info("………………………………告警任务列表查询start………………………………")
        try:
            cond_type_dict = {
                "告警任务名称": "input",  # 输入框
                "告警类型": "dropdown",
                "任务状态": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………告警任务列表查询end………………………………")

    @allure.step("删除告警任务：{alarm_rule_name}")
    def delete_alarm_rule(self, alarm_rule_name):
        ui_logger.info("………………………………删除告警任务start………………………………")
        try:
            ui_logger.info(f"删除告警任务：{alarm_rule_name}")
            self.search_alarm_rules({"告警任务名称": alarm_rule_name})
            alarm_rules_list = self.table_all_row_td(2)  # 获取查询的所有告警任务
            ui_logger.debug(f"告警任务查询列表：{alarm_rules_list}")
            self.button_operate_with_line(alarm_rule_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除告警任务end………………………………")

    @allure.step("校验--验证告警任务列表是否存在以下告警任务：{expect_alarm_rules}")
    def assert_alarm_rules(self, expect_alarm_rules):
        flag = True
        # 获取所有的告警任务
        alarm_rules = self.table_all_row_data()
        for row in expect_alarm_rules.rows:
            flag = any(row.items() <= item.items() for item in alarm_rules)
            if not flag:
                break
        assert flag

    @allure.step("输入新增告警任务信息：{alarm_rules_info}")
    def input_alarm_rules_info(self, alarm_rules_info):
        """
        新增告警任务页面，输入告警任务信息
        :param alarm_rules_info: 告警任务信息
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增")
        # 页面参数配置类型
        para_conf_type_dict = {
            "告警任务名称": "input",  # 输入框
            "告警任务描述": "textarea",
            "告警类型": "dropdown",  # 下拉框
            "告警对象": "",
            "通知方式": "radio",  # radio点选
            "通知人": "",
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in alarm_rules_info.items():
            if not para_conf_type_dict[para]:    # 没有定义类型的参数
                # 根据参数名称定位到参数模块
                para_location = self.locate_by_para_name(para, location)
                if para == "告警对象":
                    # 告警对象模块
                    alarm_rule_object_loc = para_location.locator(".service-association")
                    if alarm_rules_info['告警类型'] == "服务失联告警":
                        # ------选择告警对象-------
                        alarm_rule_object_loc.locator("xpath=/div[1]//input").click()
                        # 定位到下拉框并选择值
                        self.dropdown_check_value(para_value[0])
                        # -----选择具体的服务------
                        server_dropdown_button = alarm_rule_object_loc.locator("xpath=/div[2]//div[@class='el-select__tags']//input")
                        server_dropdown_button.click()
                        # 定位到下拉框并选择值
                        self.dropdown_checkbox_group_check_value(para_value[1])
                        server_dropdown_button.click()
                    # 告警频率模块
                    alarm_rule_freq_loc = para_location.locator(".alarm-line")
                    # 输入告警频率
                    self.input_by_placeholder("请输入告警频率", para_value[2], alarm_rule_freq_loc)
                    # 选择时、分
                    alarm_rule_freq_loc.locator("xpath=/div/div[3]//input").click()
                    # 定位到下拉框并选择值
                    self.dropdown_check_value(para_value[3])
                elif para == "通知人":
                    # 点击"添加管理员"按钮
                    self.click_by_role_text("button", "添加管理员", para_location)
                    # 定位到添加管理员
                    add_admin_label = self.get_label_locator("添加管理员")
                    # ------选择用户-------
                    user_dropdown_button = add_admin_label.locator(".el-dialog__body .el-input i")
                    user_dropdown_button.click()
                    # 定位到下拉框并选择值
                    self.dropdown_check_value(para_value)
                    user_dropdown_button.click()
                    # 点击"确认"按钮
                    self.click_by_role_text("button", "确认", add_admin_label)
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
