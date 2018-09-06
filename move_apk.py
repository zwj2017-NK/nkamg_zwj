#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import shutil
import multiprocessing as mp

#把apk文件从文件夹移动到三层目录下
path_src= '/data/test/'
path_des = '/data/malware'
def return_path(path_des, filename):
  return "{0}/{1}/{2}/{3}/".format(path_des, filename[0], filename[1], filename[2])

def move_apk(filename):
  if len(filename) < 64:
    return
  if os.path.exists(return_path(path_des,filename) + filename):
    return
  if 'download' in filename:
    os.system('mv ' + path_src + filename + ' ' + path_src + filename.split('sha256=')[-1])
    os.system('mv ' + path_src + filename.split('sha256=')[-1] + ' ' + return_path(path_des, filename.split('sha256=')[-1]))
  else:
    shutil.move(path_src + filename, return_path(path_des, filename))
  print return_path(path_des, filename) + filename

def main():
  pool = mp.Pool(32)
  list_filename = os.listdir(path_src)
  for seq in xrange(len(list_filename) + 1):
    pool.map(move_apk, list_filename[seq * 32 : (seq + 1) * 32])
  pool.close()  

if __name__ == '__main__':
  main()  
