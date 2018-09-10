#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import re
from multiprocessing import Process,Pool
import os
import pandas as pd
import time
import sys
SAMPLES_PATH='/data/malware/'
#SAMPLES_PATH='/data/benign/'
def get_sample_sha256(sample_path):
  compute_sha256=os.popen('sha256sum '+sample_path)
  sha256=((compute_sha256.read()).split())[0]
  return sha256 
 
def check_sha256(first_dir):
  print 'Run task %s (%s)...' % (first_dir, os.getpid())
  incorrect_sha256_samples=[]
  detect_pattern='[0123456789abcdef]{64}$'
  child_dir=make_file_dir(first_dir)
  
  for each_dir in child_dir:
    files=os.listdir(SAMPLES_PATH+each_dir)
    for each_file in files:
      if re.match(detect_pattern, each_file):
        #print each_dir+each_file
        if each_file!=get_sample_sha256(SAMPLES_PATH+each_dir+each_file):
          print SAMPLES_PATH+each_dir+each_file
          incorrect_sha256_samples.append(SAMPLES_PATH+each_dir+each_file)
  print incorrect_sha256_samples
  
def make_file_dir(first):
  ret=[]
  chr_list=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  tmp=''
  for second in chr_list:
    two='/'+second
    for third in chr_list:
      three=two+'/'+third+'/'
      ret.append(first+three)
  return ret
  
def main():
  print('Parent process %s.' %os.getpid())
  first_dir=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  p=Pool(16)
  for each in first_dir:
    p.apply_async(check_sha256,args=(each,))
  p.close()
  p.join()
  
if __name__=='__main__':
  main()
