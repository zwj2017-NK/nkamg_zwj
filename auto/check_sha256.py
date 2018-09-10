#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Nankai University Information Security
#QiuKF 1055419050@qq.com
#check the samples' sha256 
#record incorrect samples

import re
from multiprocessing import Process,Pool,Lock
import os
import pandas as pd
import time
import sys

SAMPLES_PATH='/data/malware/'
DELETED_SAMPLES_SHA256='/home/nkamg/QiuKF_test/sha256_uncorrect_list.csv'
DIR_CHR=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
#SAMPLES_PATH='/data/benign/'
lock=Lock()

def get_sample_sha256(sample_path):
  #sample_path must be abs path
  compute_sha256=os.popen('sha256sum '+sample_path)
  sha256=((compute_sha256.read()).split())[0]
  #compute_sha256.read() e.g
  #'000fffd28bfe1e96a4c8f2763c752e5c0e7f4291defe62d44b30db5f50e40226  0/000fffd28bfe1e96a4c8f2763c752e5c0e7f4291defe62d44b30db5f50e40226\n'
  #print sha256
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
        correct_sha256=get_sample_sha256(SAMPLES_PATH+each_dir+each_file)
        if each_file!=correct_sha256:
          print SAMPLES_PATH+each_dir+each_file,' correct: ',correct_sha256
          incorrect_sha256_samples.append(SAMPLES_PATH+each_dir+each_file)
          os.popen('rm '+SAMPLES_PATH+each_dir+each_file)
  print incorrect_sha256_samples
  tmp_pd=pd.DataFrame(incorrect_sha256_samples)
  lock.arquire()
  tmp_pd.to_csv(DELETED_SAMPLES_SHA256,mode='a',header=False,index=False)
  lock.release()


def make_file_dir(first):
  ret=[]
  tmp=''
  for second in DIR_CHR:
    two='/'+second
    for third in DIR_CHR:
      three=two+'/'+third+'/'
      ret.append(first+three)
  return ret

def main():
  print "Task 2: check_sha256.py"
  print('Parent process %s.' %os.getpid())
  p=Pool(16)
  for each in DIR_CHR:
    p.apply_async(check_sha256,args=(each,))
  p.close()
  p.join()

if __name__=='__main__':
  main()
