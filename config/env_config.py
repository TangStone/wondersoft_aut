# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: env_config.py
@IDE: PyCharm
@time: 2024-03-27 16:25
@description: 环境配置信息
"""

# ------------------------------------ 环境配置信息 ----------------------------------------------------#
ENV_VARS = {
    "test": {
        # 项目名称
        "project_name": "统一管理平台",
        # 服务地址
        "host": "https://192.168.148.174:31000",
        # 登录账号
        "login": "admin",
        "password": "Ws-123456",
        "login_name": "admin",  # 登录用户名
        "login_url": "/portal-login",  # 登录页面url
    },
    "dev": {
        # 项目名称
        "project_name": "统一管理平台",
        # 服务地址
        "host": "https://192.168.150.227:31000",
        # 登录账号
        "login": "admin",
        "password": "Ws-123456",
        "login_name": "admin",  # 登录用户名
        "login_url": "/portal-login",  # 登录页面url
    },
    "prod": {}
}

# ------------------------------------ 基础参数信息 ----------------------------------------------------#
BASE_VARS = {
    # AD域配置
    "domain": {
        # 参数配置
        "config": {
            "数据源名称": "70.235",  # 数据源名称
            "域地址": "192.168.70.235",  # 域地址
            "域端口": "389",  # 域端口
            "域管理员账号": r"xiantest\administrator",  # 域管理员账号
            "域管理员密码": "Ws-123456r",  # 域管理员密码
            "根域名": "DC=xiantest,DC=com",  # 根域名
            "组织机构名称": "ou=北京明朝万达",  # 组织机构名称
            "启用加密": False,  # 启用加密
            "用户过滤条件": "",  # 用户过滤条件
            "组织过滤条件": "",  # 组织过滤条件
            "是否增量同步": False  # 是否增量同步
        },
        "relations": {
            "数据唯一标识": "objectGUID",  # 数据唯一标识
            "机构标签": "ou",  # 机构标签
            "机构名称": "name",  # 机构名称
            "用户标签": "cn",  # 用户标签
            "用户账号": "sAMAccountName",  # 用户账号
            "用户Sid": "objectSid",  # 用户Sid
            "用户唯一标识符": "distinguishedName",  # 用户唯一标识符
            "上级领导人": "",  # 上级领导人
            "用户密码": "",  # 用户密码
            "工号": "",  # 工号
            "电话": "",  # 电话
            "手机": "",  # 手机
            "邮箱": "mail",  # 邮箱
            "增量同步标识": ""  # 增量同步标识
        }
    }
    # # AD域配置
    # "domain": {
    #     # 参数配置
    #     "config": {
    #         "name": "70.235",   # 数据源名称
    #         "host": "192.168.70.235",  # 域地址
    #         "port": "389",  # 域端口
    #         "username": r"xiantest\administrator", # 域管理员账号
    #         "password": "Ws-123456e",  # 域管理员密码
    #         "base": "DC=xiantest,DC=com",  # 根域名
    #         "org": "ou=北京明朝万达",   # 组织机构名称
    #         "isEncrypt": "false",   # 启用加密
    #         "userFilter": "",   # 用户过滤条件
    #         "groupFilter": "",  # 组织过滤条件
    #         "isIncrement": "false"  # 是否增量同步
    #     },
    #     "relations": {
    #         "sourceUUID":  "objectGUID",  # 数据唯一标识
    #         "groupLabel":  "ou",  # 机构标签
    #         "groupName":  "name",  # 机构名称
    #         "userLabel":  "cn",  # 用户标签
    #         "userName":  "sAMAccountName",  # 用户账号
    #         "userSid":  "Sid：objectSid",  # 用户Sid
    #         "dnKey":  "distinguishedName",  # 用户唯一标识符
    #         "leaderUserSid":  "",  # 上级领导人
    #         "userPwd":  "",  # 用户密码
    #         "employeeId":  "",  # 工号
    #         "telephone":  "",  # 电话
    #         "mobile":  "",  # 手机
    #         "email":  "mail",  # 邮箱
    #         "deleteFlag":  ""  # 增量同步标识
    #     }
    # }
}
