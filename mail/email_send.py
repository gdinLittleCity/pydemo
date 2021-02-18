#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
sender = 'gdinhxc@163.com'

receivers = ['gdinxiao@sina.com', 'huangxiaocheng@ecpark.cn']

message = MIMEText('Just for test', 'plain', 'utf-8')
message['From'] = Header("admin")   # 发送者
message['To'] =  Header("test")        # 接收者

subject = 'SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')


try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")


