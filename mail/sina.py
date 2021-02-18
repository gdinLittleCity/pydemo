#! /usr/bin/env python
#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


#qq邮箱smtp服务器
# host_server = 'smtp.sina.com'
host_server = 'smtp.qq.com'
#sender_qq为发件人的qq号码
# user = 'gdinxiao@sina.com'
user = '1137835956@qq.com'
# user = 'test@test.com'
#pwd为qq邮箱的授权码
# pwd = '7ad2375c2ba3c212' ## xh**********bdc
pwd = 'ppozbpjwkiwyjdde'
# pwd = '123456'
#发件人的邮箱
# sender_mail = 'gdinxiao@sina.com'
sender_mail = '1137835956@qq.com'
#收件人邮箱
# receiver = 'jiangnan@ecpark.cn'
receiver = 'huangxiaocheng@ecpark.cn'

#邮件的正文内容
mail_content = ''
with open('年会.htm', "r", encoding='utf-8') as infile:
    mail_content = infile.read()
#邮件标题
mail_title = '【通知】2021年会行程通知！！！'

#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(user, pwd)

msg = MIMEText(mail_content, "html", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = Header('yanggm@ecpark.cn') #'gdinxiao@sina.com'
msg["To"] = Header('所有员工','utf-8')  #'huangxiaocheng@ecpark.cn'
smtp.sendmail(sender_mail, receiver, msg.as_string())
smtp.quit()