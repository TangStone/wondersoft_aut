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
        "base_url": "https://192.168.148.174:31000",
        #全局登录接口
        "logincase": "login_01",
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
    },
     # 数据库类型
    "db_type": "mysql",
     # 数据库相关配置
    "mysql_db": {
        "host": "192.168.148.174",
        "user": "root",
        "password": "ws-123456",
        "port": 3306
    },
    # redis相关配置
    "redis": {
        "host": "192.168.148.174",
        "port": 6379,
        "password": "unity2.0@wondersoft"
    },
    # kafka相关配置
    "kafka": {
        "bootstrap-servers": "192.168.148.174:9094"
    },
    # 用例路径,列表形式
    "casedata_path": [],
    # 证书文件
    "cert": [
        "example.crt",
        "example.key"
    ],
    # 邮件配置
    "email": {
        "sendemail": False,
        "sendserver": "smtp.wondersoft.cn",
        "port": 25,
        "sender": None,
        "senderPwd": None,
        "receiver": None
    }
}
