#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Nankai University
#Email:1103466626@qq.com
#date:2018.09.01

from core.settings import APIKEYS
from core.settings import URL
from core.settings import VT_FOLDER
from core.settings import get_time, get_local_ip
from core.rsync import rsync
from core.mail import send_email
import multiprocessing as mp
import os
import time
import requests
import json
import re
import datetime
import random
import shutil

def get_report(total_num):
  with open(VT_FOLDER + 'todo.txt','rb') as f1:
    temp = f1.read().split('\n')
    temp.remove('')
  time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  if os.path.exists(VT_FOLDER + 'result_' + time_string[:10] + '.json'):
    with open(VT_FOLDER + 'result_' + time_string[:10] + '.json', 'rb') as f2:
      result_dict = json.load(f2)
      result_count = len(result_dict)
  else:
    result_count = 0
  todo_count = len(temp)
  info_head = '------Daily Mail------\n'
  info_middle = 'ip: ' + get_local_ip('enp2s0') + '\n' + 'total: '  + str(total_num) + '\n'
  info_tail = 'current: ' + str(todo_count) + '\n' + 'today: ' + str(result_count)
  return info_head + info_middle + info_tail 

def update_todo(list_res):
  if len(list_res) == 0:
    return
  regex = re.compile('\s+')
  with open(VT_FOLDER + 'todo.txt','rb') as f:
    list_todo = regex.split(f.read())
    list_todo.remove('')
  for i in list_res:
    try:
      if i[0] == 0 and i[1] == 0:
	continue
      list_todo.remove(i[1])
    except Exception,e:
      pass
  with open(VT_FOLDER + 'todo.txt','wb') as e:
    for j in list_todo:
      e.write(j + '\n')
  return
    
def write_res(list_res):
  if len(list_res) == 0:
    return
  if os.path.exists(VT_FOLDER + 'result_' + get_time() + '.json'):
    with open(VT_FOLDER + 'result_' + get_time()  +'.json', 'rb') as e:
      dict_total = json.load(e)
  else:
    dict_total = {}
  if len(list_res) == 0:
    return
  for i in list_res:
    if i[0] == 0 and i[1] == 0:
      continue
    dict_total[i[1]] = i[0]
  if len(dict_total.keys()) is not 0:
    str_json = json.dumps(dict_total)
    with open(VT_FOLDER + 'result_' + get_time() + '.json','w') as f:
      f.write(str_json)
  return
  
def do_task(temp, seq):
  try:
    params = {'apikey': APIKEYS[seq], 'resource': temp}
    k = 0
    while True:
      response = requests.get(URL, params=params)
      if response.status_code == 200:
        return (response.json(),temp)
      k = k + 1
      if k == 4:
        return (0, 0)
      time.sleep(15)
  except Exception,e:
    return (0,0)

def main():
  with open(VT_FOLDER + 'todo.txt', 'rb') as f:
    list_todo = f.read().split('\n')
  list_todo.remove('')
  total_num = len(list_todo)
  if os.path.exists(VT_FOLDER + 'result_' + get_time() + '.json'): 
    with open(VT_FOLDER + 'result_' + get_time() + '.json', 'rb') as g:
      dict_done = json.load(g)
  else:
    dict_done = {}
  list_done = dict_done.keys()
  for i in list_done:
    try:
      list_todo.remove(i)
    except Exception, e:
      pass
  with open(VT_FOLDER + 'todo.txt','wb') as h:
    for j in list_todo:
      h.write(j + '\n')

  print 'the task starts'
  list_res = []  
  flag = 0
  for k in range(len(list_todo)):
    tuple_res = do_task(list_todo[k], random.randint(0,57))
    list_res.append(tuple_res)
    if tuple_res[0] == 0 and tuple_res[1] == 0:
      flag = flag + 1
    else:
      print list_todo[k] + '--->' + 'succeed'
      flag = 0

    if k % 20 == 0:
      write_res(list_res)
      update_todo(list_res)
      list_res = []
      print "Flushing"

    if flag >= 200:
      write_res(list_res)
      update_todo(list_res)
      break
    if k == len(list_todo) - 1:
      write_res(list_res)
      update_todo(list_res)
  send_email(get_report(total_num))
  rsync('192.168.0.115', '/data/vt/experiment/','/data/vt/backup/')

if __name__ == '__main__':
  main()
