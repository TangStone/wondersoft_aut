# -*- coding: utf-8 -*-

"""
@author: tanglei
@File: handledict.py
@IDE: PyCharm
@time: 2024-06-21 18:00
@description: 字典处理
"""
def dict_update(old_dict, update_dict):
    """
    字典更新
    :param old_dict: 原始字典
    :param update_dict: 更新字典
    :return: 更新后的字典
    """
    if old_dict:   #非空字典
        if isinstance(old_dict, dict) and isinstance(update_dict, dict):
            for key, value in update_dict.items():
                if isinstance(value, dict) and key in old_dict.keys():
                        old_value = old_dict[key]
                        old_dict[key] = dict_update(old_value, value)
                else:
                    old_dict[key] = value
    else:
        old_dict = update_dict
    return old_dict


def cmp_dict(expect_data, recv_data):
    """
    返回值比较比较
    :param expect_data: 期望字典
    :param recv_data: 返回值
    :return:
    """
    flag = True
    if isinstance(expect_data, dict) and isinstance(recv_data, dict):
        if set(expect_data.keys()).issubset(set(recv_data.keys())):
            for field, data in expect_data.items():
                if type(data) == dict:  # 预期值为字典
                    if type(recv_data[field]) == dict:  # 返回值也为字典
                        flag = cmp_dict(data, recv_data[field])  # 递归比较
                    else:
                        flag = False
                    if not flag:
                        break
                elif type(data) == list:  # 预期值为列表
                    if type(recv_data[field]) == list:  # 返回值也为列表
                        for i in data:
                            if type(i) == dict:
                                flag = False
                                for j in recv_data[field]:
                                    flag = cmp_dict(i, j)
                                    if flag:  # 字典中有一个比较成功就返回
                                        break
                                if not flag:
                                    break
                            else:  # 非字典格式直接比较
                                # if data != recv_dict[field]:
                                if str(data) != str(recv_data[field]):  # 暂时只进行字符串比较
                                    flag = False
                                break
                    else:
                        flag = False
                    if not flag:
                        break
                else:  # 非字典，列表格式直接比较
                    # if expect_dict[field] != recv_dict[field]:
                    if str(expect_data[field]) != str(recv_data[field]):  # 暂时只进行字符串比较
                        flag = False
                        break
        else:
            flag = False
    elif isinstance(expect_data, list) and isinstance(recv_data, list):
        for i in expect_data:
            if type(i) == dict:
                flag = False
                for j in recv_data:
                    flag = cmp_dict(i, j)
                    if flag:  # 字典中有一个比较成功就返回
                        break
                if not flag:
                    break
            else:  # 非字典格式直接比较
                # if data != recv_dict[field]:
                if str(expect_data) != str(recv_data):  # 暂时只进行字符串比较
                    flag = False
                break
    else:
        flag = False
    return flag
