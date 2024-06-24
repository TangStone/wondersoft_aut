# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: relevancecase.py
@IDE: PyCharm
@time: 2023-06-04 20:10
@description: 关联用例
"""
import logging

import allure, jsonpath

from config import *
from common import readcase
from common import runcase

class Relevance:
    """
    关联信息
    """

    def get_relevance_data(self, relevance):
        """
        获取依赖参数值
        :param relevance:
        :return:
        """
        relevance_dict = {}
        if relevance:
            with allure.step("执行关联接口"):
                for rele_case in relevance:
                    caseid = rele_case['caseid']  # 关联用例id

                    #关联用例信息
                    # case_data = readcase.ReadCase().get_case_data(caseid, readcase.all_case[caseid]['casepath'])
                    case_data = readcase.ReadCase().get_case_dict(readcase.all_case[caseid])[caseid]


                    # 发送请求
                    try:
                        case_send_data, recv_data = runcase.excute_case(case_data)
                    except Exception as e:
                        raise Exception("关联用例：" + caseid + '执行失败，' + str(e))

                    if 'response' in rele_case.keys():
                        for param in rele_case['response']:
                            value = jsonpath.jsonpath(recv_data, param['value'])
                            name = param['name']
                            if value:
                                # relevance_dict[name] = value[0]
                                relevance_dict[name] = value
                            else:
                                raise Exception("关联参数：" + name + "获取失败，请检查用例！")
                    elif 'request' in rele_case.keys():
                        for param in rele_case['request']:
                            value = jsonpath.jsonpath(case_send_data, param['value'])
                            name = param['name']
                            if value:
                                # relevance_dict[name] = value[0]
                                relevance_dict[name] = value
                            else:
                                raise Exception("关联参数：" + name + "获取失败，请检查用例！")
        return relevance_dict
