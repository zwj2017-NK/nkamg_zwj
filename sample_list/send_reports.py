#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Author: Wenjun Zhu
#Time: 23th July,2018.
#Email: 1103466626@qq.com

import os
import shutil
import subprocess
import pandas as pd
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

PATH_RES = config.get("path", "path_res")
PATH_CSV = config.get("path", "path_csv")
PATH_JSON = config.get("path", "path_json") 
PATH_BAK = config.get("path", "path_bak")
PATH_TXT = config.get("path","path_txt")
PATH_YEAR = config.get("path","path_year")
FROM_ADDR = config.get("email_info","from_addr")
PASSWORD = config.get("email_info","password")
TO_ADDR = [i[1] for i in config.items("email_addr")]
SMTP_SERVER = config.get("email_info","smtp_server")
CMD = [i[1] for i in config.items("cmd")]
YEARS = [i[1] for i in config.items("years")]

def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_email(msg_string):
  msg = MIMEText(msg_string, 'plain', 'utf-8')
  msg['From'] = _format_addr(u'NKAMG<%s>' % FROM_ADDR)
  msg['To'] = _format_addr(u'Administrator <%s>' % TO_ADDR)
  msg['Subject'] = Header(u'--每日报告--', 'utf-8').encode()
  server = smtplib.SMTP(SMTP_SERVER, 25)
  server.set_debuglevel(1)
  server.login(FROM_ADDR, PASSWORD)
  server.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())# 
  server.quit()

def monitor():
  #the function monitors the path of /data/daily_json/, which includes all json files from other servers today, and
  #can generate two lists saved in txt files(malware.txt and benign.txt)
  list_malware = []
  list_benign = []
  path = os.listdir(PATH_JSON)
  if len(path) == 0:
    print "no json file"
    return
  for i in path:
    if 'json' in i:
      try:
        with open(PATH_JSON + i, 'rb') as f:
          temp = json.load(f)
      except Exception,e:
	print i + 'error'
      for j in temp.keys():
        try:
          if temp[j]['positives'] == 0:
            list_benign.append(j)
          else:
            list_malware.append(j)
        except Exception,e:
          pass
    print i

  with open(PATH_TXT + 'malware.txt','wb') as h1:
    for m in list_malware:
      h1.write(m + '\n')
  with open(PATH_TXT + 'benign.txt','wb') as h2:
    for n in list_benign:
      h2.write(n + '\n') 
  for j in path:
    try:
      shutil.move(PATH_JSON + j, PATH_BAK)
    except Exception,e:
      pass

def get_intersection():
  #according to year, appending hash string into different files.
  path = os.listdir(PATH_YEAR)
  years = [i[:-4] for i in path]
  for year in years:
    #cmd3 = 'grep -F -f vt_malware.txt ' + PATH_YEAR + year + '.txt' + ' | sort | uniq > ' + PATH_RES + year + '_m.txt' 
    cmd3 = 'grep -F -f ' + PATH_TXT + 'malware.txt ' + PATH_YEAR + year + '.txt' + ' | sort | uniq >> ' + PATH_RES + year + '_m.txt' 
    subprocess.call(cmd3, shell=True)  
    print year,'m'
  for year in years:
    #cmd3 = 'grep -F -f vt_benign.txt ' + PATH_YEAR + year + '.txt' + ' | sort | uniq > ' + PATH_RES + year + '_b.txt' 
    cmd3 = 'grep -F -f ' + PATH_TXT + 'benign.txt ' + PATH_YEAR + year + '.txt' + ' | sort | uniq >> ' + PATH_RES + year + '_b.txt' 
    subprocess.call(cmd3, shell=True)  
    print year,'b'

def rsync(cmd):
  #conduct a shell command
  subprocess.call(cmd, shell=True)

def get_vt_num():
  #getting the number of vt, which include malware and benign number of 2014,2015,2016,2017.
  #2014_m,2015_m,2016_m,2017_m,2014_b,2015_b,2016_b,2017_b

  list_num = []
  for i in ['_m.txt','_b.txt']:
    for year in YEARS:
      with open(PATH_RES + year + i, 'rb') as f:
	list_num.append(len(f.readlines()))
  print list_num
  return list_num

def get_download_and_data_num():
  #2014,2015,2016,2017
  #list_num1 for download number 
  #list_num2 for data file number

  for i in range(len(CMD)):
    rsync(CMD[i])
  list_num1 = [0 for i in range(4)]
  list_num2 = [0 for i in range(4)]

  for year in YEARS:
      if os.path.exists('/data/sample_list/162/162_' + year + '.txt'):
        with open('/data/sample_list/162/162_' + year + '.txt', 'rb') as f:
          num = len(f.readlines())
          list_num1[int(year) - 2014] = list_num1[int(year) - 2014] + num
          list_num2[int(year) - 2014] = list_num2[int(year) - 2014] + num
  print list_num1,list_num2

  for year in YEARS:
    str_num = os.popen('ls /data/' + year + '/ -l | grep data | wc -l')
    flag = int(str_num.read())
    list_num2[int(year) - 2014] = list_num2[int(year) - 2014] + flag
    print year,flag

  dict_time = {'061':2016,'161':2014,'166':2015,'164':2017}
  paths = os.listdir(PATH_CSV)
  for i in paths:
    if 'bhs' not in i:
      df = pd.read_csv(PATH_CSV + i, sep=',')
      for j in dict_time.keys():
        if j in i:
          list_num1[dict_time[j] - 2014] = list_num1[dict_time[j] - 2014] + df.ix[0]['count']
          print i,j,df.ix[0]['count']
          break
    else: 
      df = pd.read_csv(PATH_CSV + i, sep=',')
      for k in range(df.shape[0]):
        list_num1[k] = list_num1[k] + df.ix[k]['apk']
        list_num2[k] = list_num2[k] + df.ix[k]['data'] 
        print i,df.ix[k]['apk'],df.ix[k]['data']

  for year in YEARS:
    num1 = int((os.popen('ls /data/' + year + '/ -l | wc -l')).read())
    num2 = int((os.popen('ls /data/' + year + '/ -l | grep data | wc -l')).read())
    num3 = int((os.popen('ls /data/' + year + '/ -l | grep xml | wc -l')).read())
    num_year = num1 - num2 - num3
    list_num1[int(year) - 2014] = list_num1[int(year) - 2014] + num_year
    #print year,num_year
  print list_num1, list_num2
  return list_num1, list_num2

def format_string(year, num1, num2, num3, num4 ):
  #formatting string information for sending e-mail.
  return "{0}:android:{1:<10} malicious_label:{2:<10} benign_label:{3:<10} data:{4:<10}".format(year, num4, num1, num2, num3) 

def return_mail_string(list_vt, list_data, list_download):
  #joint the numbers in lists to generate the daily report.
  string_mail = "{0:^75}".format("----------Daily Mail----------") + "\n"
  for i in range(len(YEARS)):
    string_mail = string_mail + format_string(YEARS[i], list_vt[i], list_vt[i+4], list_data[i], list_download[i]) + "\n"
  return string_mail

def main():
  monitor()
  cmd = 'rsync -av --progress /data/sample_list/result/ /data/sample_list/bakeup_txt/'
  rsync(cmd) 
  get_intersection()
  #list_download, list_data = get_download_and_data_num()
  #list_vt = get_vt_num()
  #string_mail = return_mail_string(list_vt, list_data, list_download)
  #send_email(string_mail)
  #print string_mail

if __name__ == '__main__':
  main()

