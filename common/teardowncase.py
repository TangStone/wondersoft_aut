# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: teardowncase.py
@IDE: PyCharm
@time: 2023-06-04 21:38
@description: 后置用例处理
"""
import allure

from common import readcase
from common import runcase

def case_teardown(case_data):
    """
    后置请求处理
    :param case_data: 用例信息
    :return:
    """
    if 'teardown' in case_data.keys():
        for teardown_case in case_data['teardown']:
            caseid = teardown_case['caseid']  # 关联用例id

            # 读取用例信息
            # case_data = readcase.ReadCase().get_case_data(caseid, readcase.all_case[caseid]['casepath'])
            case_data = readcase.ReadCase().get_case_dict(readcase.all_case[caseid])[caseid]

            with allure.step("执行后置接口"):
                case_send_data, recv_data = runcase.excute_case(case_data)