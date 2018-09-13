#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import hashlib
import multiprocessing as mp

def get_sha256(x):
  f = codecs.open(x, 'rb')
  sh = hashlib.sha256()
  sh.update(f.read())
  sha256=sh.hexdigest()
  return sha256

def check(prefix):
  list_except = []
  for path_hd in ['/data/benign', '/data/malware']:
    path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, prefix[0], prefix[1], prefix[2])
    paths = os.listdir(path_dir)
    for item in paths:
      if 'xml' in item or 'data' in item or 'csv' in item:
        continue
      if len(item) == 64:
        sha256 = get_sha256(path_dir + item)
        if sha256 <> item:
          list_except.append(path_dir + item)
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
  result = pool.map(check, list_path)
  with open('report_about_sample.txt','wb') as f:
    for each in result:
      if len(each) == 0:
        continue
      f.write(each + '\n')
  pool.close()

if __name__ == '__main__':
  main()
