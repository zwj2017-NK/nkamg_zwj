#-*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from settings import SMTP_SERVER
from settings import FROM_ADDR
from settings import PASSWORD
from settings import TO_ADDR

def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_email(msg_string):
  msg = MIMEText(msg_string, 'plain', 'utf-8')
  msg['From'] = _format_addr(u'zhuwenjun<%s>' % FROM_ADDR)
  msg['To'] = _format_addr(u'Administrator <%s>' % TO_ADDR)
  msg['Subject'] = Header(u'--每日报告--', 'utf-8').encode()
  server = smtplib.SMTP(SMTP_SERVER, 25)
  server.set_debuglevel(1)
  server.login(FROM_ADDR, PASSWORD)
  server.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())# 
  server.quit()

# IP地址由各个服务器自己生成，email.py只负责发邮件
#def get_local_ip(ifname):
#  import socket, fcntl, struct
#  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
#  ret = socket.inet_ntoa(inet[20:24])
#  return ret

