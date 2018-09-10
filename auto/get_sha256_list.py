#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import hashlib
import multiprocessing as mp
import re

def check(list_suffix):
  list_sha256 = []
  detect_pattern='[0123456789abcdef]{64}$'
  for suffix in list_suffix:
    for path_hd in ['/data/benign', '/data/malware']:
      path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, suffix[0], suffix[1], suffix[2])
      paths = os.listdir(path_dir)
      for filename in paths:
        if not re.match(detect_pattern, filename):
          continue      
        list_sha256.append(filename)
      #print path_dir
  return list_sha256

def main():
  print "Task 4: get_sha256_list.py"
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
  with open('/data/all_sha256_list.txt','wb') as f:
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
