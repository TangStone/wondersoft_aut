# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: user_group_page.py
@IDE: PyCharm
@time: 2024-03-28 17:28
@description: 用户及机构管理页面操作封装
"""
# 标准库导入
import re
# 第三方库导入
import allure
from utils.log_utils.logger_handle import api_logger,ui_logger
# 本地模块导入
from utils.base_utils.exception_handle import ExceptionHandle
from utils.ui_utils.base_page import BasePage
from pages import common_page


class UserGroupPage(BasePage):
    """
    用户及机构管理页面操作封装
    """
    @allure.step("根据查询条件查询用户列表，查询条件{query_conditions}")
    def search_users(self, query_conditions: dict):
        ui_logger.info("………………………………用户列表查询start………………………………")
        try:
            cond_type_dict = {
                "账号": "input",  # 输入框
                "姓名": "input",
                "邮箱": "input",
                "用户sid": "input",
                "手机号": "input",
                "职位": "dropdown",   # 下拉框
                "用户组范围": "dropdown"
            }
            self.icon_arrow_up()  # 若存在高级查询条件，展开高级查询条件
            # 查询数据输入
            for para, para_value in query_conditions.items():
                if para in cond_type_dict.keys():
                    self.para_config(para, cond_type_dict[para], para_value)
            common_page.CommonPage(self.page).click_button("搜索")  # 点击【搜索】按钮
            self.page.wait_for_load_state()
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………用户列表查询end………………………………")

    @allure.step("删除用户：{username}")
    def delete_user(self, username):
        ui_logger.info("………………………………删除用户start………………………………")
        try:
            ui_logger.info(f"删除用户：{username}")
            self.search_users({"账号": username})
            user_list = self.table_all_row_td(2)  # 获取查询的所有用户
            ui_logger.debug(f"用户查询列表：{user_list}")
            self.button_operate_with_line(username, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除用户end………………………………")

    @allure.step("删除机构：{organ}")
    def delete_group(self, organ):
        ui_logger.info("………………………………删除用户组start………………………………")
        try:
            ui_logger.info(f"删除组织机构：{organ}")
            group_name, group_location = self.tree_node_location(organ)   # 根据所属机构定位到最底层机构模块
            group_location.locator(
                "xpath=/div[@class='el-tree-node__content']//span[@class='custom-tree-button']/span[3]").click()  # 在最底层机构模块点击【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除用户组end………………………………")

    @allure.step("组织机构：{parent_group_name}下新增组织机构：{group_name}")
    def group_add(self, parent_group_name: str, group_name: str):
        # 点击”新增下级节点按钮“
        self.page.locator("#app div").filter(has_text=re.compile(r"^" + parent_group_name + "$"))\
            .locator(".custom-tree-button > span").first.click()
        # 输入机构名称
        self.page.get_by_placeholder("请输入机构名称").click()
        self.page.get_by_placeholder("请输入机构名称").fill(group_name)
        # 点击”确定“按钮
        self.page.get_by_role("button", name="确认").click()

    @allure.step("在左侧组织机构栏中，展开: {parent_group_name}，存在新增的机构: {group_name}")
    def assert_group_add(self, parent_group_name: str, group_name: str):
        # 获取父节点整个模块
        name_mod = self.page.locator("#app div").filter(has_text=re.compile(r"^" + parent_group_name + "$"))
        parent_mod = name_mod.locator("../..")
        # 判断父节点是否展开,若没有，则点击展开
        if parent_mod.locator("div").nth(1).get_attribute("aria-expanded", timeout=500) is None:
            name_mod.locator("span").first.click()
        # 获取所有下级机构名称
        child_mod = parent_mod.locator("div > div").nth(1).locator(".custom-tree-node > span").all()
        flag = False
        for i in child_mod:
            if i.inner_text() == group_name:
                flag = True
        assert flag

    @allure.step("校验--鼠标悬浮在组织机构：{organ}, 显示组织机构全称：{hover_info}")
    def assert_hover(self, organ, hover_info):
        """
        悬浮提示信息校验
        :param organ: 所属机构： 默认组 -> 北京明朝万达 -> 人事行政中心 -> 人事部
        :param hover_info: 悬浮提示信息
        :return:
        """
        # 根据所属机构定位到最底层机构模块
        group_name, group_location = self.tree_node_location(organ)
        # 在最底层机构模块获取机构名称模块
        group_name_location = group_location.locator("xpath=/div[@class='el-tree-node__content']//span[text()='" + group_name + "']")
        # # 鼠标悬浮后校验提示信息
        self.location_hover_have_text(hover_info, group_name_location)

    @allure.step("在用户新增页面输入用户信息：{user_info}")
    def input_user_info(self, user_info: dict):
        """
        在用户新增页面输入用户信息
        :param user_info:
        :return:
        """
        # 定位到新增页面
        location = self.get_label_locator("新增")
        # 页面参数配置类型
        para_conf_type = {
            "账号": "input",   # 输入框
            "认证方式": "dropdown",  # 下拉框
            "姓名": "input",
            "性别": "radio",   # radio点选
            "所属机构": "dropdown",
            "上级领导人": "dropdown",
            "base地": "dropdown",
            "职位": "dropdown",
            "其他职位": "dropdown",
            "是否管理员": "radio",
            "管理员角色": "dropdown",
            "管理机构": "dropdown",
            "工号": "input",
            "ip": "input",
            "电话": "input",
            "手机": "input",
            "电子邮箱": "input",
            "备注": "textarea",  # 文本框
            "IP段类型": "radio",
            "IP段配置": "input"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in user_info.items():
            if para in para_conf_type:
                if para_conf_type[para] == "input":   # input输入框
                    self.input_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "dropdown":  # 下拉框
                    self.dropdown_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "radio":  # 下拉框
                    self.radio_locator_by_para(para_value, para, location)
                elif para_conf_type[para] == "textarea":  # 文本框
                    self.textarea_locator_by_para(para_value, para, location)
            # 未定义的参数
            else:
                pass

    @allure.step("用户管理模块输入搜索条件：{search_condition}")
    def input_search_condition(self, search_condition):
        """
        用户管理模块输入搜索条件
        :param search_condition: 搜索条件
        :return:
        """
        # 展开参数
        expand_button = self.page.locator(".el-tabs__content .el-button.el-button--text.el-button--small")
        if expand_button.inner_text() == '展开':
            expand_button.click()
        # 页面参数配置类型
        para_conf_type_dict = {
            "账号": "input",  # 输入框
            "姓名": "input",
            "邮箱": "input",
            "用户sid": "input",
            "手机号": "input",
            "职位": "dropdown",   # 下拉框
            "用户组范围": "dropdown"
        }
        # 遍历传入的用户信息，进行数据输入
        for para, para_value in search_condition.items():
            if para in para_conf_type_dict.keys():
                self.para_config(para, para_conf_type_dict[para], para_value)

    @allure.step("校验--用户列表显示条数：{user_list_totle}, 数据量显示：{data_volume_display}")
    def assert_user_list_display(self, user_list_totle, data_volume_display):
        """
        用户根据搜索条件搜索后，校验返回值
        :param user_list_totle: 列表首页显示条数
        :param data_volume_display: 统计信息
        :return:
        """
        # 获取返回值
        username_list = self.table_all_row_td(1)
        # # 获取统计信息
        # statistic = self.page.locator(".pagination-container>div:nth-child(2)>p>span").inner_text()
        # 校验列表显示条数
        assert len(username_list) == int(user_list_totle)
        # 校验数据量显示
        self.have_text(".pagination-container>div:nth-child(2)>p>span", data_volume_display)


