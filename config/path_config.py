# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: path_config.py
@IDE: PyCharm
@time: 2024-03-27 16:20
@description: 项目相关路径
"""

# 标准库导入
import os

# ------------------------------------ 项目相关路径 ----------------------------------------------------#
# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "logs")


# 报告路径
REPORT_DIR = os.path.join(BASE_DIR, "report")
# Allure报告，测试结果集目录
ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, "allure_results")
# Allure报告，HTML测试报告目录
ALLURE_HTML_DIR = os.path.join(REPORT_DIR, "allure_html")

# 第三方库目录
LIB_DIR = os.path.join(BASE_DIR, "lib")

# 文件目录
FILES_DIR = os.path.join(BASE_DIR, "files")


# 获取主目录路径
ROOT_DIR = os.path.realpath(__file__).split('config')[0].replace('\\', '/')

# 中间件参数传递文件路径
EXTRACT_DIR = ROOT_DIR + 'test_cases/extract.yaml'

# 所有用例caseid文件
# CASE_DIR = ROOT_DIR + 'bms/case.yaml'

# 文件路径
FILE_DIR = ROOT_DIR + 'files'

# 接口，接口数据文件路径
API_DIR = ROOT_DIR + 'ApiData'

# 测试用例路径
CASE_DIR = ROOT_DIR + 'test_cases'

# 证书文件路径
CERT_DIR = ROOT_DIR + 'certs'

# 自定义脚本参数数据路径
SCRIPT_DATA_DIR = ROOT_DIR + 'scripts/data'


