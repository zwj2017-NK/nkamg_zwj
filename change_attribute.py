#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

def change_attribute(list_path):
  for path_hd in list_path:
    pass
    #os.system('chown nkamg -R ' + path_hd)
    #os.system('chgrp nkamg -R ' + path_hd)
    #os.system('chmod 644 -R ' + path_hd)
  

def chmod_dir(path_list):
  for path_hd in path_list:
    for i in strpath:
      for j in strpath:
        for k in strpath:
          path_dir = "{0}/{1}/{2}/{3}".format(path_hd, i, j, k)
          os.system('chmod 744 ' + path_dir)
          print i+j+k
        path_dir = "{0}/{1}/{2}".format(path_hd,i,j)
        os.system('chmod 744 ' + path_dir)
        print i+j
      path_dir = "{0}/{1}".format(path_hd, i)
      os.system('chmod 744 ' + path_dir)
      print i
   
if __name__ == '__main__':
  path_malhd = '/data/malware'
  path_benhd = '/data/benign'
  change_attribute([path_malhd, path_benhd])
  chmod_dir([path_malhd, path_benhd])
