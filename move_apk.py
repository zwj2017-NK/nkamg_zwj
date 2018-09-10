#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import shutil
import multiprocessing as mp
import hashlib
import codecs

#把样本文件，特征文件，布局文件，从文件夹移动到三层目录下
PATH_SRC= '/data/test'
PATH_DES = '/data/malware'

def get_sha256(x):
  f = codecs.open(x, 'rb')
  sh = hashlib.sha256()
  sh.update(f.read())
  sha256=sh.hexdigest()
  return sha256

def return_path(path, filename):
  return "{0}/{1}/{2}/{3}/".format(path, filename[0], filename[1], filename[2])

def move_apk(list_filename):
  for filename in list_filename:
    if len(filename) < 64:
      continue

    path_file = PATH_SRC + '/' + filename
    if 'data' in filename:
      os.system('mv ' + path_file  + ' ' + return_path(PATH_DES, filename))
      print path_file + '.data'
      continue

    if 'xml' in filename:
      os.system('mv ' + path_file  + ' ' + return_path(PATH_DES, filename))
      print path_file + '.xml'
      continue

    sha256 = get_sha256(path_file)
    if sha256 == filename:
      os.system('mv ' + path_file + ' ' + return_path(PATH_DES, filename))
      print path_file

def main():
  list_filename = os.listdir(PATH_SRC)
  move_apk(list_filename)

if __name__ == '__main__':
  main()
~          
