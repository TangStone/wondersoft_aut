# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: dlp_doc_rules_page.py
@IDE: PyCharm
@time: 2024-04-28 13:40
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


class DlpDocRulesPage(BasePage):
    """
    关键字/正则页面操作封装
    """
    @allure.step("根据查询条件查询关键字/正则，查询条件：{query_conditions}")
    def search_dlp_doc_rules(self, query_conditions):
        logger.info("………………………………关键字/正则查询start………………………………")
        try:
            cond_type_dict = {
                "规则名称": "input",
                "规则类型": "dropdown",
                "规则来源": "dropdown",
                "使用状态": "dropdown"
            }
            self.icon_arrow_up()  # 若存在高级查询条件，展开高级查询条件
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………关键字/正则查询end………………………………")

    @allure.step("删除关键字/正则规则：{dlp_doc_rules_name}")
    def delete_dlp_doc_rules(self, dlp_doc_rules_name):
        logger.info("………………………………删除关键字/正则规则start………………………………")
        try:
            logger.info(f"删除关键字/正则：{dlp_doc_rules_name}")
            self.search_dlp_doc_rules({"规则名称": dlp_doc_rules_name})
            dlp_doc_rules_list = self.table_all_row_td(2)  # 获取查询的所有关键字/正则规则配置
            logger.debug(f"关键字/正则规则查询列表：{dlp_doc_rules_list}")
            self.button_operate_with_line(dlp_doc_rules_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………删除关键字/正则规则end………………………………")

    @allure.step("输入新增规则信息：{dlp_doc_rules_info}")
    def input_dlp_doc_rules_info(self, dlp_doc_rules_info):
        """
        新增规则页面，输入规则信息
        :param dlp_doc_rules_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增规则")
        # 页面参数配置类型
        para_conf_type_dict = {
            "规则类型": "dropdown",
            "规则名称": "input",
            "规则详情": "input"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in dlp_doc_rules_info.items():
            if para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)

    @allure.step("校验--规则详情中包含：{expect_dlp_doc_rule_info}")
    def assert_dlp_doc_rule_info(self, expect_dlp_doc_rule_info,):
        """
        校验规则详情
        :param expect_dlp_doc_rule_info: 期望规则详情信息
        :return:
        """
        flag = True
        location = self.get_label_locator("查看详情")
        for para, expect_para_value in expect_dlp_doc_rule_info.items():
            # 根据参数名称获取参数值
            para_value = location.locator(".item span", has_text=re.compile("^" + para + ".*：$")).locator(
                "../span[2]").inner_text()
            logger.info(f"参数【{para}】，期望值：{expect_para_value}，实际值：{para_value}")
            if para_value != expect_para_value:
                flag = False
                break
        assert flag
