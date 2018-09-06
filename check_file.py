#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import hashlib

list_str = '0123456789abcdef'

def get_sha256(x):
  f = codecs.open(x, 'rb')
  sh = hashlib.sha256()
  sh.update(f.read())
  sha256=sh.hexdigest()
  return sha256

def check(list_path):
  list_except = []
  for path_hd in list_path:
    for i in list_str:
      for j in list_str:
        for k in list_str:
          path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, i, j, k)
          paths = os.listdir(path_dir)

          for item in paths:
            sha256 = get_sha256(path_dir + item)
            if len(item) == 64 and item.lower() == item:
              if sha256 <> item:
                list_except.append((path_dir + item, 0))
              continue
            else:
              if len(item) == 64:
                try: 
                  if sha256 == item.lower():
                    os.rename(path_dir + item, path_dir + item.lower())
                  else:
                    list_except.append((path_dir + item, 11))
                except Exception,e:
                  list_except.append((path_dir + item, 12))
                continue

            if '.data' in item and len(item) == 69:
              continue

            if '.xml' in item and len(item) == 68:
              continue

            if '.csv' in item and len(item) == 11:
              continue

            
            if '.apk' in item:
              try:
                if sha256 == item[:-4].lower():
                  os.rename(item, item[:-4].lower())
                else:
                  list_except.append((path_dir + item,31))
                  continue
              except Exception,e:
                list_except.append((path_dir + item,32))
                continue
            list_except.append((path_dir + item,3))

  with open('test_report.txt','wb') as f:
    for line in list_except:
      f.write(str(line) + '\n')

if __name__ == '__main__':
  check(['/data/malware','/data/benign'])                                                                                                                                                                             1,3          顶端
