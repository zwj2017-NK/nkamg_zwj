#!/usr/bin/env python
#-*- coding: utf-8 -*-

from GetApkData import GetApkData
import sys
sys.path.append('..')
from core.settings import STRPATH
from core.settings import MALWARE_FOLDER, BENIGN_FOLDER
import psutil, datetime

def return_path(path, suffix):
  return "{0}/{1}/{2}/{3}/".format(path, suffix[0], suffix[1], suffix[2])

#def return_time():
#  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def extract():
  list_todo = []
  for i in list(STRPATH):
    for j in list(STRPATH):
      for k in list(STRPATH):
        list_todo.append(i + j + k)

  #with open('time.txt','ab') as f:
  #  f.write( return_time() + '\n')

  list_total = [return_path(MALWARE_FOLDER, i) for i in list_todo] + [return_path(BENIGN_FOLDER, j) for j in list_todo]
  GetApkData(36, list_total)

  #with open('time.txt','ab') as f:
  #  f.write(return_time() + '\n')
