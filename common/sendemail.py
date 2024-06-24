# -*- coding: utf-8 -*-

"""
@author: tanglei
@File: sendemail.py
@IDE: PyCharm
@time: 2024-6-21 15:34
@description: 发送邮件
"""
import smtplib, shutil
from utils.log_utils.logger_handle import api_logger
from common import handleallure
from common.basefunc import config_dict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import *

class SendEmail:
    """
    发送邮件
    """

    def __init__(self, report_name):
        self.report_name = report_name     # 报告名称
        self.report_path = REPORT_DIR + '/' + report_name  # allure报告路径
        self.run_case_data = handleallure.AllureReportData(report_name).get_case_count()    # 获取用例运行数据
        self.email_config = config_dict['email']   # 邮箱配置信息

    def send_main(self):
        api_logger.info('-·-·-·-·-·-·-·-·-·-发送结果邮件 START-·-·-·-·-·-·-·-·-·-')

        sendAddress = self.email_config['sender']
        password = self.email_config['senderPwd']
        server = smtplib.SMTP(self.email_config['sendserver'], self.email_config['port'])

        msg = MIMEMultipart()
        msg['Subject'] = config_dict['project_name'] + "接口自动化报告"
        msg['From'] = sendAddress
        msg['To'] = self.email_config['receiver']

        content = f"""
        大家好:
            {config_dict['project_name']}接口自动化用例执行完成，执行结果如下:

                开始时间: {self.run_case_data['start_time']}
                结束时间: {self.run_case_data['end_time']}
                运行时长: {self.run_case_data['time']}
                -------------------------------------------------
                用例运行总数: {self.run_case_data['total']} 个
                通过用例个数: {self.run_case_data['passed']} 个
                失败用例个数: {self.run_case_data['failed']} 个
                异常用例个数: {self.run_case_data['broken']} 个
                跳过用例个数: {self.run_case_data['skipped']} 个
                成  功   率: {self.run_case_data['pass_rate']} %

            测试报告见附件！
        """
        msg.attach(MIMEText(content, 'plain', 'utf-8'))  # 添加邮件内容

        # 压缩allure报告
        shutil.make_archive(self.report_path, 'zip', self.report_path)

        att1 = MIMEApplication(open(self.report_path + '.zip', 'rb').read())   # 添加附件
        att1['Content-Type'] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment; filename="' + self.report_name + '.zip"'
        msg.attach(att1)

        server.login(sendAddress, password)    # 登录邮箱
        server.sendmail(sendAddress, [x for x in self.email_config['receiver'].split(';') if x], msg.as_string())  # 发送邮件
        server.quit()

        api_logger.info('-·-·-·-·-·-·-·-·-·-发送结果邮件 END-·-·-·-·-·-·-·-·-·-')
