# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: readcase.py
@IDE: PyCharm
@time: 2023-06-04 18:07
@description: 处理用例数据
"""
import collections

from config import *
from common import handleyaml
from common import handledict

all_case = collections.OrderedDict()

class ReadCase:
    """
    获取用例数据
    """

    def get_case_data(self, caseid, casepath):
        """
        获取用例数据
        :param caseid: 用例id
        :param casepath: 用例路径
        :return: 用例信息
        """
        yaml_data = handleyaml.YamlHandle(casepath).read_yaml()

        casedata = yaml_data[caseid]

        return casedata


    def get_case_dict(self, casepath):
        """
        获取用例数据
        :param casepath: 用例路径
        :return: case_dict   {caseid: casedata}
        """
        yaml_data = handleyaml.YamlHandle(casepath).read_yaml()

        if isinstance(yaml_data, list):
            case_dict = collections.OrderedDict()
            for api in yaml_data:
                case_info = api.pop('case_info')  # 接口基本信息
                case_data = api.pop('case_data')  # 用例信息
                case_info = handledict.dict_update(api, case_info)
                if isinstance(case_data, dict):
                    for caseid, casedata in case_data.items():
                        casedata = handledict.dict_update(casedata, case_info)   #用例基础信息与用例数据合并
                        casedata['caseid'] = caseid   #在用例信息中添加用例id
                        case_dict[caseid] = casedata
                else:
                    raise Exception(api['story'] + '用例case_data模块编写有误，非字典格式！')
            return case_dict
        else:
            raise Exception(casepath + 'yaml文件编写有误，非列表格式！')

    def get_api_casedata(self, api_path, api, api_caseid):
        """
        获取接口用例
        :param api_path: 接口路径
        :param api: 接口id
        :param api_caseid: 接口用例id
        :return: 接口用例
        """
        # 读取yaml文件
        yaml_data = handleyaml.YamlHandle(api_path).read_yaml()
        if isinstance(yaml_data, dict):
            api_info = yaml_data[api]['ApiInfo']  #接口基本信息
            api_data = yaml_data[api]['ApiData'][api_caseid]  #接口数据
            api_casedata = handledict.dict_update(api_info, api_data)
            return api_casedata
        else:
            raise Exception(api_path + 'yaml文件编写有误，非json格式！')

    def get_apicase_list(self, casedata):
        """
        根据用例信息获取测试步骤中的接口用例列表
        :param casedata: 测试用例数据
        :return:
        """
        api_case_list = []
        step_list = casedata['steps']
        for step in step_list:
            if 'api_path' in step.keys():    #调用接口用例
                if type(step['data']) == list:
                    for api_data in step['data']:
                        tem_step = step.copy()
                        tem_step['data'] = api_data
                        api_case_list.append(tem_step)
                else:
                    api_case_list.append(step)
            elif 'case_path' in step.keys():    #引用其它用例
                case_path = CASE_DIR + step['case_path']
                case_id = step['case']
                case_data = self.get_case_data(case_id, case_path)
                api_case_list += self.get_apicase_list(case_data)
            elif 'script_path' in step.keys():   #调用脚本
                api_case_list.append(step)
            else:
                raise Exception('用例步骤编写有误！步骤：' + step + '非接口用例或引用其它用例！')
        return api_case_list

    def get_case(self, file_pathlist):
        """
        获取yaml文件中的所有用例
        :param file_pathlist: yaml文件路径列表
        :return:
        """
        case_list = []
        if file_pathlist:
            for file_path in file_pathlist:
                file_data = handleyaml.YamlHandle(file_path).read_yaml()
                for case, casedata in file_data.items():
                    case_list.append((case, casedata))
        return case_list

    def get_yaml_case(self, file_path):
        """
        获取yaml文件中的所有用例
        :param file_path: yaml文件路径
        :return:
        """
        case_list = []
        if file_path:
            file_data = handleyaml.YamlHandle(file_path).read_yaml()
            for case, casedata in file_data.items():
                case_list.append((case, casedata))
        return case_list

    def get_cases(self, path_list, filetype, exclude=[]):
        """
        获取测试用例
        :param path_list: 文件夹路/文件路径列表
        :param filetype: 文件类型
        :param exclude: 排除目录/文件列表
        :return:
        """
        if isinstance(path_list, list):
            for path in path_list:
                if os.path.isdir(path):  # 文件夹
                    for root, dirs, files in os.walk(path):
                        if root.replace('\\', '/') in exclude:  # 排除目录
                            continue
                        if files:
                            for file in files:
                                if root.replace('\\', '/') + '/' + file in exclude:  # 排除目录
                                    continue
                                if filetype in file:
                                    case_list = self.get_yaml_case(root + '/' + file)  # 获取yaml文件中的所有用例
                                    for i in case_list:
                                        yield i
                else:  # 文件
                    if path in exclude:  # 排除文件
                        continue
                    if filetype in path:
                        case_list = self.get_yaml_case(path)  # 获取yaml文件中的所有用例
                        for i in case_list:
                            yield i
