# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: regroupdata.py
@IDE: PyCharm
@time: 2023-06-04 20:19
@description: 参数替换
"""
import json
import re, sys, logging, datetime, uuid, random, string, jsonpath
from faker import Faker
from functools import reduce

from config import *
from common import exceptions
from common import encryption
from common import handleyaml
from common import handledict
from common.basefunc import config_dict


class RegroupData:
    """
    参数替换
    """

    def __init__(self, api_casedata, temp_var_dict):
        """
        :param api_casedata: 接口用例信息
        :param temp_var_dict: 临时变量字典
        """
        self.api_casedata = api_casedata  # 接口用例信息
        self.global_var_dict = handleyaml.YamlHandle(EXTRACT_DIR).read_yaml()  # 全局变量字典
        self.temp_var_dict = temp_var_dict  # 临时变量字典
        self.env_var_dict = config_dict  # 环境变量字典
        self.update_dict = {}  # 更新字典
        # logging.info("api_casedata:%s", self.api_casedata)
        # logging.info("global_var_dict:%s", self.global_var_dict)
        # logging.info("temp_var_dict:%s", self.temp_var_dict)
        # logging.info("env_var_dict:%s", self.env_var_dict)

    def is_key_in_nested_dict(self, nested_dict, key):
        """
        判断key是否在字典中
        :param nested_dict: 字典
        :param key: key
        :return:
        """
        if key in nested_dict:
            return True
        return any(self.is_key_in_nested_dict(v, key) for v in nested_dict.values() if isinstance(v, dict))

    @staticmethod
    def get_value_from_path(nested_dict, para_path):
        """
        根据参数路径从字典中取值
        :param nested_dict: 字典
        :param para_path: 参数路径：action.scanRandId_10
        :return:
        """
        try:
            return reduce(lambda d, key: d[key], para_path.split('.'), nested_dict)
        except (KeyError, TypeError):
            return None

    def get_param_value(self, param_path):
        """
        获取参数值
        :param param_path: 取值参数路径
        :return:
        """
        logging.info(f"参数取值，参数路径：{param_path}")
        getvaluedict_list = [self.temp_var_dict, self.global_var_dict, self.env_var_dict,
                             self.api_casedata['request']['data']]
        value = None
        for i in getvaluedict_list:
            if i and self.is_key_in_nested_dict(i, param_path.split('.')[-1]):
                value = self.get_value_from_path(i, param_path)
                if value:
                    return value
        if not value:
            raise Exception("参数取值失败，参数路径：%s" % param_path)

    def get_value(self, param):
        """
        获取参数值，并处理
        :param param:
        :return:
        """
        param_list = param.split(";")  # 拆分取值需求 ${data;update={"realName":"ceshi"}}
        value = self.get_param_value(param_list[0])  # 获取参数值
        if len(param_list) >= 2:
            for pa in param_list[1:]:
                pa_list = pa.split("=")
                if pa_list[0] == 'type':  # 参数类型替换，针对值转换为字符串类型场景
                    if pa_list[1] == 'str':
                        value = str(value)
                elif pa_list[0] == 'update':  # 更新字典中的值
                    logging.info("pa_list[1]:%s", pa_list[1])
                    update_dict = self.update_dict[pa_list[1]]
                    value = handledict.dict_update(value, update_dict)
                else:
                    raise Exception("暂不支持此扩展" + pa)
        return value

    def eval_data(self, param):
        """
        还原数据类型
        :param param: key
        :return:
        """
        param_list = param.split(";")  # 拆分取值需求 ${relevance(fileContent)};path=filelist[0].md5
        value = self.replace_value(param_list[0])
        try:
            # path = None
            if len(param_list) >= 2:
                for pa in param_list[1:]:
                    pa_list = pa.split("=")
                    if pa_list[0] == 'path':  # 获取字典中的特定值
                        path = '$.' + pa_list[1]
                        value = jsonpath.jsonpath(json.loads(value.replace("\\", '/')), path)[0]
                    if pa_list[0] == 'cal':  # 计算
                        value = eval(str(value) + pa_list[1])
            # str_data = eval(value)
            # if path:
            #     str_data = jsonpath.jsonpath(str_data, path)[0]
        except:
            raise Exception("参数取值失败，参数名：%s" % param)
            # str_data = value
        return value

    @staticmethod
    def get_enc_value(param):
        """
        参数加密
        :param param: key
        :return:
        """
        param_list = param.split(';')  # 获取多个配置项
        if len(param_list) >= 2:
            for pa in param_list[1:]:
                pa_list = pa.split("=")
                if pa_list[0] == 'type':  # 获取字典中的特定值
                    if pa_list[1] == 'base64':
                        data = encryption.enc_base64(param_list[0])
                    elif pa_list[1] == 'sha1':
                        data = encryption.enc_sha1(param_list[0])
                    else:
                        raise Exception("暂不支持此种加密方式：" + pa_list[1])
                else:
                    raise Exception("暂不支持此扩展" + pa)
        else:  # 默认使用RSA加密+base64加密
            data = encryption.encryption(param)
        return data

    @staticmethod
    def get_time(param):
        """
        获取时间
        :param str: format='%Y-%m-%d %H:%M:%S'
        :return:
        """
        param_list = param.split(';')  # 获取多个配置项
        time_str = datetime.datetime.now()  # 获取当前时间
        format = None  # 时间格式
        timestamp_num = 13  # 时间戳位数
        for param in param_list:
            pa_list = param.split('=')  # 拆分配置项
            if pa_list[0] == 'format':  # 时间格式
                format = pa_list[1]
            if pa_list[0] == 'tds_num':  # 时间戳位数
                timestamp_num = int(pa_list[1])
            if pa_list[0] == 'cal':  # 时间偏移
                cal_list = pa_list[1].split(',')
                for cal in cal_list:
                    num = int(cal[2:])
                    cal_dict = {'w': 'weeks', 'd': 'days', 'h': 'hours', 'm': 'minutes'}
                    if cal[1] == '+':  # 向后偏移
                        if cal[0] in cal_dict.keys():
                            time_str += datetime.timedelta(**{cal_dict[cal[0]]: num})
                        else:
                            raise Exception("暂不支持此种时间偏移：" + pa_list[1])
                    elif cal[1] == '-':  # 向前偏移
                        if cal[0] in cal_dict.keys():
                            time_str -= datetime.timedelta(**{cal_dict[cal[0]]: num})
                        else:
                            raise Exception("暂不支持此种时间偏移：" + pa_list[1])
        if format:  # 时间格式转换
            time_str = time_str.strftime(format)
        else:  # 不存在时间格式，返回时间戳
            time_str = str(round(time_str.timestamp() * 1000))[0:timestamp_num]
        return time_str

    @staticmethod
    def get_uuid(param):
        """
        获取UUID
        :param param:
        :return:
        """
        return str(uuid.uuid1())

    @staticmethod
    def get_rand_int(param):
        """
        获取随机整数
        :param param: 参数(1,100),取值范围1-100
        :return:
        """
        try:
            param_randint = tuple(map(int, param.split(",")))
            number = random.randint(*param_randint)
            return number
        except:
            raise Exception("随机整数取值参数有误：" + param)

    @staticmethod
    def get_rand_str(param):
        """
        获取随机字符串
        :param param: 字符串长度
        :return:
        """
        try:
            number = int(param)
            str_list = random.sample(string.ascii_letters, number)
            return "".join(str_list)
        except:
            raise Exception("随机字符串取值参数有误：" + param)

    @staticmethod
    def fakedata(param):
        """
        获取随机数据
        :param param: 随机类型
        :return:
        """
        fake = Faker(locale='zh_CN')
        if param == 'name':  # 随机姓名
            return fake.name()
        elif param == 'phone':  # 随机手机号
            return fake.phone_number()
        elif param == 'email':  # 随机邮箱
            return fake.email()
        else:
            raise Exception("暂不支持此种随机类型：" + param)

    @staticmethod
    def get_rand_choice(param):
        """
        获取随机选择
        :param param: 选择列表
        :return:
        """
        choice_list = param.split(",")
        return random.choice(choice_list)

    def regroup_case_data(self):
        """
        重组用例数据
        :return:
        """
        # 若存在updatedata，先重组updatedata
        if 'updatedata' in self.api_casedata['request'].keys():
            sign, rawDict = self.regroup_dict(self.api_casedata['request']['updatedata'])  # 重组updatedata
            if sign == 'success':
                # self.api_casedata['request']['updatedata'] = rawDict  #更新updatedata
                self.update_dict = rawDict
                self.api_casedata['request'].pop('updatedata')  # 删除updatedata
            else:
                return sign, rawDict
        sign, rawDict = self.regroup_dict(self.api_casedata)
        return sign, rawDict

    def regroup_dict(self, rawDict):
        """
        递归重组接口用例数据
        :param rawdict: 用例数据字典
        :return:
        """
        try:
            sign = 'success'  # 标识参数
            if isinstance(rawDict, dict):
                for dict_key in rawDict:  # 遍历字典
                    sign, tem_rawDict = self.regroup_dict(rawDict[dict_key])  # 递归处理
                    if sign == 'success':
                        rawDict[dict_key] = tem_rawDict
                    else:
                        rawDict = tem_rawDict
                        break
            elif isinstance(rawDict, list):
                tem_raw_list = []
                for list_value in rawDict:
                    sign, tem_rawDict = self.regroup_dict(list_value)
                    if sign == 'success':
                        tem_raw_list.append(tem_rawDict)
                    else:
                        rawDict = tem_rawDict
                        break
                if sign == 'success':
                    rawDict = tem_raw_list
            elif isinstance(rawDict, str):
                rawDict = self.replace_value(rawDict)
            else:
                pass
        except:
            # 异常处理
            ex_type, ex_val, ex_stack = sys.exc_info()
            error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
            rawDict = "重组用例数据异常" + str(error_info)
            sign = 'error'
        return sign, rawDict

    def replace_value(self, str_data):
        """
        参数值替换
        :param data_str: 原始字符串
        :return:
        """
        type_methos_1 = {'\$Eval\((.*?)\)': [self.eval_data]  # 格式转换
                         }

        type_method_2 = {'\$GetRandChoice\((.*?)\)': [self.get_rand_choice],  # 随机选择
                         '\$GetRandName\((.*?)\)': [self.fakedata, 'name'],  # 随机姓名
                         '\$GetRandPhone\((.*?)\)': [self.fakedata, 'phone'],  # 随机手机号
                         '\$GetRandEmail\((.*?)\)': [self.fakedata, 'email'],  # 随机邮箱
                         '\$GetRandStr\((.*?)\)': [self.get_rand_str],  # 随机字符串
                         '\$GetRandInt\((.*?)\)': [self.get_rand_int],  # 随机整数
                         '\$GetUuid\((.*?)\)': [self.get_uuid],  # UUID
                         '\$GetTime\((.*?)\)': [self.get_time],  # 时间
                         '\$Enc\((.*?)\)': [self.get_enc_value],  # 加密
                         '\$\{(.*?)\}': [self.get_value],  # 变量替换
                         }

        for expre1, method1 in type_methos_1.items():
            param_list1 = re.findall(expre1, str_data)
            if len(param_list1):
                for param1 in param_list1:
                    value = method1[0](param1)
                    if expre1 == '\$Eval\((.*?)\)':
                        if str_data[0:6] == '$Eval(' and str_data[-1:] == ')':
                            return value
                        else:
                            rep_data = '$Eval(' + param1 + ')'
                            str_data = str_data.replace(rep_data, str(value), 1)
                            return str_data

        for expre, method in type_method_2.items():
            param_list = re.findall(expre, str_data)
            if len(param_list):
                for param in param_list:
                    # 获取参数值
                    if len(method) == 1:
                        value = method[0](param)
                    else:
                        value = method[0](method[1])
                    # 重组表达式
                    expre_ori = expre.replace("(.*?)", param).replace('\\', '')
                    expre_par = expre.replace("(.*?)", param)

                    if expre_ori == str_data:  # 返回原始类型
                        return value
                    if expre == '\$GetTime\((.*?)\)' and '+' in param:  # 日期向后偏移时 +字符转换
                        expre_par = expre_par.replace('+', '\+')
                    pattern = re.compile(expre_par)
                    str_data = re.sub(pattern, str(value), str_data, count=1)

        return str_data

    # def replace_value(self, str_data):
    #     """
    #     参数值替换
    #     :param data_str: 原始字符串
    #     :return:
    #     """
    #     var_list = re.findall(r"\$\{(.*?)\}", str_data)  # 变量替换
    #     eval_list = re.findall(r"\$Eval\((.*?)\)", str_data)  # 格式转换
    #     enc_list = re.findall(r"\$Enc\((.*?)\)", str_data)  # 加密
    #     time_list = re.findall(r"\$GetTime\((.*?)\)", str_data)  # 时间
    #     uuid_list = re.findall(r"\$GetUuid\((.*?)\)", str_data)  # UUID
    #     int_list = re.findall(r"\$GetRandInt\((.*?)\)", str_data)  # 随机整数
    #     str_list = re.findall(r"\$GetRandStr\((.*?)\)", str_data)  # 随机字符串
    #     name_list = re.findall(r"\$GetRandName\((.*?)\)", str_data)  # 随机姓名
    #     phone_list = re.findall(r"\$GetRandPhone\((.*?)\)", str_data)  # 随机手机号
    #     email_list = re.findall(r"\$GetRandEmail\((.*?)\)", str_data)  # 随机邮箱
    #     choice_list = re.findall(r"\$GetRandChoice\((.*?)\)", str_data)  # 随机选择
    #
    #     if len(choice_list):
    #         for i in choice_list:
    #             value = self.get_rand_choice(i)
    #             if '$GetRandChoice(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandChoice\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(name_list):
    #         for i in name_list:
    #             value = self.fakedata('name')
    #             if '$GetRandName(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandName\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(phone_list):
    #         for i in phone_list:
    #             value = self.fakedata('phone')
    #             if '$GetRandPhone(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandPhone\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(email_list):
    #         for i in email_list:
    #             value = self.fakedata('email')
    #             if '$GetRandEmail(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandEmail\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(str_list):
    #         for i in str_list:
    #             value = self.get_rand_str(i)
    #             if '$GetRandStr(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandStr\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(int_list):
    #         for i in int_list:
    #             value = self.get_rand_int(i)
    #             if '$GetRandInt(' + i + ')' == str_data:
    #                 return value
    #             pattern = re.compile(r'\$GetRandInt\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(uuid_list):
    #         for i in uuid_list:
    #             pattern = re.compile(r'\$GetUuid\(' + i + r'\)')
    #             value = self.get_uuid(i)
    #             if '$GetUuid(' + i + ')' == str_data:
    #                 return value
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(eval_list):
    #         for i in eval_list:
    #             value = self.eval_data(i)
    #             if str_data[0:6] == '$Eval(' and str_data[-1:] == ')':  #当前值需要转换类型
    #                 return value
    #             else:  #返回字符串
    #                 rep_data = '$Eval(' + i + ')'
    #                 str_data = str_data.replace(rep_data, str(value), 1)
    #                 return str_data
    #
    #     if var_list:
    #         for var in var_list:
    #             pattern = re.compile(r'\$\{' + var + r'\}')
    #             value = self.get_value(var)
    #             if '${' + var + '}' == str_data:
    #                 return value
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(enc_list):
    #         for i in enc_list:
    #             pattern = re.compile(r'\$Enc\(' + i + r'\)')
    #             value = self.get_enc_value(i)
    #             if '$Enc(' + i + ')' == str_data:
    #                 return value
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(time_list):
    #         for i in time_list:
    #             value = self.get_time(i)
    #             if '$GetTime(' + i + ')' == str_data:
    #                 return value
    #             if '+' in i:   #日期向后偏移时 +字符转换
    #                 i = i.replace('+', '\+')
    #             pattern = re.compile(r'\$GetTime\(' + i + r'\)')
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     return str_data
