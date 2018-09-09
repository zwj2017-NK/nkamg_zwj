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
      return
    if 'data' in filename or 'xml' in filename:
      return
    path_file = PATH_SRC + '/' + filename
    sha256 = get_sha256(path_file)
    if sha256 == filename:
      os.system('mv ' + path_file + ' ' + return_path(PATH_DES, filename))
      print path_file
      if os.path.exists(path_file + '.data'):
        os.system('mv ' + path_file + '.data' + ' ' + return_path(PATH_DES, filename))
        print path_file + '.data'
      if os.path.exists(path_file + '.xml'):
        os.system('mv ' + path_file  + '.xml' + ' ' + return_path(PATH_DES, filename))
        print path_file + '.xml'

def main():
  #pool = mp.Pool(32)
  list_filename = os.listdir(PATH_SRC)
  #for seq in xrange(len(list_filename) + 1):
  #  pool.map(move_apk, list_filename[seq * 32 : (seq + 1) * 32])
  #pool.close()
  move_apk(list_filename)

if __name__ == '__main__':
  main()
