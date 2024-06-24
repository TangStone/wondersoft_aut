# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: handleallure.py
@IDE: PyCharm
@time: 2023-06-14 15:54
@description:
"""
import allure, json, time
from config import *

def allure_display(casedata):
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

