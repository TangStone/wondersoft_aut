# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: data_dict_page.py
@IDE: PyCharm
@time: 2024-04-28 16:14
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


class DataDictPage(BasePage):
    """
    数据字典页面操作封装
    """
    @allure.step("根据查询条件查询数据字典，查询条件：{query_conditions}")
    def search_datadict(self, query_conditions):
        logger.info("………………………………数据字典查询start………………………………")
        try:
            cond_type_dict = {
                "规则名称": "input",
                "规则来源": "dropdown",
                "使用状态": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………数据字典查询end………………………………")

    @allure.step("删除数据字典：{datadict_name}")
    def delete_datadict(self, datadict_name):
        logger.info("………………………………删除数据字典start………………………………")
        try:
            logger.info(f"删除数据字典：{datadict_name}")
            self.search_datadict({"规则名称": datadict_name})
            datadict_list = self.table_all_row_td(2)  # 获取查询的所有关键字/正则规则配置
            logger.debug(f"数据字典查询列表：{datadict_list}")
            self.button_operate_with_line(datadict_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………删除数据字典end………………………………")

    @allure.step("输入新增数据字典信息：{data_dict_info}")
    def input_data_dict_info(self, data_dict_info):
        """
        新增数据字典页面，输入数据字典信息
        :param data_dict_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增数据字典")
        # 页面参数配置类型
        para_conf_type_dict = {
            "规则名称": "input",
            "规则内容配置": {
                "关键字": "input",
                "分数": "input"
            }
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in data_dict_info.items():
            if para == '规则内容配置':  # 规则内容配置,一组一组添加
                for rule in para_value:
                    # 添加关键字
                    self.input_locator_by_para(rule['关键字'], "关键字", location)
                    # 添加分数
                    self.input_locator_by_para(rule['分数'], "分数", location)
                    # 定位到分数模块
                    score_location = self.locate_by_para_name("分数", location)
                    # 点击"添加"按钮
                    self.click_by_role_text("button", "添加", score_location)
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)

    @allure.step("校验--数据字典详情中包含：{expect_data_dict_info}")
    def assert_data_dict_info(self, expect_data_dict_info, ):
        """
        校验数据字典详情
        :param expect_data_dict_info: 期望数据字典详情信息
        :return:
        """
        flag = True
        location = self.get_label_locator("查看详情")
        for para, expect_para_value in expect_data_dict_info.items():
            # 根据参数名称获取参数值
            para_value = location.locator(".item span", has_text=re.compile("^" + para + ".*：$")).locator(
                "../span[2]").inner_text()
            logger.info(f"参数【{para}】，期望值：{expect_para_value}，实际值：{para_value}")
            if para_value != expect_para_value:
                flag = False
                break
        assert flag
