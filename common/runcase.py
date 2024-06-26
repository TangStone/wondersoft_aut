# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: runcase.py
@IDE: PyCharm
@time: 2023-06-04 19:41
@description:
"""
from common.logger_handle import api_logger
import allure, requests, json
import time

from requests_toolbelt import MultipartEncoder

from config import *
from common import readcase
from common import handleyaml
from common import regroupdata
from common import checkresult
from common import extract
from common import database
from common import handledict
from common import customscript
from common.basefunc import config_dict

class RunCase:
    """
    执行测试用例
    """

    def __init__(self):
        self.temp_var_dict = {}  # 临时变量字典

    def excute_case(self, casedata):
        """
        执行测试用例
        :param casedata: 用例信息
        :return:
        """
        info = "'-·-·-·-·-·-·-·-·-·-执行用例 START:-·-·-·-·-·-·-·-·-·-" + f"{casedata['name']}\n"
        api_logger.info(info)
        if 'steps' in casedata.keys():
            # 获取测试步骤中的接口用例列表
            get_apicase_list = readcase.ReadCase().get_apicase_list(casedata)
            # 遍历接口用例列表
            for apicase in get_apicase_list:
                # 判断是否存在等待时间
                if 'sleep' in apicase.keys():
                    api_logger.info("========等待时间：%s秒" % apicase['sleep'])
                    time.sleep(apicase['sleep'])
                if 'script_path' in apicase.keys():  # 调用脚本
                    customscript.excute_custom_script(apicase)
                else:   # 调用接口
                    api_path = API_DIR + apicase['api_path']  # 接口用例路径
                    api = apicase['api']  # 接口用例
                    api_caseid = apicase['data']  # 接口用例id
                    # 获取接口用例数据
                    api_casedata = readcase.ReadCase().get_api_casedata(api_path, api, api_caseid)
                    # 执行接口用例
                    with allure.step(api_casedata['name']):
                        self.excute_apicase(api, api_casedata)
        api_logger.info('-·-·-·-·-·-·-·-·-·-执行用例 END：%s-·-·-·-·-·-·-·-·-·-' % casedata['name'])

    def excute_apicase(self, api, api_casedata):
        """
        执行接口用例
        :param api: 接口
        :param api_casedata: 接口用例数据
        :return:
        """
        api_logger.info('-·-·-·-·-·-·-·-·-·-执行接口 START：%s-·-·-·-·-·-·-·-·-·-' % api_casedata['name'])
        # 校验用例格式
        flag, msg = handleyaml.standard_yaml(api_casedata)
        if flag:  # 用例格式无误
            # 判断是否存在前置操作
            if 'preProcessors' in api_casedata.keys():
                self.apicase_processors(api_casedata['preProcessors'])

            # 重组接口用例数据
            sign, api_casedata = regroupdata.RegroupData(api_casedata, self.temp_var_dict).regroup_case_data()
            if sign:  # 重组数据成功
                api_logger.info("重组后的用例信息：%s" % api_casedata)
                # 发送请求
                recv_data, recv_code = send_request(api_casedata)
                # 判断是否存在后置操作
                if 'postProcessors' in api_casedata.keys():
                    self.apicase_processors(api_casedata['postProcessors'], recv_data, recv_code)

                api_logger.info('-·-·-·-·-·-·-·-·-·-执行接口 END：%s-·-·-·-·-·-·-·-·-·-' % api_casedata['name'])
                return api_casedata, recv_data
            else:
                raise Exception(api_casedata)
        else:
            api_logger.error("用例格式错误：%s" % msg)
            raise Exception("用例格式校验失败，" + msg)

    def apicase_processors(self, pro_data, recv_data=None, recv_code=None):
        """
        接口用例前后置操作
        :param recv_data: 返回数据
        :param recv_code: 返回状态码
        :param pro_data: 前后置操作数据
        :return:
        """
        for pro in pro_data.keys():
            # 结果校验
            if pro == 'assert':
                checkresult.check_result(pro_data['assert'], recv_data, recv_code)
            # 数据库操作
            if pro == 'database':
                # 执行数据库操作，获取参数
                db_dict = database.HandleDB().handle_dbdata(pro_data['database'])
                # db_dict = database.SetUpDB().get_setup_sql_data(pro_data['database'])
                # 更新临时变量字典
                self.temp_var_dict = handledict.dict_update(self.temp_var_dict, db_dict)
            # 提取变量
            if pro == 'extract':
                temp_value = extract.handle_extarct(pro_data['extract'], recv_data)
                self.temp_var_dict = handledict.dict_update(self.temp_var_dict, temp_value)
            # 执行自定义脚本
            if pro == 'script':
                exec(pro_data['script'])
            if pro == 'sleep':
                time.sleep(pro_data['sleep'])

def send_request(casedata):
    """
    发送请求
    :param casedata: 用例信息
    :return:
    """
    with allure.step("发送请求"):
        request_data = casedata['request']
        url = casedata['base_url'] + request_data['address']
        method = request_data['method']
        headers = request_data['headers']

        api_logger.info("请求地址：%s" % url)
        api_logger.info("请求方法：%s"% method)
        api_logger.info("请求头：%s"% headers)

        allure.attach(name="请求方法：", body=method)
        allure.attach(name="请求地址", body=url)
        allure.attach(name="请求头", body=str(headers))

        data = None
        file = None
        cert = None
        # 判断是否存在请求参数
        if 'data' in request_data.keys():
            data = request_data['data']
            api_logger.info("请求参数：%s"% data)
            allure.attach(name="请求参数", body=str(data))
        # 判断是否存在文件
        if 'file' in request_data.keys():
            file = request_data['file']
            api_logger.info("上传文件：%s" % file)
            allure.attach(name="上传文件", body=str(file))
        # 判断是否存在证书
        if 'iscert' in casedata.keys() and casedata['iscert']:
            cert = tuple([os.path.join(CERT_DIR, i) for i in config_dict['cert']])
            api_logger.info("证书：%s" % cert)
            allure.attach(name="证书", body=str(cert))

        #发送请求
        if method in ['post', 'POST']:
            recv_data, recv_code = ApiMethod(url, headers, data, file, cert).post()
        elif method in ['get', 'GET']:
            recv_data, recv_code = ApiMethod(url, headers, data, file, cert).get()
        elif method in ['put', 'PUT']:
            recv_data, recv_code = ApiMethod(url, headers, data, file, cert).put()
        elif method in ['delete', 'DELETE']:
            recv_data, recv_code = ApiMethod(url, headers, data, file, cert).delete()
        else:
            raise Exception("暂不支持" + method + "请求类型！")
        return recv_data, recv_code


class ApiMethod:
    """
    request请求封装
    """

    def __init__(self, url, headers, data=None, file=None, cert=None):
        self.url = url
        self.headers = headers
        self.data = data
        self.file = file
        self.cert = cert

    def file_upload(self):
        """
        文件上传文件处理
        :return:
        """
        fields = []
        if self.data:
            for kv in self.data.items():
                fields.append(kv)
        if 'file_type' in self.file.keys():
            file_type = self.file['file_type']
            self.file.pop('file_type')
        else:
            file_type = 'application/octet-stream'
        for key in self.file:
            value = self.file[key]
            if type(value) == list:
                for i in value:
                    file_path = FILE_DIR + '/' + i
                    file = (key, (os.path.basename(file_path), open(file_path, 'rb'), file_type))
                    fields.append(file)
            else:
                file_path = FILE_DIR + '/' + value
                file = (key, (os.path.basename(file_path), open(file_path, 'rb'), file_type))
                fields.append(file)
        multipart = MultipartEncoder(fields)
        self.headers['Content-Type'] = multipart.content_type
        return multipart

    #post请求
    def post(self):
        if "application/json" in self.headers.values():
            recv_result = requests.post(url=self.url,
                                        headers=self.headers,
                                        json=self.data, cert=self.cert, verify=False)
        elif "multipart/form-data" in self.headers.values():
            if self.file:
                multipart = self.file_upload()
                recv_result = requests.post(url=self.url, data=multipart, headers=self.headers, cert=self.cert, verify=False)
            else:
                recv_result = requests.post(url=self.url, headers=self.headers, data=self.data, cert=self.cert, verify=False)
        else:
            recv_result = requests.post(url=self.url, headers=self.headers, data=self.data, cert=self.cert, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        api_logger.info("请求接口结果： %s" % str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    #get请求
    def get(self):
        recv_result = requests.get(url=self.url, headers=self.headers, params=self.data, cert=self.cert, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        api_logger.info("请求接口结果： %s" % str(res))
        allure.attach(name="请求结果", body=str(res))

        return res, recv_result.status_code

    #put请求
    def put(self):
        if 'application/json' in self.headers.values():
            recv_result = requests.put(url=self.url, headers=self.headers, json=self.data, cert=self.cert, verify=False)
        elif "multipart/form-data" in self.headers.values():
            if self.file:
                multipart = self.file_upload()
                recv_result = requests.put(url=self.url, data=multipart, headers=self.headers, cert=self.cert, verify=False)
            else:
                recv_result = requests.put(url=self.url, headers=self.headers, data=self.data, cert=self.cert, verify=False)
        else:
            if self.data:
                self.data = json.dumps(self.data)
            recv_result = requests.put(url=self.url, headers=self.headers, data=self.data, cert=self.cert, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        api_logger.info("请求接口结果： %s" % str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    #delete请求
    def delete(self):
        if 'application/json' in self.headers.values():
            recv_result = requests.delete(url=self.url, json=self.data, headers=self.headers, cert=self.cert, verify=False)
        else:
            recv_result = requests.delete(url=self.url, params=self.data, headers=self.headers, cert=self.cert, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        api_logger.info("请求接口结果： %s" % str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code
