# -*- coding: utf-8 -*-

"""
@author: tanglei
@File: basefunc.py
@IDE: PyCharm
@time: 2024-06-21 17:36
@description: 基础处理函数
"""
from config import *
from common import handleyaml
# 第三方库导入
from common.logger_handle import ui_logger
import jsonpath
from urllib.parse import unquote

#config_dict = handleyaml.YamlHandle(CONFIG_DIR).read_yaml()
config_dict = {**ENV_VARS['test'],**BASE_VARS}

def eval_data(data):
    """
    执行一个字符串表达式，并返回其表达式的值
    """
    try:
        if hasattr(eval(data), "__call__"):
            return data
        else:
            return eval(data)
    except Exception as e:
        ui_logger.trace(f"{data} --> 该数据不能被eval\n报错：{e}")
        return data

def clean_dir(path):
    """清空目录下所有文件，保留文件夹"""
    for i in os.listdir(path):
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clean_dir(c_path)
        else:
            os.remove(c_path)
    for i in os.listdir(path):
        dir_path = os.path.join(path, i)
        if os.listdir(dir_path):
            clean_dir(path)
        else:
            os.rmdir(dir_path)

def file_execute_list(path_list, filetype, exclude=[]):
    """
    获取目录列表下所有的文件
    :param path_list: 文件夹路/文件路径列表
    :param filetype: 文件类型
    :param exclude: 排除目录/文件列表
    :return: 文件绝对路径列表
    """
    if isinstance(path_list, list):
        # 获取所有文件路径
        file_path_list = []
        for path in path_list:
            if os.path.isdir(path):   #文件夹
                for root, dirs, files in os.walk(path):
                    if root.replace('\\', '/') in exclude:
                        continue
                    if files:
                        for file in files:
                            if root.replace('\\', '/') + '/' + file in exclude:
                                continue
                            if filetype in file:
                                file_path_list.append(root + '/' + file)
            else:
                if path in exclude:
                    continue
                if filetype in path:
                    file_path_list.append(path)
        return file_path_list


def pre_process():
    """
    执行用例前置处理操作
    :return:
    """
    # 清空临时文件目录
    clean_dir(ALLURE_RESULTS_DIR)
    # 清空报告
    clean_dir(ALLURE_HTML_DIR)
    # 清空中间件文件
    handleyaml.YamlHandle(EXTRACT_DIR).clear_yaml()
    # # 获取用例数据
    # casedata_path = [ BASE_DIR + i for i in config_dict['casedata_path']]
    # readcase.ReadCase().read_case(casedata_path)

def post_process():
    """
    执行用例后置处理操作
    :return:
    """
    # 添加environment.properties到allure目录
    # project_name = config_dict['project_name']
    baseurl = config_dict['base_url']
    environment = 'BaseURL=' + baseurl + '\n'
    with open(ALLURE_RESULTS_DIR + '/environment.properties', 'w', encoding='ascii', errors='ignore') as file_obj:
        file_obj.write(environment)


def create_handle_response(url, var_list, jsonpath_list):
    """
       监听url操作,参数var_list和jsonpath_list具有强关联性，一一对应
       :param url: 需要监听的url
       :param var_list: 自定义的全局变量列表，eg [displayNmae,sid]
       :param jsonpath_list:需要传递给全局变量的jsonpath，eg [$.data.list[0].displayName,$.data.list[0].sid]
       :return: 注册监听的函数名
    """
    initial_values = {}  # 外部字典来保存初始值
    def handle_response(response):
        if url in unquote(response.url):  # 根据具体的登录请求 URL 进行判断
            try:
                content_type = response.headers.get("content-type", "")
                ui_logger.info("Content-Type: %s" % content_type)
                # 检查响应的内容类型是否为 JSON
                if "application/json" in content_type:
                    try:
                        response_body = response.json()
                    except Exception as e:
                        ui_logger.error("Failed to parse JSON response: %s" % e)
                        ui_logger.error("Response text: %s" % response.text())
                    for var, json_path in zip(var_list, jsonpath_list):
                        if var not in initial_values:
                            # 只在第一次遇到该变量时进行赋值
                            initial_values[var] = jsonpath.jsonpath(response_body, json_path)[0]
                            extract_value = {var: initial_values[var]}
                            handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()
                else:
                    ui_logger.error("Response is not in JSON format")
            except Exception as e:
                ui_logger.error("Error handling response: %s" % e)
    return handle_response