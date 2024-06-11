# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: doc_md5_page.py
@IDE: PyCharm
@time: 2024-04-28 17:36
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


class DocMd5Page(BasePage):
    """
    文件MD5页面操作封装
    """
    @allure.step("根据查询条件查询md5，查询条件：{query_conditions}")
    def search_docmd5(self, query_conditions):
        logger.info("………………………………文件MD5查询start………………………………")
        try:
            cond_type_dict = {
                "名称": "input"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………文件MD5查询end………………………………")

    @allure.step("删除数据字典：{docmd5_name}")
    def delete_docmd5(self, docmd5_name):
        logger.info("………………………………删除文件MD5start………………………………")
        try:
            logger.info(f"删除文件MD5：{docmd5_name}")
            self.search_docmd5({"规则名称": docmd5_name})
            docmd5_list = self.table_all_row_td(2)  # 获取查询的所有文件MD5
            logger.debug(f"文件MD5查询列表：{docmd5_list}")
            self.button_operate_with_line(docmd5_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="操作"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "操作")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        logger.info("………………………………删除文件MD5end………………………………")

    @allure.step("输入MD5规则导入信息：{doc_md5_info}")
    def input_doc_md5_info(self, doc_md5_info):
        """
        导入MD5规则页面，输入导入信息
        :param doc_md5_info:
        :return:
        """
        try:
            # 定位到导入页面
            location = self.get_label_locator("规则导入")
            # 页面参数配置类型
            para_conf_type_dict = {
                "是否覆盖现有文件MD5名称": "radio",
                "文件MD5名称": "input",
                "文件": "upload"
            }
            # 遍历传入的用户信息，进行数据输入
            for para, para_value in doc_md5_info.items():
                if para == "文件":
                    self.upload_file(".el-upload__input", para_value)
                elif para in para_conf_type_dict.keys():
                    # 定位到需要操作的行
                    para_location = location.locator(".dlp-file-finger-container > div > span",
                                                     has_text=re.compile("^" + para + ".*：$")).locator("..")
                    self.md5_para_config(para, para_conf_type_dict[para], para_value, para_location)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def md5_para_config(self, para, para_conf_type, para_value, location):
        """
        md5规则导入参数配置
        :param para: 参数名称
        :param para_conf_type: 参数类型
        :param para_value: 参数值
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        logger.info(f"处理参数：{para}，参数输入类型：{para_conf_type}， 参数值：{para_value}")

        if para_conf_type == "input":  # input输入框
            self.md5_para_input(para_value, para, location)
        elif para_conf_type == "radio":  # 下拉框
            self.md5_para_radio(para_value, para, location)

    @staticmethod
    def md5_para_radio(check_value: str, para_name: str, location):
        """
        定位到规则导入参数点选框进行数据点选
        :param para_name: 参数名称
        :param check_value: 点选值
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        logger.info(f"在参数：【{para_name}】的点选模块选择：{check_value}")
        # 选择参数
        location.locator('//div[@role="radiogroup"]//span[text()="' + check_value + '"]/..').check()

    @staticmethod
    def md5_para_input(input_value: str, para_name: str, location):
        """
        定位到规则导入参数输入框进行数据输入
        :param para_name: 参数名称
        :param input_value: 输入值
        :param location: 定位器，在相对模块进行定位
        :return:
        """
        logger.info(f"在参数：【{para_name}】的输入框中输入：{input_value}")
        # 定位到input输入框
        input_location = location.locator("xpath=//input")
        # 清空输入框
        input_location.clear()
        # 输入值
        input_location.fill(input_value)

