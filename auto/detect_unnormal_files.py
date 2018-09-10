#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

SAMPLES_PATH='/data/malware/'

def detect():
  unnormal_list=[]
  detect_pattern='(([0123456789abcdef]{64})|(dex_date.csv)|(vt_report.csv)|([0123456789abcdef]{64}(.data|.xml)))$'
  normal_path=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  first_level=os.listdir(SAMPLES_PATH)
  for first_chr in first_level:
    if first_chr not in normal_path:
      print SAMPLES_PATH+first_chr+'/'
      unnormal_list.append(SAMPLES_PATH+first_chr+'/')
      continue
    second_level=os.listdir(SAMPLES_PATH+first_chr+'/')
    for second_chr in second_level:
      if second_chr not in normal_path:
        print SAMPLES_PATH+first_chr+'/'+second_chr+'/'
        unnormal_list.append(SAMPLES_PATH+first_chr+'/'+second_chr+'/')
        continue
      third_level=os.listdir(SAMPLES_PATH+first_chr+'/'+second_chr+'/')
      for third_chr in third_level:
        if third_chr not in normal_path:
          print SAMPLES_PATH+first_chr+'/'+second_chr+'/'+third_chr+'/'
          unnormal_list.append(SAMPLES_PATH+first_chr+'/'+second_chr+'/'+third_chr+'/')
          continue
        files=os.listdir(SAMPLES_PATH+first_chr+'/'+second_chr+'/'+third_chr+'/')
        for each_file in files:
          if not re.match(detect_pattern, each_file):
            print SAMPLES_PATH+first_chr+'/'+second_chr+'/'+third_chr+'/'+each_file
            unnormal_list.append(SAMPLES_PATH+first_chr+'/'+second_chr+'/'+third_chr+'/'+each_file)
  return unnormal_list

def del_unnormal_files(unnormal_list):
  for f in unnormal_list:
    os.popen("rm -fr " + f)

def main():
  print "Task-1: detect_unnormal_files.py"
  unnormal_list=detect()
  print  unnormal_list
  print len(unnormal_list)
  del_unnormal_files(unnormal_list)

if __name__=='__main__':
  main()
