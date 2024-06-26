# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: user_sync_page.py
@IDE: PyCharm
@time: 2024-04-03 10:35
@description: 用户同步页面操作封装
"""
# 标准库导入
# 第三方库导入
import allure
from common.logger_handle import ui_logger
# 本地模块导入
from common.exception_handle import ExceptionHandle
from common.base_page import BasePage
from pages import common_page


class UseSyncPage(BasePage):
    """
    用户同步页面操作封装
    """
    @allure.step("根据查询条件查询数据源配置，查询条件{query_conditions}")
    def search_datasource(self, query_conditions: dict):
        ui_logger.info("………………………………数据源配置查询start………………………………")
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
        ui_logger.info("………………………………数据源配置查询end………………………………")

    # @allure.step("新增数据源配置：{datasource_info}")
    # def add_datasource(self, datasource_info):
    #     ui_logger.info("………………………………新增数据源配置start………………………………")
    #     try:
    #
    #     except Exception as e:
    #         ExceptionHandle().handle_exception(e)
    #     ui_logger.info("………………………………新增数据源配置end………………………………")

    @allure.step("删除数据源配置：{datasource_name}")
    def delete_datasource(self, datasource_name):
        ui_logger.info("………………………………删除数据源配置start………………………………")
        try:
            ui_logger.info(f"删除数据源配置：{datasource_name}")
            self.search_datasource({"名称": datasource_name})
            datasource_list = self.table_all_row_td(2)  # 获取查询的所有数据源配置
            ui_logger.debug(f"数据源配置查询列表：{datasource_list}")
            self.button_operate_with_line(datasource_name, "删除")  # 点击操作模块的【删除】按钮
            self.wait_for_selector('[role="dialog"][aria-label="提示"]')  # 等待提示框出现
            common_page.CommonPage(self.page).click_button("确定", "提示")  # 点击【提示】页面的【确定】按钮
            common_page.CommonPage(self.page).assert_prompt_information("删除成功")  # 弹出提示框，显示提示信息：删除成功
        except Exception as e:
            ExceptionHandle().handle_exception(e)
        ui_logger.info("………………………………删除数据源配置end………………………………")

    @allure.step("选择数据源类型：{data_source_type}")
    def select_data_source_type(self, data_source_type):
        self.page.get_by_placeholder("请选择类型").click()
        self.page.locator("li").filter(has_text=data_source_type).click()
        self.page.get_by_role("button", name="下一步").click()

    @allure.step("AD域参数配置: {domain_config}")
    def ad_domain_config(self, domain_config):
        # ui_logger.info(f"____AD域参数配置：{domain_config}")

        for para in domain_config:
            if para == "启用加密" or para == "是否增量同步":
                checkbox_state = self.page.get_by_text(f"{para}：").locator('..//div[@aria-checked="true"]').is_visible()
                if checkbox_state != domain_config.get(para):
                    self.page.get_by_text(f"{para}：").locator("..//span").click()
            else:
                self.page.get_by_text(f"{para}：").locator("..//input").fill(domain_config.get(para))

    @allure.step("AD域数据关联")
    def ad_domain_relation(self, domain_relations):
        # ui_logger.info(f"____AD域数据关联：{domain_relations}")
        for para, para_value in domain_relations.items():
            if para_value:
                if type(para_value) == list:
                    # 设置数据源输入方式
                    self.page.get_by_text(f"{para}：").locator("../div").click()
                    for span in self.page.locator("span").get_by_text(para_value[0], exact=True).all():
                        if span.is_visible():
                            span.click()
                            break
                    self.page.get_by_text(f"{para}：").locator("../following-sibling::*[1]//input").clear()
                    self.page.get_by_text(f"{para}：").locator("../following-sibling::*[1]//input").fill(para_value[1])
                elif para == "上级领导人同步关联":
                    self.page.get_by_text(f"{para}：").locator("../div").click()
                    for span in self.page.locator("span").get_by_text(para_value, exact=True).all():
                        if span.is_visible():
                            span.click()
                            break
                else:
                    # 点击出现下拉框
                    self.page.get_by_text(f"{para}：").locator("../following-sibling::*[1]").click()
                    # 点击下拉框中的选项
                    # for span in self.page.locator("span").filter(has_text=domain_relations.get(para)).all():
                    for span in self.page.locator("span").get_by_text(para_value, exact=True).all():
                        if span.is_visible():
                            span.click()
                            break

    @allure.step("设置同步配置参数：{sync_config_param}")
    def set_sync_config(self, sync_config_param):
        # ui_logger.info(f"____同步配置参数：{sync_config_param}")

        # 输入名称
        self.page.get_by_label("新增").get_by_text("名称：").locator("..//input").click()
        self.page.get_by_label("新增").get_by_text("名称：").locator("..//input").fill(sync_config_param.get("名称"))

        # 选择数据源
        self.page.get_by_label("新增").get_by_text("数据源：").locator("..//input").click()
        # self.page.locator("li").filter(has_text=sync_config_param.get("数据源")).click()
        self.page.locator("li").get_by_text(sync_config_param.get("数据源"), exact=True).click()
        self.page.get_by_label("新增").get_by_text("数据源：").click()

        # 选择同步模式
        self.page.get_by_label("新增").get_by_text("同步模式：").locator("..//input").click()
        # self.page.locator("li").filter(has_text=sync_config_param.get("同步模式")).click()
        self.page.locator("li").get_by_text(sync_config_param.get("同步模式"), exact=True).click()

        # 设置任务时间
        task_time_list = sync_config_param.get("任务时间").split(" ")
        time_type_id_dict = {"天": "tab-day", "周": "tab-week", "月": "tab-month"}
        self.page.get_by_label("新增").get_by_placeholder("请选择任务时间").click()
        time_type = task_time_list[0]    # 任务时间类型
        self.page.locator("#" + time_type_id_dict.get(time_type)).click()

        # 天
        if time_type == "天":
            self.page.get_by_placeholder("时间", exact=True).fill(task_time_list[1])
        elif time_type == "周":
            self.page.get_by_label("周").get_by_placeholder("请选择").click()
            self.page.get_by_text(task_time_list[1]).click()
            self.page.get_by_label("周").get_by_placeholder("时间", exact=True).clear()
            self.page.get_by_label("周").get_by_placeholder("时间", exact=True).fill(task_time_list[2])
        elif time_type == "月":
            self.page.get_by_label("月").get_by_placeholder("请选择").click()
            self.page.get_by_text(task_time_list[1]).click()
            self.page.get_by_label("月").get_by_placeholder("时间", exact=True).clear()
            self.page.get_by_label("月").get_by_placeholder("时间", exact=True).fill(task_time_list[2])
        self.page.get_by_text("每" + time_type).click()
        self.page.locator(".cronBox").get_by_role("button", name="确定").click()

        # 设置错误阈值
        self.page.get_by_label("新增").locator("form div").filter(has_text="错误阈值").locator("//input").clear()
        self.page.get_by_label("新增").locator("form div").filter(has_text="错误阈值").locator("//input").fill(sync_config_param.get("错误阈值"))
        # self.page.get_by_label("新增").get_by_text(re.compile(r"^错误阈值")).locator("..//input").clear()
        # self.page.get_by_label("新增").get_by_text(re.compile(r"^错误阈值")).locator("..//input").fill(sync_config_param.get("错误阈值"))

        # 日志保留周期
        self.page.get_by_label("新增").get_by_text("日志保留周期：").locator("..//input").clear()
        self.page.get_by_label("新增").get_by_text("日志保留周期：").locator("..//input").fill(sync_config_param.get("日志保留周期"))

    @allure.step("选择同步配置名称：：{sync_name}")
    def check_sync_name(self, sync_name):
        # 选择同步配置名称
        self.check_radio(sync_name)