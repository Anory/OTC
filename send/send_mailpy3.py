#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import json
from email.header import Header
from email.mime.text import MIMEText
 

class SendMail(object):
    # init attribute
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.exmail.qq.com"      # SMTP服务器
        self.mail_user = 'janmmeyzhu@mozi.top'     # 用户名
        self.mail_pass = 'System_32'               # 登录密码
        self.sender = 'janmmeyzhu@mozi.top'    # 发件人邮箱(最好写全, 不然会失败)
        self.receivers = ['876522068@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    def sendMessage(self, content, title):
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = title 
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)


if __name__ == '__main__':
    init_env = SendMail()
    content = '发送测试邮件'
    title = 'Send Mail By Python'  # 邮件主题
    init_env.sendMessage(content,title)

