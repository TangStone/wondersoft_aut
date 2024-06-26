# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: checkresult.py
@IDE: PyCharm
@time: 2023-06-04 21:31
@description: 结果校验
"""
import allure,jsonpath, json
from utils.log_utils.logger_handle import api_logger
from common import handledict
from common import database


def check_result(hope_res, real_res, real_code):
    """
    返回结果校验
    :param hope_res: 期望结果
    :param real_res: 实际结果
    :param real_code: 返回状态码
    :return:
    """
    with allure.step("结果校验"):
        for key, value in hope_res.items():
            if key == 'code':
                assert_code(value, real_code)
            elif key == 'jsonpath':
                assert_text(value,real_res)
            elif key == 'response':
                assert_response(value, real_res)
            elif key == 'dbcheck':
                assert_db(value)

def assert_db(hope_res):
    """
    数据库校验
    :param hope_res:
    :return:
    """
    if hope_res:
        for dbcheck_data in hope_res:
            db_type = dbcheck_data['type']  # 数据库类型
            if db_type == 'mysql':
                db_sql = dbcheck_data['sql']
                if db_sql[0:6].upper() == 'SELECT':
                    sql_date = database.MysqlConn().mysql_query(db_sql)
                    with allure.step("数据库校验"):
                        for param in dbcheck_data['result']:
                            try:
                                sql_value = jsonpath.jsonpath(sql_date, param['path'])
                                value = param['value']
                                allure.attach(name="查询sql", body=str(db_sql))
                                allure.attach(name="期望返回值", body=str(value))
                                if sql_value:
                                    allure.attach(name='实际返回值', body=str(sql_value[0]))
                                    assert str(value) == str(sql_value[0])
                                    api_logger.info("数据库断言通过, 期望结果:%s, 实际结果:%s" % (value, sql_value[0]) )
                                else:
                                    allure.attach(name='实际返回值', body=str(sql_value))
                                    raise AssertionError("该条sql未查询出任何数据:" + str(db_sql))
                            except AssertionError:
                                api_logger.error("数据库断言未通过, 期望返回值:%s, 实际返回值：%s" % (value, sql_value[0]))
                                raise
                else:
                    raise Exception("断言的 sql 必须是查询的 sql")
            elif db_type == 'redis': # redis 数据库校验
                redis_conn = database.RedisConn(dbcheck_data['db'])   # 连接 redis
                cmd_list = dbcheck_data['cmd'].split(' ')
                new_list = ['"' + item + '"' for item in cmd_list[1:]]
                para = ','.join(new_list)    # 拼接参数
                run_code = f"""redis_conn.conn.{cmd_list[0]}({para})"""    # 拼接执行代码
                cmd_data = eval(run_code)  # 执行代码
                with allure.step("redis校验"):
                    if 'result' in dbcheck_data.keys():  # 存在 result 时，使用 jsonpath 校验
                        for param in dbcheck_data['result']:
                            try:
                                cmd_value = jsonpath.jsonpath(json.loads(cmd_data), param['path'])
                                value = param['value']

                                allure.attach(name="操作命令", body=str(dbcheck_data['cmd']))
                                allure.attach(name="期望返回值", body=str(value))
                                if cmd_value:
                                    allure.attach(name='实际返回值', body=str(cmd_value[0]))
                                    assert str(value) == str(cmd_value[0])
                                    api_logger.info("redis断言通过, 期望结果:%s, 实际结果:%s" % (value, cmd_value[0]))
                                else:
                                    allure.attach(name='实际返回值', body=str(cmd_value))
                                    raise AssertionError("该命令未查询出任何数据:" + str(dbcheck_data['cmd']))
                            except AssertionError:
                                api_logger.error("redis断言未通过, 期望返回值:%s, 实际返回值：%s" % (value, cmd_value[0]))
                                raise
                    else:  # 不存在 result 时，直接使用 value 校验
                        allure.attach(name="操作命令", body=str(dbcheck_data['cmd']))
                        allure.attach(name="期望返回值", body=str(dbcheck_data['value']))
                        allure.attach(name='实际返回值', body=str(cmd_data))
                        assert str(cmd_data) == str(dbcheck_data['value'])
            elif db_type == 'kafka':    # kafka 数据库校验
                kafka_msg = database.KafkaConn().kafka_get_msg(dbcheck_data['topic'])   # 获取kafka最后一条消息
                with allure.step("kafka校验"):
                    if 'result' in dbcheck_data.keys(): # 存在 result 时，使用 jsonpath 校验
                        for param in dbcheck_data['result']:
                            try:
                                kafka_value = jsonpath.jsonpath(json.loads(kafka_msg), param['path'])
                                value = param['value']

                                allure.attach(name="查询topic", body=str(dbcheck_data['topic']))
                                allure.attach(name="期望返回值", body=str(value))
                                if kafka_value:
                                    allure.attach(name='实际返回值', body=str(kafka_value[0]))
                                    assert str(value) == str(kafka_value[0])
                                    api_logger.info("kafka断言通过, 期望结果:%s, 实际结果:%s" % (value, kafka_value[0]))
                                else:
                                    allure.attach(name='实际返回值', body=str(kafka_value))
                                    raise AssertionError("该topic未查询出任何数据:" + str(kafka_value))
                            except AssertionError:
                                api_logger.error("kafka断言未通过, 期望返回值:%s, 实际返回值：%s" % (value, kafka_value[0]))
                                raise
                    else: # 不存在 result 时，直接使用 value 校验
                        allure.attach(name="查询topic", body=str(dbcheck_data['topic']))
                        allure.attach(name="期望返回值", body=str(dbcheck_data['value']))
                        allure.attach(name='实际返回值', body=str(kafka_msg))
                        assert str(kafka_msg) == str(dbcheck_data['value'])

            else:
                raise Exception("当前暂不支持此种数据库类型：" + str(db_type))


def assert_response(hope_res, real_res):
    """
    返回结果校验 -全返回校验
    :param hope_res: 
    :param real_res: 
    :return: 
    """
    try:
        with allure.step("返回值校验"):
            hope_res = json.loads(json.dumps(hope_res))
            allure.attach(name="期望返回值", body=str(hope_res))
            allure.attach(name='实际返回值', body=str(real_res))
            if isinstance(hope_res, (dict, list)) and isinstance(real_res, (dict, list)):
                flag = handledict.cmp_dict(hope_res, real_res)
                assert flag
            else:
                assert str(hope_res) == str(real_res)
            api_logger.info("返回结果断言通过, 期望返回值:%s, 实际返回值:%s" % (hope_res, real_res))
    except AssertionError:
        api_logger.error("返回结果断言未通过, 期望返回值:%s, 实际返回值:%s"% (hope_res, real_res))
        raise

def assert_text(hope_res, real_res):
    """
    返回结果校验 -jsonpath
    :param hope_res: 期望返回结果
    :param real_res: 实际返回结果
    :return:
    """
    if isinstance(hope_res, list):
        for h_res in hope_res:
            if jsonpath.jsonpath(real_res, h_res['path']):
                r_res = jsonpath.jsonpath(real_res, h_res['path'])[0]
                if h_res['type'] == '==':
                    try:
                        with allure.step("json断言判断相等"):
                            allure.attach(name="期望结果", body=str(h_res))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) == str(r_res)
                            api_logger.info("json断言通过, 期望结果:%s, 实际结果:%s" % (h_res, r_res))
                    except AssertionError:
                        api_logger.error("json断言未通过, 期望结果:%s, 实际结果:%s" % (h_res, r_res))
                        raise
                elif h_res["type"] == "!=":
                    try:
                        with allure.step("json断言判断不等"):
                            allure.attach(name="json期望结果", body=str(h_res))
                            allure.attach(name='json实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) != str(r_res)
                            api_logger.info("json断言通过, 期望结果:%s, 实际结果:%s" % (h_res, r_res))
                    except AssertionError:
                        api_logger.error("json断言未通过,  期望结果:%s, 实际结果:%s" % (h_res, r_res))
                        raise
                elif h_res["type"] == "in":
                    r_res = str(r_res)
                    try:
                        with allure.step("json断言判断包含"):
                            allure.attach(name="期望结果", body=str(h_res))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) in str(r_res)
                            api_logger.info("json断言通过, 期望结果:%s, 实际结果:%s" % (h_res, real_res))
                    except AssertionError:
                        api_logger.error("json断言未通过, 期望结果:%s, 实际结果:%s" % (h_res, real_res))
                        raise
                else:
                    raise TypeError("type方法错误")
            else:
                with allure.step("json断言"):
                    allure.attach(name="json期望结果", body=str(h_res))
                    allure.attach(name='json实际实际结果', body="None")
                    api_logger.error("获取json值失败，请检查jsonpath")
                    assert False
                # raise ValueError('获取json值失败，请检查jsonpath')

def assert_code(hope_code, real_code):
    """
    返回状态码校验
    :param hope_res: 期望返回状态码
    :param real_res: 实际返回状态码
    :return:
    """
    try:
        with allure.step("状态码校验"):
            allure.attach(name="期望状态码", body=str(hope_code))
            allure.attach(name='实际状态码', body=str(real_code))
            assert real_code == hope_code
            api_logger.info("code断言通过, 期望状态码:%s, 实际状态码:%s" % (hope_code, real_code))
    except AssertionError:
        api_logger.error("code断言未通过, 期望状态码:%s, 实际状态码:%s" % (hope_code, real_code))
        raise