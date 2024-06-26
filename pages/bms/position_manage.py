# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: role.py
@IDE: PyCharm
@time: 2024-04-22 18:24
@description:
"""
# 标准库导入
# 第三方库导入
import allure
from common.logger_handle import ui_logger
# 本地模块导入
from common.exception_handle import ExceptionHandle
from common.base_page import BasePage
from pages import common_page


class PositionManagePage(BasePage):
    """
    职位管理页面操作封装
    """
    @allure.step("根据查询条件查询职位列表，查询条件{query_conditions}")
    def search_positions(self, query_conditions: dict):
        ui_logger.info("………………………………职位列表查询start………………………………")
        try:
            cond_type_dict = {
                "职位": "input",  # 输入框
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………职位列表查询end………………………………")

    @allure.step("删除职位：{position_name}")
    def delete_position(self, position_name):
        ui_logger.info("………………………………删除职位start………………………………")
        try:
            ui_logger.info(f"删除职位：{position_name}")
            self.search_positions({"职位": position_name})
            position_list = self.table_all_row_td(1)  # 获取查询的所有职位
            ui_logger.debug(f"用户查询列表：{position_list}")
            self.button_operate_with_line(position_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除职位end………………………………")

    @allure.step("导入职位文件：{position_file}")
    def import_position(self, position_file):
        """
        导入职位文件
        :param position_file: 职位文件
        :return:
        """
        self.upload_file(".el-upload__input", position_file)

    @allure.step("校验职位列表中包含：{expect_positions}")
    def assert_position_list(self, expect_positions):
        """
        校验职位列表
        :param expect_positions: 期望职位
        :return:
        """
        expect_position_list = expect_positions.split("、")   # 期望职位
        position_list = self.table_all_row_td(1)
        assert set(expect_position_list).issubset(set(position_list))


