# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: user_admin.py
@IDE: PyCharm
@time: 2024-04-23 11:29
@description:
"""
# 标准库导入
import os
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from config.path_config import FILES_DIR
from utils.base_utils.exception_handle import ExceptionHandle
from utils.ui_utils.base_page import BasePage
from pages import common_page


class UserAdminPage(BasePage):
    """
    职位管理页面操作封装
    """
    @allure.step("根据查询条件查询管理员列表，查询条件{query_conditions}")
    def search_user_admin(self, query_conditions: dict):
        ui_logger.info("………………………………管理员列表查询start………………………………")
        try:
            cond_type_dict = {
                "登录名": "input",  # 输入框
                "角色": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………管理员列表查询end………………………………")

    @allure.step("删除管理员：{user_admin_name}")
    def delete_user_admin(self, user_admin_name):
        ui_logger.info("………………………………删除管理员start………………………………")
        try:
            ui_logger.info(f"删除管理员：{user_admin_name}")
            self.search_user_admin({"登录名": user_admin_name})
            user_admin_list = self.table_all_row_td(1)  # 获取查询的所有管理员
            ui_logger.debug(f"管理员查询列表：{user_admin_list}")
            self.button_operate_with_line(user_admin_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除管理员end………………………………")

    @allure.step("导入管理员文件：{user_admin_file}")
    def import_user_admin(self, user_admin_file):
        """
        导入管理员文件
        :param user_admin_file: 管理员文件
        :return:
        """
        # 上传文件
        self.upload_file(".el-upload__input", user_admin_file)

    @allure.step("校验管理员列表中包含：{expect_user_admin}")
    def assert_user_admin_list(self, expect_user_admin):
        """
        校验职位列表
        :param expect_user_admin: 期望职位
        :return:
        """
        expect_user_admin_list = expect_user_admin.split("、")  # 期望职位
        user_admin_list = self.table_all_row_td(1)
        assert set(expect_user_admin_list).issubset(set(user_admin_list))
