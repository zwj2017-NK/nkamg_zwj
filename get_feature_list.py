#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import hashlib
import multiprocessing as mp

list_str = '0123456789abcdef'
#path_test = '/media/zhuwenjun/a046836e-2436-4362-a0f1-0023db7b7ad4/malware'

def check(suffix):
  list_except = []
  for path_hd in ['/data/benign', '/data/malware']:
    path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, suffix[0], suffix[1], suffix[2])
    paths = os.listdir(path_dir)
   
    list_sha256 = list(set([i[:64] for i in paths if len(i) >= 64]))
    
    for sha256 in list_sha256:
      if os.path.exists(path_dir + sha256 + '.data') and os.path.exists(path_dir + sha256): 
        continue
      else:
        if os.path.exists(path_dir + sha256):
          list_except.append(path_dir + sha256)
        if os.path.exists(path_dir + sha256 + '.data'):
          list_except.append(path_dir + sha256 + '*')
    print path_dir
  return list_except

if __name__ == '__main__':
  pool = mp.Pool(32)
  list_path = []
  for first_dir in list_str:
    for second_dir in list_str:
      for third_dir in list_str:
        list_path.append(first_dir + second_dir + third_dir)

  for m in xrange(len(list_path) / 32 + 1):
    result = pool.map(check, list_path[32 * m : 32 * (m + 1)])
    with open('report_about_feature.txt','ab') as f:
      for each in result:
        if len(each) == 0:
          continue
        for path_str in each:
          if len(path_str) == 0:
            continue
          else:
            f.write(path_str + '\n')
  pool.close()

