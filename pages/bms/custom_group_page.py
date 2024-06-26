# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: custom_group_page.py
@IDE: PyCharm
@time: 2024-04-02 17:24
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


class CustomGroupPage(BasePage):
    """
    自定义用户组管理页面操作封装
    """
    @allure.step("根据查询条件查询自定义用户组，查询条件{query_conditions}")
    def search_custom_group(self, query_conditions: dict):
        ui_logger.info("………………………………自定义用户组查询start………………………………")
        try:
            cond_type_dict = {
                "用户组名称": "input",
                "使用状态": "dropdown"
            }
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………自定义用户组查询end………………………………")

    @allure.step("删除自定义用户组：{custom_group_name}")
    def delete_custom_group(self, custom_group_name):
        ui_logger.info("………………………………删除自定义用户组start………………………………")
        try:
            ui_logger.info(f"删除自定义用户组：{custom_group_name}")
            self.search_custom_group({"用户组名称": custom_group_name})
            custom_group_list = self.table_all_row_td(2)  # 获取查询的所有数据源配置
            ui_logger.debug(f"自定义用户组查询列表：{custom_group_list}")
            self.button_operate_with_line(custom_group_name, "删除")  # 点击操作模块的【删除】按钮
            # self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            # common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            # common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除自定义用户组end………………………………")

    @allure.step("输入用户组名称：{group_name}，备注：{remark}")
    def input_group_name(self, group_name: str, remark: str):
        # 输入用户组名称
        self.page.get_by_label("新增用户组").get_by_placeholder("请输入用户组名称").click()
        self.page.get_by_label("新增用户组").get_by_placeholder("请输入用户组名称").fill(group_name)
        # 输入备注
        self.page.get_by_placeholder("请输入备注").click()
        self.page.get_by_placeholder("请输入备注").fill(remark)

    @allure.step("添加用户页面选择用户：{user}")
    def check_user(self, user: str):
        # 输入账号
        self.page.get_by_placeholder("请输入账号").click()
        self.page.get_by_placeholder("请输入账号").fill(user)
        # 点击【查询】按钮
        self.page.get_by_label("添加用户").get_by_role("button", name="搜索").click()
        # 勾选用户
        # # self.page.get_by_role("cell", name="ceshi").locator("../../label").check()
        # self.page.locator(".el-table__fixed-body-wrapper > .el-table__body > tbody > .el-table__row > .el-table_4_column_17 > .cell > .el-checkbox > .el-checkbox__input > .el-checkbox__inner").first.check()

        self.table_row_check(user)
        # 点击【确定】按钮
        self.page.get_by_label("添加用户").get_by_role("button", name="确定").click()
