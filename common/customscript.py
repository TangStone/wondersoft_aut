# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: customscript.py
@IDE: PyCharm
@time: 2023-09-15 11:40
@description: 执行自定义脚本
"""
from utils.log_utils.logger_handle import api_logger

from common import handleyaml
from config import *

def excute_custom_script(script_data):
    """
    执行自定义脚本
    :param script_data: 自定义脚本相关数据
    :return:
    """
    api_logger.info('-·-·-·-·-·-·-·-·-·-执行自定义脚本 START-·-·-·-·-·-·-·-·-·-')
    # 调用模块
    module = ""    #调用模块
    module_list = script_data['script_path'].split('/')
    for i in module_list:
        if i:
            module += i + '.'
    module = module[:-1]
    # 调用方法
    method = script_data['method']
    # 获取方法参数
    params_path = SCRIPT_DATA_DIR + '/' + script_data['params_path']    #参数路径
    params_id = script_data['params']     #参数id
    yaml_data = handleyaml.YamlHandle(params_path).read_yaml()
    params = yaml_data[params_id]
    param_str = ""
    for key, value in params.items():
        if isinstance(value, str):
            param_str += key + '="' + str(value) + '",'
        else:
            param_str += key + '=' + str(value) + ','
    param_str = param_str[:-1]

    # 重组自定义脚本数据
    run_code = f"""
from scripts.{module} import {method} 
{method}({param_str})
    """

    api_logger.info('执行自定义脚本：' % run_code)
    exec(run_code)
    api_logger.info('-·-·-·-·-·-·-·-·-·-执行自定义脚本 END-·-·-·-·-·-·-·-·-·-')
