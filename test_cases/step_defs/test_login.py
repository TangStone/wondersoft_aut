# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_login.py
@IDE: PyCharm
@time: 2024-03-27 18:58
@description:
"""
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("./login.feature")
