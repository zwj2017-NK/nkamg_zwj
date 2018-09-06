#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

list_str = '0123456789abcdef'

#更改文件夹的权限为744
def chmod_dir(path_list):
  for path_hd in path_list:
    for i in list_str:
      for j in list_str:
        for k in list_str:
          path_dir = "{0}/{1}/{2}/{3}".format(path_hd, i, j, k)
          os.system('chmod 744 ' + path_dir)
          print i+j+k
    for i in list_str:
      for j in list_str:
        path_dir = "{0}/{1}/{2}".format(path_malhd,i,j)
        os.system('chmod 744 ' + path_dir)
        print i+j
    for k in list_str:
      path_dir = "{0}/{1}".format(path_malhd, k)
      os.system('chmod 744 ' + path_sample)
      print k

#更改文件目录下文件夹和文件的组属性
def changegroup(path_list):
  for path_hd in path_list:
    os.system('chgrp nkamg -R ' + path_hd)

#去掉文件的后缀，并且保证单层文件目录下以sha256命名文件的唯一性,删除其他没用的文件(*.py文件，client.conf文件，rsyncd.scrt文件)
def remove_apk_suffix(path_list):
  for path_hd in path_list:
    for i in list_str:
      for j in list_str:
        for k in list_str:
          path_dir = "{0}/{1}/{2}/{3}/".format(path_hd, i, j, k)
          paths = os.listdir(path_dir)
          for item in paths:
            if '.apk' in item:
              try:
                os.rename(item, item[:-4].lower())
              except Exception,e:
                os.remove(path_dir + item)
            if '.py' in item or 'rsync' in item or 'client' in item:
              os.remove(path_dir + item)
              
def main():
  path_malhd = '/data/malware'
  path_benhd = '/data/benign'
  remove_apk_suffix([path_malhd, path_benhd])
  chmod_dir([path_malhd, path_benhd])
  changegroup([path_malhd, path_benhd])
  
if __name__ == '__main__':
  main()
