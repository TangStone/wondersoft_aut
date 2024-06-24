# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: sys_email.py
@IDE: PyCharm
@time: 2024-04-25 9:51
@description:
"""
# 标准库导入
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from pages.common_page import CommonPage
from utils.ui_utils.base_page import BasePage
from utils.base_utils.exception_handle import ExceptionHandle


class SysEmailPage(BasePage):
    """
    系统邮箱配置页面操作封装
    """
    @allure.step("系统邮箱配置修改-输入邮箱配置：{email_info}")
    def input_email_info(self, email_info):
        """
        输入邮箱配置信息
        :param email_info: 邮箱配置
        :return:
        """
        try:
            # 页面参数配置类型
            para_conf_type = {
                "是否使用微软Exchange": "dropdown",
                "系统邮箱编码": "input",  # 输入框
                "系统服务器地址": "input",
                "系统邮箱密码": "input",
                "系统邮箱端口": "input",
                "是否安全连接": "dropdown",  # 下拉框
                "系统邮箱用户": "input",
            }
            for para, para_value in email_info.items():
                if para in para_conf_type:
                    # 定位到需要操作的行
                    para_line_location = self.table_row(para, table_type=2)
                    self.email_para_config(para, para_conf_type[para], para_value, para_line_location)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    @allure.step("参数【email_para】提交，校验提示信息是否为：{pro_msg}")
    def assert_email_info_submit(self, email_para, pro_msg):
        """
        邮箱参数提交校验
        :param pro_msg: 提示信息
        :param email_para: 邮箱参数名称
        :return:
        """
        # 定位到需要操作的行
        para_line_location = self.table_row(email_para, table_type=2)
        # 点击提交按钮
        self.email_para_submit(email_para, para_line_location)
        # 校验提示信息
        CommonPage(self.page).assert_prompt_information(pro_msg)

    def email_para_config(self, para, para_conf_type, para_value, location):
        """
        邮件参数配置
        :param para: 参数名称
        :param para_conf_type: 参数类型
        :param para_value: 参数值
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"处理参数：{para}，参数输入类型：{para_conf_type}， 参数值：{para_value}")

        if para_conf_type == "input":  # input输入框
            self.email_para_input(para_value, para, location)
        elif para_conf_type == "dropdown":  # 下拉框
            self.email_para_dropdown(para_value, para, location)

    def email_para_input(self, input_value: str, para_name: str, location):
        """
        定位到邮箱配置参数输入框进行数据输入
        :param para_name: 参数名称
        :param input_value: 输入值
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"在参数：【{para_name}】的输入框中输入：{input_value}")
        # 定位到input输入框
        input_location = location.locator("xpath=/td[2]//input")
        # 清空输入框
        input_location.clear()
        # 输入值
        input_location.fill(input_value)

    def email_para_dropdown(self, select_value: str, para_name: str, location):
        """
        定位到邮箱配置参数下拉框进行数据选择
        :param select_value: 选择值
        :param para_name: 参数名称
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"在参数：【{para_name}】的下拉框中选择：{select_value}")
        # 定位到下拉输入框
        input_location = location.locator("xpath=/td[2]//input")
        # 点击下拉输入框
        input_location.click()
        # 定位到下拉框并选择值
        self.dropdown_check_value(select_value)

    def email_para_submit(self, para_name: str, location):
        """
        邮箱配置参数修改后提交
        :param para_name: 参数名称
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"提交参数修改：【{para_name}】")
        # 定位到提交按钮，点击提交按钮
        self.click_by_role_text("button", "提交", location)




