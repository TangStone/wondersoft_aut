# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: base_page.py
@IDE: PyCharm
@time: 2024-03-27 18:37
@description: Playwright UI自动化基础操作封装
"""
# 标准库导入
import re, os
# 第三方库导入
from common.logger_handle import ui_logger
from playwright.sync_api import Page, expect
# 本地模块导入
from config.path_config import FILES_DIR
from common.exception_handle import ExceptionHandle


class BasePage:
    """
    Playwright UI自动化基础操作封装
    """

    def __init__(self, page: Page):
        """

        :param page:
        """
        self.page = page

    # ---------------- 页面相关操作 ----------------
    def visit(self, url: str):
        """
        访问页面
        :param url:
        :return:
        """
        self.page.goto(url)
        ui_logger.info(f"访问页面：{url}")

    def wait_for_selector(self, selector: str):
        """
        等待元素出现
        :param selector: 元素选择器
        :return:
        """
        ui_logger.info(f"等待元素：{selector}")
        return self.page.wait_for_selector(selector, strict=True)

    # ---------------- 查询相关操作 ----------------
    def icon_arrow_up(self):
        """
        展开高级查询条件
        :return:
        """
        ui_logger.info(f"若存在高级查询条件，展开高级查询条件")
        try:
            # self.page.wait_for_load_state()
            self.page.wait_for_selector("xpath=//form/div[last()]/div/button")
            # 判断是否存在高级查询选项
            button_location = self.page.locator("xpath=//form/div[last()]/div/button")
            if button_location.count() == 3:  # 存在高级查询条件，展开
                button_location.nth(2).click()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 定位相关操作 ----------------
    def get_label_locator(self, lable_name):
        """
        根据lable名称定位到lable标签页
        :param lable_name: lable名称
        :return: lable定位
        """
        ui_logger.info(f"定位到lable：{lable_name}")
        locator = self.page.get_by_label(lable_name)
        return locator

    def tree_node_location(self, node_link: str, location=None):
        """
        根据节点链路在树状图中定位到最底层节点
        :param node_link: 节点链路，如：默认组 -> 北京明朝万达 -> 人事行政中心 -> 人事部
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return: 定位
        """
        ui_logger.info(f"根据节点链路定位最底层节点：{node_link}")
        try:
            if location is None:
                location = self.page
            # 节点链路列表
            node_link_list = [i.strip() for i in node_link.split("->")]
            # 定位到整个树
            node_location = location.locator("xpath=//*[@role='tree']")
            # 根据节点链路列表，逐级定位，获取最后一级
            for n in range(len(node_link_list)):
                # 定位到节点模块
                node_location = node_location.locator(
                    "xpath=/div/div[@class='el-tree-node__content']//span[text()='" + node_link_list[
                        n] + "']/../../..")
                # 判断节点是否展开，若没有展开，展开节点
                if node_location.get_attribute("aria-expanded") is None:
                    node_location.locator(
                        "xpath=/div[@class='el-tree-node__content']/span[contains(@class,'el-tree-node__expand-icon')]").click()
                # 不是最底层节点，获取子节点模块
                if n != len(node_link_list) - 1:
                    node_location = node_location.locator("xpath=/div[@role='group']")
            return node_link_list[-1], node_location
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 页面输入操作统一处理 ----------------
    def para_config(self, para, para_conf_type, para_value, location=None):
        """
        各个参数配置统一处理入口
        :param para_conf_type: 参数类型
        :param para: 参数名称
        :param para_value: 参数值
        :param location:
        :return: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        """
        ui_logger.info(f"处理参数：{para}，参数输入类型：{para_conf_type}， 参数值：{para_value}")
        try:
            if location is None:
                location = self.page
            if para_conf_type == "input":  # input输入框
                self.input_locator_by_para(para_value, para, location)
            elif para_conf_type == "dropdown":  # 下拉框
                self.dropdown_locator_by_para(para_value, para, location)
            elif para_conf_type == "radio":  # 点选框
                self.radio_locator_by_para(para_value, para, location)
            elif para_conf_type == "textarea":  # 文本框
                self.textarea_locator_by_para(para_value, para, location)
            elif para_conf_type == "checkbox_switch":  # 勾选框-switch类型
                self.checkbox_switch_conf_by_para_name(para_value, para, location)
            elif para_conf_type == "checkbox_group":  # 勾选框-group类型
                self.checkbox_group_conf_by_para_name(para_value, para, location)
            elif para_conf_type == 'upload':  # 上传文件操作
                self.upload_file(".el-upload__input", para_value)
            elif para_conf_type == 'date_range':  # 日期范围选择
                self.select_date_range_conf_by_para_name(para_value, para, location)
            elif para_conf_type == 'time':  # 时间选择
                self.select_time_conf_by_para_name(para_value, para, location)
            else:
                pass
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def locate_by_para_name(self, para_name, location=None):
        """
        根据参数名称定位到参数所在的模块
        :param para_name: 参数名称
        :param location:
        :return:
        """
        ui_logger.info(f"定位到参数【{para_name}】模块")
        try:
            if location is None:
                location = self.page
            # para_location = location.locator("form div label", has_text=re.compile(r"^" + para_name + ".*：$")).locator("..")
            para_location = location.locator("form div label",
                                             has_text=re.compile(r"^\s*" + para_name + ".*[：:]\s*$")).locator(
                "..")
            return para_location
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 时间下拉框相关操作 ----------------
    def time_location(self):
        """
        在整个页面获取时间下拉框
        :return:
        """
        ui_logger.info(f"在整个页面定位时间下拉框")
        try:
            flag = self.wait_for_selector(".el-time-panel")
            if flag:
                return self.page.locator(".el-time-panel")
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def select_time_conf_by_para_name(self, time_str: str, para_name: str, location=None):
        """
        根据参数名称定位到时间选择模块进行时间选择
        :param time_str: 时间 00:00:00
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"设置参数：【{para_name}】的时间为：{time_str}")
        try:
            if location is None:
                location = self.page
            # 根据参数名称定位到参数模块
            para_location = self.locate_by_para_name(para_name, location)
            # 定位到时间图标并点击
            para_location.locator("//input").click()
            # 定位到时间下拉框
            time_location = self.time_location()
            time_list = time_str.split(":")
            for i in range(len(time_list)):
                time_location.locator(
                    "//div[contains(@class,'el-time-spinner__wrapper')][" + str(i + 1) + "]//ul/li[text()='" +
                    time_list[i] + "']")
            # 点击确定按钮
            self.click_by_role_text("button", "确定", time_location)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def date_range_location(self):
        """
        在整个页面获取时间范围选择框
        :return:
        """
        ui_logger.info(f"在整个页面定位时间范围选择框")
        try:
            flag = self.wait_for_selector(".el-date-range-picker")
            if flag:
                return self.page.locator(".el-date-range-picker")
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def select_date_range_conf_by_para_name(self, date_range: dict, para_name: str, location=None):
        """
        根据参数名称定位到时间范围选择模块进行时间范围选择
        :param date_range: 时间范围
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"设置参数：【{para_name}】的时间范围为：{date_range}")
        try:
            if location is None:
                location = self.page
            # 根据参数名称定位到参数模块
            para_location = self.locate_by_para_name(para_name, location)
            # 定位到时间图标并点击
            para_location.locator(".el-range__icon").click()
            # 定位到时间范围选择框
            date_range_select_location = self.date_range_location()
            # 开始日期
            self.input_by_placeholder("开始日期", date_range['开始日期'], date_range_select_location)
            # 开始时间
            self.input_by_placeholder("开始时间", date_range['开始时间'], date_range_select_location)
            # 结束日期
            self.input_by_placeholder("结束日期", date_range['结束日期'], date_range_select_location)
            # 结束时间
            self.input_by_placeholder("结束时间", date_range['结束时间'], date_range_select_location)
            # 点击确定按钮
            footer_location = date_range_select_location.locator(".el-picker-panel__footer")
            self.click_by_role_text("button", "确定", footer_location)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 输入框相关操作 ----------------
    def input_locator_by_para(self, input_value: str, para_name: str, location=None):
        """
        根据参数名称定位到参数的输入框进行数据输入
        :param input_value: 输入值
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"在参数：【{para_name}】的输入框中输入：{input_value}")
        try:
            if location is None:
                location = self.page
            # 根据参数名称定位到参数输入框
            # para_input_location = location.locator("form div label", has_text=re.compile("^" + para_name + ".*：$")).locator(
            #     "..//input")
            # 根据参数名称定位到参数模块
            para_location = self.locate_by_para_name(para_name, location)
            # 定位到参数输入框
            para_input_location = para_location.locator("//input")
            # 清空输入框
            para_input_location.clear()
            # 输入值
            para_input_location.fill(input_value)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def textarea_locator_by_para(self, textarea_value: str, para_name: str, location=None):
        """
        根据参数名称定位到参数的输入框进行数据输入
        :param textarea_value: 文本值
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        if location is None:
            location = self.page
        # 根据参数名称定位到参数文本框
        para_textarea_location = location.locator("form div label",
                                                  has_text=re.compile("^" + para_name + ".*：$")).locator(
            "..//textarea")
        # 清空文本框
        para_textarea_location.clear()
        # 输入值
        para_textarea_location.fill(textarea_value)
        ui_logger.info(f"在参数：【{para_name}】的文本框中输入：{textarea_value}")

    def input_by_placeholder(self, placeholder: str, value: str, location=None):
        """
        通过输入框的placeholder定位输入框，并输入值
        :param placeholder: 输入框的placeholder
        :param value: 输入值
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"输入框：{placeholder}，输入值：{value}")
        if location is None:
            location = self.page
        elem = location.get_by_placeholder(placeholder)
        elem.clear()  # 清空输入框
        elem.fill(value)  # 输入值

    # ---------------- 下拉框相关操作 ----------------
    def dropdown_locator_by_para(self, select_value: str, para_name: str, location=None):
        """
        根据参数名称定位到参数的下拉框进行数据选择
        :param select_value: 选择值
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"在参数：【{para_name}】的下拉框中选择：{select_value}")
        try:
            if location is None:
                location = self.page
            # # 根据参数名称定位到参数下拉按钮
            # para_dropdown_location = location.locator("form div label",
            #                                           has_text=re.compile("^" + para_name + ".*：$")).locator(
            #     "..//i")      # 部分下拉按钮跟清空按钮放在一块，点击会清空
            # # 根据参数名称定位到参数输入框
            # para_dropdown_location = location.locator("form div label",
            #                                           has_text=re.compile("^" + para_name + ".*：$")).locator(
            #     "..//input")   # 查询参数输入模块，存在两个input
            # 根据参数名称定位到参数输入框
            para_dropdown_location = location.locator("form div label",
                                                      has_text=re.compile("^" + para_name + ".*：$")).locator(
                "..//input").nth(0)
            # 点击下拉按钮/输入框
            para_dropdown_location.click()
            # # 在整个页面获取下拉框
            # dropdown_locators = self.page.locator(".el-select-dropdown.el-popper").all()
            # dropdown_locator = None
            # for i in dropdown_locators:
            #     if i.is_visible():
            #         dropdown_locator = i
            #         break
            # # 在下拉框中选择指定值
            # self.page.wait_for_timeout(100)
            # dropdown_locator.locator('//span[text()="' + select_value + '"]').click()
            self.dropdown_check_value(select_value)
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def dropdown_location(self):
        """
        在整个页面获取下拉框
        :return:
        """
        ui_logger.info(f"在整个页面定位下拉框")
        try:
            self.page.wait_for_timeout(200)
            dropdown_locator = None
            i = 0
            while i < 5:  # 5秒内没有定位到可见的下拉框，返回None
                # 在整个页面获取下拉框
                dropdown_locators = self.page.locator(".el-select-dropdown.el-popper").all()
                for i in dropdown_locators:
                    if i.is_visible():
                        dropdown_locator = i
                        break
                if dropdown_locator:
                    break
                else:
                    self.page.wait_for_timeout(1000)
            return dropdown_locator
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def dropdown_check_value(self, check_value):
        """
        在下拉框中勾选值
        :param check_value: 需要选择的值，str or list
        :return:
        """
        ui_logger.info(f"在下拉框中勾选值：{check_value}")
        try:
            # 定位到下拉框
            dropdown_locator = self.dropdown_location()
            # ui_logger.info(dropdown_locator.inner_html())
            # 在下拉框中勾选值
            if type(check_value) == str:
                check_value = [check_value]
            for i in check_value:
                dropdown_locator.locator('//span[text()="' + i + '"]').click()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def dropdown_checkbox_group_check_value(self, check_value):
        """
        在下拉框(下拉框中的值为checkbox)中勾选值
        :param check_value: 需要选择的值，str or list
        :return:
        """
        ui_logger.info(f"在下拉框中勾选值：{check_value}")
        try:
            # 定位到下拉框
            dropdown_locator = self.dropdown_location()
            if check_value == "全选":
                dropdown_locator.locator("//div[@role='group']/preceding-sibling::*[1]/label").check()
            else:
                # 在下拉框中勾选值
                if type(check_value) == str:
                    check_value = [check_value]
                checkbox_group = dropdown_locator.locator("[role='group'] > label").all()
                # 遍历lable,根据checked_value勾选、取消勾选
                for checkbox in checkbox_group:
                    if checkbox.inner_text() in check_value:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 选择框/选择按钮相关操作 ----------------
    def checkbox_switch_conf_by_para_name(self, ischecked: bool, para_name: str, location=None):
        """
        根据参数名称定位到参数后的勾选框，根据传入的值确定是否勾选
        :param ischecked: 是否勾选
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"参数：【{para_name}】的勾选框是否选择：{ischecked}")
        try:
            if location is None:
                location = self.page
            # 根据参数名称定位到参数模块
            para_location = self.locate_by_para_name(para_name, location)
            # 定位到checkbox
            checkbox = para_location.locator("[role='switch']")
            # 根据传参确定是否选中
            if ischecked:
                checkbox.check()
            else:
                checkbox.uncheck()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def checkbox_group_conf_by_para_name(self, checked_value: list, para_name: str, location=None):
        """
        根据参数名称定位到参数后的所有勾选框，根据传入的值勾选对应的项
        :param checked_value: 需要勾选的值列表
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"参数：【{para_name}】勾选值：{checked_value}")
        try:
            if location is None:
                location = self.page
            # 根据参数名称定位到参数模块
            para_location = self.locate_by_para_name(para_name, location)
            # 定位到checkbox-group
            checkbox_group = para_location.locator("[role='group'] > label").all()
            # 遍历lable,根据checked_value勾选、取消勾选
            for checkbox in checkbox_group:
                if checkbox.inner_text() in checked_value:
                    checkbox.check()
                else:
                    checkbox.uncheck()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def radio_locator_by_para(self, check_value: str, para_name: str, location=None):
        """
        根据参数名称定位到参数的点选模块进行数据点选
        :param check_value: 点选值
        :param para_name: 参数名称
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        ui_logger.info(f"在参数：【{para_name}】的点选模块选择：{check_value}")
        if location is None:
            location = self.page
        # 根据参数名称定位到radiogroup
        para_radio_location = location.locator("form div label", has_text=re.compile("^" + para_name + ".*：$")).locator(
            '..//div[@role="radiogroup"]')
        # ui_logger.info(para_radio_location.inner_html())
        # 点选参数
        para_radio_location.locator('//span[text()="' + check_value + '"]/..').check()
        # para_radio_location.locator("//input[@value='" + check_value + "']/..").check()

    def check_radio(self, name: str):
        """
        根据文本内容选择radio框
        :param name:
        :return:
        """
        self.page.get_by_role(role="radio", name=name).check()
        ui_logger.info(f"选择radio框：{name}")

    # ---------------- 按钮相关操作 ----------------
    def click_button_repre_by_icon(self, title):
        """
        点击按钮(按钮前端显示为图标)
        :param title: 按钮title属性
        :return:
        """
        pass

    # ---------------- 点击相关操作 ----------------
    def click_by_role_text(self, role, name: str, location=None):
        """
        通过role属性和文本点击元素
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :param role: 元素的role属性
        :param name: 按钮文本
        :return:
        """
        # self.page.get_by_role(role, name=name).click()
        ui_logger.info(f"点击{role}：{name}")
        try:
            if location is None:
                location = self.page
            location.get_by_role(role, name=name).click()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- 文件上传相关操作 ----------------
    def upload_file(self, location, files):
        """
        上传文件
        :param location: 上传
        :param files:
        :return:
        """
        ui_logger.info(f"在元素：【{location}】中上传文件：{files}")
        try:
            # 定位到文件上传的input元素
            input_element = self.page.locator(location)
            # 上传文件
            input_element.set_input_files(os.path.join(FILES_DIR, files))
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # ---------------- table相关操作 ----------------
    def table_header(self):
        """
        获取列表表头数据，返回列表
        :return:
        """
        ui_logger.info(f"获取列表表头")
        try:
            return self.page.locator(".el-table__header-wrapper th").all_inner_texts()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def table_all_row_data(self):
        """
        获取列表中所有行的数据
        :return: list
        """
        ui_logger.info(f"获取列表全部数据")
        try:
            row_datas = []
            # 获取表头
            header_list = self.table_header()
            ui_logger.debug(f"header_list：{header_list}")
            # 获取表格数据
            all_row = self.page.locator(".el-table__body-wrapper .el-table__row ").all()
            for row in all_row:
                row_datas.append(dict(zip(header_list, row.locator("xpath=/td").all_inner_texts())))
            ui_logger.debug(f"row_datas：{row_datas}")
            return row_datas
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def table_all_row_td(self, td_nu):
        """
        获取列表中的某列数据
        :param td_nu: 第几列
        :return: list
        """
        ui_logger.info(f"获取列表模块第{td_nu}列的所有值")
        try:
            # return self.page.locator(
            #     "//div[contains(@class,'el-table__body-wrapper')]//tr[@class='el-table__row']/td[1]").all_inner_texts()
            return self.page.locator(
                "//div[contains(@class,'el-table__body-wrapper')]//tr[@class='el-table__row']/td[" + str(
                    td_nu) + "]").all_inner_texts()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    # def table_row(self, td_nu, line_uniq_iden: str):
    #     """
    #     根据行唯一标识定位到具体的行
    #     :param td_nu: 第几列
    #     :param line_uniq_iden: 行唯一标识
    #     :return:
    #     """
    #     ui_logger.info(f"根据第{td_nu}列唯一标识{line_uniq_iden}定位到具体的行")
    #     try:
    #         # 根据唯一标识定位到当前行
    #         # return self.page.locator('//tr[@class="el-table__row"]/td[1]//span[normalize-space(text())="' + line_uniq_iden + '"]/../../../..')
    #         return self.page.locator(
    #             '//div[contains(@class,"el-table__body-wrapper")]//tr[@class="el-table__row"]/td["' + str(
    #                 td_nu) + '"]//span[normalize-space(text())="' + line_uniq_iden + '"]/../../../..')
    #     except Exception as e:
    #         ExceptionHandle().handle_exception(e)
    def table_row(self, line_uniq_iden: str, module='el-table__body-wrapper', table_type=1):
        """
        根据行唯一标识定位到具体的行
        :param line_uniq_iden: 行唯一标识
        :param module: 定位模块，el-table__header-wrapper, el-table__body-wrapper, el-table__fixed, el-table__fixed-right
        :param table_type: 表格类型，1: 所有页面的显示列表  2: 邮箱配置、系统参数配置等页面的参数列表
        :return:
        """
        ui_logger.info(f"在【{module}】模块根据行唯一标识{line_uniq_iden}定位到具体的行")
        try:
            module_location = self.page.locator('//div[contains(@class,"' + module + '")]')  # 定位到具体的模块
            if table_type == 1:  # 标准数据列表
                td_location = module_location.locator(
                    '//tr[@class="el-table__row"]//span[normalize-space(text())="' + line_uniq_iden + '"]/../../..')
            elif table_type == 2:
                td_location = module_location.locator(
                    '//tr[@class="el-table__row"]//span[normalize-space(text())="' + line_uniq_iden + '"]/../../../..')
            else:
                ui_logger.error(f'不支持该表格类型：{table_type}')
                raise Exception('不支持该表格类型')
            return td_location
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def table_row_check(self, line_uniq_iden: str):
        """
        根据行唯一标识勾选行
        :param line_uniq_iden: 行唯一标识
        :return:
        """
        ui_logger.info(f"根据行唯一标识{line_uniq_iden}勾选行")
        try:
            table_location = self.table_row(line_uniq_iden, "el-table__fixed")  # 定位到具体的行
            table_location.locator("xpath=//td[1]//label").check()
        except Exception as e:
            ExceptionHandle().handle_exception(e)

    def button_operate_with_line(self, line_uniq_iden: str, operate: str, location=None):
        """
        根据行唯一标识，定位到具体的行的操作模块，点击具体的操作按钮
        :param line_uniq_iden: 行唯一标识
        :param operate: 操作
        :param location: 定位器，默认为None，从整个页面定位，当传入值时，在相对模块进行定位
        :return:
        """
        if location is None:
            location = self.page
        location.locator(
            '//div[@class="el-table__fixed-right"]//span[normalize-space(text())="' + line_uniq_iden + '"]/../../..//button[@title="' + operate + '"]').click()
        ui_logger.info(f"选择数据行：{line_uniq_iden}，点击操作：{operate}")

    # ---------------- 断言相关操作 ----------------
    def have_text(self, locator: str, text: str):
        """
        验证元素是否具有指定的文本内容
        :param locator: 元素定位器
        :param text: 文本内容
        :return:
        """
        ui_logger.info(f"断言：元素：{locator} 具有文本：{text}")
        expect(self.page.locator(locator)).to_have_text(text)

    def location_hover_have_text(self, text: str, location):
        """
        鼠标悬浮在元素上，校验提示信息
        :param location: 定位
        :param text: 预期提示信息
        :return:
        """
        ui_logger.info(f"鼠标悬浮在元素：{location}上，校验提示信息是否为：{text}")
        try:
            # 鼠标悬浮
            location.hover()
            # 获取鼠标悬浮显示模块
            hover_location = self.page.locator("//div[@role='tooltip'][@aria-hidden='false']")
            # 鼠标悬浮显示信息
            hover_text = hover_location.inner_text()
            ui_logger.info(f"鼠标悬浮显示信息：{hover_text}")
            assert hover_text == text
        except Exception as e:
            ExceptionHandle().handle_exception(e, "assert")
