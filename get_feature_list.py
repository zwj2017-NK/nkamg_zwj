#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import hashlib
import multiprocessing as mp

def check(list_suffix):
  list_except = []
  for suffix in list_suffix:
    for path_hd in ['/data/benign', '/data/malware']:
      path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, suffix[0], suffix[1], suffix[2])
      paths = os.listdir(path_dir)
      for filename in paths:
        if len(filename) <> 64:
          continue
        if os.path.exists(path_dir + filename) and not os.path.exists(path_dir + filename + '.data'):
          list_except.append(filename)
      print path_dir
  return list_except

def main():
  list_str = list('0123456789abcdef')
  pool = mp.Pool(32)
  list_path = []
  for first_dir in list_str:
    for second_dir in list_str:
      for third_dir in list_str:
        list_path.append(first_dir + second_dir + third_dir)
  m = len(list_path) / 32
  list_task = [list_path[m * i : m * (i + 1)] for i in xrange(32)]
  result = pool.map(check, list_task)
  #print result
  with open('todo_list_for_feature.txt','ab') as f:
    for each in result:
      if len(each) == 0:
        continue
      for path_str in each:
        if len(path_str) == 0:
          continue
        else:
          f.write(path_str + '\n')
  pool.close()
  
if __name__ == '__main__':
  main()
