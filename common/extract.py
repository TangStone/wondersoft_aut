# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: extract.py
@IDE: PyCharm
@time: 2023-06-08 15:59
@description: 处理参数传递
"""
import jsonpath

from config import *
from common import handleyaml



def handle_extarct(extract, recv_data):
    """
    处理中间参数
    :param extract: 提取参数字典
    :param recv_data: 接口返回值
    :param send_data: 接口请求数据
    :return:
    """
    extract_value = {}    #全局变量字典
    temp_value = {}    #临时变量字典

    for para in extract:
        # 获取参数值
        js_value = jsonpath.jsonpath(recv_data, para['jsonpath'])
        if js_value:
            if '*' not in para['jsonpath']:
                js_value = js_value[0]
            if 'type' in para.keys():
                if para['type'] == 'global':   #参数传递到全局变量
                    extract_value[para['name']] = js_value
                else:    #参数传递到临时变量
                    temp_value[para['name']] = js_value
            else:  # 不填写默认为临时变量
                temp_value[para['name']] = js_value
        else:
            raise Exception("变量提取失败！" + para)
    handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()
    return temp_value
