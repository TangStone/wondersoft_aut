# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: case_ceshi.py
@IDE: PyCharm
@time: 2023-07-14 15:24
@description: 接口自测
"""
from common.basefunc import config_dict
from config import *
from common.readcase import ReadCase
from common.runcase import RunCase
from utils.log_utils.logger_handle import api_logger,ui_logger
from common import handleyaml
from requests.packages import urllib3
urllib3.disable_warnings()

def api_ceshi(api_path, api, api_caseid):
    """
    # 单接口测试
    :param api_path: 接口路径
    :param api: 接口
    :param api_caseid: 接口数据
    :return:
    """
    # 获取接口用例数据
    api_casedata = ReadCase().get_api_casedata(api_path, api, api_caseid)
    # 执行接口用例
    RunCase().excute_apicase(api, api_casedata)

def case_ceshi(casepath, case):
    """
    单用例测试
    :param casepath: 用例路径
    :param case: 用例
    :return:
    """
    file_data = handleyaml.YamlHandle(casepath).read_yaml()
    case_data = file_data[case]
    # 执行用例
    RunCase().excute_case(case_data)


if __name__ == '__main__':

    # 登录
    api_path = API_DIR + '/bms/login/login.yaml'  # 接口用例路径
    api = 'login'  # 接口用例
    api_caseid = 'login_01'  # 接口用例id
    api_ceshi(api_path, api, api_caseid)

    # # 单接口测试
    api_path = API_DIR + '/bms/datadictionary/datadictionary_analysisDicExcel.yaml'  # 接口用例路径
    api = 'datadictionary_analysisDicExcel'  # 接口用例
    api_caseid = 'datadictionary_analysisDicExcel_01'  # 接口用例id
    api_ceshi(api_path, api, api_caseid)

    # # 单用例测试
    # casepath = CASE_DIR + '/ndlp/send_email.yaml'  # 用例路径
    # case = 'send_email'
    # case_ceshi(casepath, case)
