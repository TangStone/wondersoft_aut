# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: doc_finger.py
@IDE: PyCharm
@time: 2024-04-28 16:57
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


class DocFingerPage(BasePage):
    """
    文件指纹页面操作封装
    """
    @allure.step("根据查询条件查询文件指纹，查询条件：{query_conditions}")
    def search_doc_finger(self, query_conditions):
        ui_logger.info("………………………………文件指纹查询start………………………………")
        try:
            cond_type_dict = {
                "指纹库名称": "input",
                "指纹计算状态": "dropdown",
                "使用状态": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………文件指纹查询end………………………………")

    @allure.step("删除文件指纹：{doc_finger_name}")
    def delete_doc_finger(self, doc_finger_name):
        ui_logger.info("………………………………删除文件指纹start………………………………")
        try:
            ui_logger.info(f"删除文件指纹：{doc_finger_name}")
            self.search_doc_finger({"指纹库名称": doc_finger_name})
            doc_finger_list = self.table_all_row_td(2)  # 获取查询的所有文件MD5
            ui_logger.debug(f"文件指纹查询列表：{doc_finger_list}")
            self.button_operate_with_line(doc_finger_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功！")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除文件指纹end………………………………")

    @allure.step("输入新增指纹库信息：{doc_finger_info}")
    def input_doc_finger_info(self, doc_finger_info):
        """
        新增指纹库页面，输入指纹库信息
        :param doc_finger_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增指纹库")
        # 页面参数配置类型
        para_conf_type_dict = {
            "指纹库名称": "input",
            "文件导入方式": ["radio", {
                "本地上传": {
                    "文件": "upload",
                    "指纹生成后是否删除该zip文件": "radio"
                },
                "服务器导入": {}
            }]
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in doc_finger_info.items():
            if para == '文件导入方式':  # 文件导入方式
                self.para_config(para, para_conf_type_dict[para][0], para_value, location)   # 选择文件导入方式
                # 选择文件导入方式后，需要输入的参数
                import_type_para_dict = para_conf_type_dict[para][1][para_value]
                for import_para, import_para_type in import_type_para_dict.items():
                    # if import_para == '文件':
                    #     self.upload_file(".el-upload__input", doc_finger_info[import_para])
                    # else:
                    self.para_config(import_para, import_para_type, doc_finger_info[import_para], location)
            elif para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value, location)
