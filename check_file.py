#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
list_str = '0123456789abcdef'

def check(list_path):
  list_except = []
  for path_hd in list_path:
    for i in list_str:
      for j in list_str:
        for k in list_str:
          path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, i, j, k)
          paths = os.listdir(path_dir)

          for item in paths:
            if len(item) == 64:
              continue

            if '.data' in item and len(item) == 69:
              continue

            if '.xml' in item and len(item) == 68:
              continue

            if '.csv' in item and len(item) == 11:
              continue

            list_except.append(path_dir + item)
            if '.apk' in item:
              try:
                os.rename(item, item[:-4].lower())
              except Exception,e:
                os.remove(path_dir + item)

  with open('test_report.txt','wb') as f:
    for line in list_except:
      f.write(line + '\n')

if __name__ == '__main__':
  check(['/data/malware','/data/benign'])
