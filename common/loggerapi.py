# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: logger.py
@IDE: PyCharm
@time: 2023-06-02 15:59
@description: 日志处理
"""
import logging.config
import os, time

from common.handleyaml import YamlHandle
from common.basefunc import clean_dir

class MyLogs:

    def setup_logging(self, root_dir):
        """

        :param root_dir: 主目录路径
        :return:
        """
        #清除日志
        # clean_dir(root_dir + 'logs/')
        # # runtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        # # log_path = root_dir + 'logs/' + runtime
        log_path = root_dir + 'logs/'
        # if not os.path.exists(log_path):
        #     os.makedirs(log_path)

        #读取日志配置文件
        log_conf_path = root_dir + 'config/logging.yml'
        log_conf = YamlHandle(log_conf_path).read_yaml()

        #修改配置文件中的日志路径
        for value in log_conf['handlers'].values():
            if 'filename' in value.keys():
                value['filename'] = log_path + '/' + value['filename']

        logging.config.dictConfig(log_conf)