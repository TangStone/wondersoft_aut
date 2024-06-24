# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: doc_attribute_rules_page.py
@IDE: PyCharm
@time: 2024-04-28 18:25
@description:
"""
# 标准库导入
import re
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from utils.ui_utils.base_page import BasePage
from utils.base_utils.exception_handle import ExceptionHandle
from pages import common_page


class DocAttributeRulesPage(BasePage):
    """
    文件属性规则页面操作封装
    """
    @allure.step("根据查询条件查询文件属性规则，查询条件：{query_conditions}")
    def search_doc_attribute_rules(self, query_conditions):
        ui_logger.info("………………………………文件属性规则查询start………………………………")
        try:
            cond_type_dict = {
                "规则名称": "input",
                "属性类型": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………文件属性规则查询end………………………………")

    @allure.step("删除文件属性规则：{doc_attribute_rule_name}")
    def delete_doc_attribute_rules(self, doc_attribute_rule_name):
        ui_logger.info("………………………………删除文件属性规则start………………………………")
        try:
            ui_logger.info(f"删除文件属性规则：{doc_attribute_rule_name}")
            self.search_doc_attribute_rules({"规则名称": doc_attribute_rule_name})
            doc_attribute_rule_list = self.table_all_row_td(2)  # 获取查询的所有文件属性规则
            ui_logger.debug(f"文件属性规则查询列表：{doc_attribute_rule_list}")
            self.button_operate_with_line(doc_attribute_rule_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除文件属性规则end………………………………")

    @allure.step("输入新增属性规则信息：{attribute_rule_info}")
    def input_attribute_rule_info(self, attribute_rule_info):
        """
        新增属性规则页面，输入属性规则信息
        :param attribute_rule_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增属性规则")
        # 页面参数配置类型
        para_conf_type_dict = {
            "规则名称": "input",
            "备注": "textarea",
            "规则类型": "dropdown"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in attribute_rule_info.items():
            if para == '文件分类':
                for file_type_link in para_value:
                    # 根据节点链路定位最底层节点
                    file_type, file_type_location = self.tree_node_location(file_type_link, location)
                    # 勾选文件分类
                    file_type_location.locator(".el-tree-node__content label").check()
            elif para == '识别类型':   # '识别类型': {'格式识别类型': {'可执行文件格式': ['exe']}}
                for file_title, file_content in para_value.items():
                    # 定位到第一大类
                    file_content_location = location.locator(
                        "//div[@class='file-title']/div[text()='" + file_title + "']/../../div[@class='file-content']")
                    if type(file_content) == dict:
                        for category, formats in file_content.items():
                            # 根据类别名称定位到类别模块
                            category_location = file_content_location.locator(
                                "//div[@class='category-item-name']/../div[@role='group']")
                            if type(formats) == list:
                                for fm in formats:
                                    # 定位到具体的格式并勾选
                                    category_location.locator("xpath=/label/span[text()=' " + fm + " ']/..").check()
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
