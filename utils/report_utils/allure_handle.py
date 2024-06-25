# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: allure_handle.py
@IDE: PyCharm
@time: 2024-03-27 17:44
@description: allure报告处理
"""
# 标准库导入
import os
# 第三方库导入
import allure,json,time
# 本地模块导入
from config.path_config import REPORT_DIR,LIB_DIR


def ui_allure_display(casedata):
    """
    处理allure显示
    :param casedata: 用例信息
    :return:
    """
    # allure.dynamic.epic(casedata['epic'])
    allure.dynamic.feature(casedata['feature_name'])
    # allure.dynamic.story(casedata['story'])
    allure.dynamic.title(casedata['scenario_name'])
    # allure.dynamic.description(casedata['description'])

def api_allure_display(casedata):
    """
    处理allure显示
    :param casedata: 用例信息
    :return:
    """
    allure.dynamic.epic(casedata['epic'])
    allure.dynamic.feature(casedata['feature'])
    allure.dynamic.story(casedata['story'])
    allure.dynamic.title(casedata['name'])
    allure.dynamic.description(casedata['description'])

def generate_allure_report(**kwargs):
    """
    通过allure生成html测试报告
    """
    allure_results_dir = kwargs.get("allure_results")
    allure_report_dir = kwargs.get("allure_report")
    # allure命令
    allure_bin = os.path.join(LIB_DIR, [i for i in os.listdir(LIB_DIR) if i.startswith("allure")][0], "bin")
    allure_path = os.path.join(allure_bin, "allure.bat")
    cmd = f"{allure_path} generate {allure_results_dir} -o {allure_report_dir} --clean"
    os.popen(cmd).read()

class AllureReportData:
    """
    获取allure报告数据
    """

    def __init__(self, report_name):
        self.report_path = REPORT_DIR + '/' + report_name  # allure报告路径

    def get_case_count(self):
        file_name = self.report_path + '/widgets/summary.json'
        with open(file_name, 'r', encoding='utf-8') as file:
            summary_data = json.load(file)
        _case_state = summary_data['statistic']    # 用例状态
        _run_time = summary_data['time']           # 运行时间
        keep_keys = {"passed", "failed", "broken", "skipped", "total"}
        run_case_data = {k: v for k, v in summary_data['statistic'].items() if k in keep_keys}
        # 判断运行用例总数大于0
        if _case_state["total"] > 0:
            # 计算用例成功率
            run_case_data["pass_rate"] = round(
                (_case_state["passed"] + _case_state["skipped"]) / _case_state["total"] * 100, 2
            )
        else:
            # 如果未运行用例，则成功率为 0.0
            run_case_data["pass_rate"] = 0.0
        # 用例执行开始时间
        run_case_data['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_run_time['start']/1000))
        # 用例执行结束时间
        run_case_data['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_run_time['stop']/1000))
        # 用例运行时长
        duration = _run_time['duration'] // 1000
        hour = duration // 3600
        minute = (duration - hour * 3600) // 60
        second = duration - hour * 3600 - minute * 60
        run_case_data['time'] = _run_time if run_case_data['total'] == 0 else f"{hour}时{minute}分{second}秒"
        return run_case_data