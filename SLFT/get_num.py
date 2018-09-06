#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Nankai University
#Email:1103466626@qq.com
#date:2018.09.01

from core.settings import STRPATH
from core.settings import MALWARE_FOLDER
from core.settings import BENIGN_FOLDER
import os

def count_3(path):
  list_sha256 = []
  total_num = 0
  for i in list(STRPATH):
    for j in list(STRPATH):
      for k in list(STRPATH):
        str_path = "{0}/{1}/{2}/{3}/".format(path, i, j, k)
        lines = os.listdir(str_path)
        for line in lines:
	  if 'data' in line:
	    continue
	  if 'xml' in line:
	    continue
	  if 'csv' in line:
	    continue
	  total_num = total_num + 1
          list_sha256.append(line)
  with open('todo.txt', 'ab') as f:
    for item in list(set(list_sha256)):
      f.write(item + '\n')

def count_1(list_path):
  total_num = 0
  list_sha256 = []
  for path in list_path:
    lines = os.listdir(path)
    for line in lines:
      if 'data' in line:
	continue
      if 'xml' in line:
	continue
      if 'csv' in line:
	continue
      total_num = total_num + 1
      list_sha256.append(line)
  with open('todo.txt','ab') as g:
    for item in list(set(list_sha256)):
      g.write(item + '\n')

def remove_duplication():
  with open('todo.txt','rb') as h:
    temp = h.read().split('\n')
    temp.remove('')
  list_todo = list(set(temp))
  with open('todo.txt','wb') as f:
    for i in list_todo:
      f.write(i + '\n')
  print len(list_todo)

def main():
  count_3(MALWARE_FOLDER)
  count_3(BENIGN_FOLDER)
  remove_duplication() 

if __name__ == '__main__':
  main()



