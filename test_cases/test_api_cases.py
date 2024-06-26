# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_api_cases.py
@IDE: PyCharm
@time: 2023-06-04 18:53
@description: 执行用例
"""
from common.logger_handle import api_logger
import pytest
from config import *
from common import readcase
from common import runcase
from common.allure_handle import api_allure_display
from common.basefunc import config_dict


class TestCases:
    """
    用例执行
    """
    # 执行基础初始化用例集
    @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_cases([CASE_DIR + '/base'], 'yaml'))
    def test_basecases(self, case, casedata):
        api_allure_display(casedata)
        api_logger.info("==========执行用例START：%s==========" % case)
        runcase.RunCase().excute_case(casedata)
        api_logger.info("==========执行用例END：%s==========" % case)

    # 执行业务用例集
    @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_cases([CASE_DIR + '/' + i for i in config_dict['casedata_path']] if config_dict['casedata_path'] else [CASE_DIR], 'yaml', [CASE_DIR + '/extract.yaml', CASE_DIR + '/base']))
    def test_businesscases(self, case, casedata):
        api_allure_display(casedata)
        api_logger.info("==========执行用例START：%s==========" % case)
        runcase.RunCase().excute_case(casedata)
        api_logger.info("==========执行用例END：%s==========" % case)


