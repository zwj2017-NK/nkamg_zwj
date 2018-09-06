#!/usr/bin/env python
#-*- coding: utf-8 -*-

import core.write_result as WR 
import multiprocessing as mp
import progressbar as pb
import os
import time
import requests
import shutil
import json
import re
import datetime
import random
import pandas as pd
from multiprocessing import Pool
from core.settings import APIKEYS
from core.settings import DATA_FOLDER
from core.settings import VT_FILE 
from core.settings import BENIGN_FOLDER
from core.settings import MALWARE_FOLDER
from core.settings import get_malware_dir
from core.settings import get_benign_dir

list_apikey = APIKEYS
n_apikey = len(list_apikey)
url = 'https://www.virustotal.com/vtapi/v2/file/report'

def get_vt_sum_lists():
  pathstr='0123456789abcdef'
  list_todo = []
  task_list = []
  for i in list(pathstr):
    for j in list(pathstr):
      for k in list(pathstr):
        task_list.append(i+j+k)
  pool = Pool(16)
  result = pool.map(get_vt_list, task_list)
  pool.close()
  pool.join()
  for m in result:
    for n in m:
      if n is '':
        continue
      list_todo.append(n)
  return list_todo

def write_res(list_res):
  if len(list_res) == 0:
    return
  list_todo = []
  for i in list_res:
    if i[0] == 0 and i[1] == 0:
      continue
    list_todo.append(i)
  print "write_res()"
  WR.write_csv(list_todo)	

def do_task(temp):
  try:
    params = { 'resource': temp}
    k = 0
    while True: 
      seq = random.randint(0,57)
      params['apikey'] = list_apikey[seq],
      response = requests.get(url, params=params)
      print response.status_code
      if response.status_code == 200:
        return (response.json(),temp)
      k = k + 1
      if k == 14:
        return (0, 0)
      time.sleep(3)
  except Exception,e:
    print e
    return (0,0)

def get_vt(vt_todo_list):
  list_res = []  
  wflag = 0
  flag = 0
  num = 0
  for i,fname in enumerate(vt_todo_list):
    tuple_res = do_task(fname)
    list_res.append(tuple_res)
    if tuple_res[0] == 0 and tuple_res[1] == 0:
      print tuple_res
      flag = flag + 1
    else:
      print fname + '>>>>>>>>' + 'succeed'
      num = num + 1
      flag = 0
    if num%2==0 and num!=0:
      write_res(list_res)
      list_res = []
    if flag >= 200 or (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[11:16] == '11:29' and wflag==0):
      wflag = 1
      if os.path.exists(VT_FILE):
        with open(VT_FILE,'rb') as f:
          num = num+int(f.read().split('\n')[0])
        os.system('echo '+str(num)+' >'+VT_FILE)
      else:
        os.system('echo '+str(num)+' >'+VT_FILE)
      num = 0 
      break
    else:
      wflag = 0
  write_res(list_res)

def get_vt_list(string):
  list_todo = []
  path_m = get_malware_dir(string)
  path_b = get_benign_dir(string) 
  df_b = pd.read_csv(path_b + 'vt_report.csv', sep=',')
  df_m = pd.read_csv(path_m + 'vt_report.csv', sep=',')
  list_m = list(df_m['sha256'])
  list_b = list(df_b['sha256'])
  paths = os.listdir(path_m)
  for m in paths:
    if len(m) == 64:
      if m in list_b:
        if os.path.exists(path_b+m):
          continue
#	  os.remove(path_b+m)
        shutil.move(path_m + m, path_b)
	if m+'.data' in paths:
          shutil.move(path_m + m + '.data', path_b)
        if m+'.xml' in paths:
          shutil.move(path_m + m + '.xml', path_b)
        continue
      elif m not in list_m:
        list_todo.append(m)
  return list(set(list_todo))

def main():
  import ctypes
  libc = ctypes.CDLL('libc.so.6')
  libc.prctl(1,15)
  vt_todo_list = get_vt_sum_lists()
  get_vt(vt_todo_list)
