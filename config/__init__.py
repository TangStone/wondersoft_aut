#coding=utf-8

"""
@author:  gaojie
@File：__init__.py.py
@IDE: PyCharm
@time: 2023-04-03 14:45
@description:
"""

import os

# 获取主目录路径
ROOT_DIR = os.path.realpath(__file__).split('config')[0].replace('\\', '/')

# 获取配置文件路径
CONFIG_DIR = ROOT_DIR + 'config/config.yml'

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

# 报告路径
REPORT_DIR = ROOT_DIR + 'report'
