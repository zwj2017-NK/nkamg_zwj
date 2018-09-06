#!/usr/bin/env python

import os

def init_dir():
  for i in range(16):
    for j in range(16):
      for k in range(16):
        
        os.popen("mkdir -p /data/malware/collection/"+hex(i)[2]+"/"+hex(j)[2]+"/"+hex(k)[2])
        os.popen("touch /data/malware/collection/"+hex(i)[2]+"/"+hex(j)[2]+"/"+hex(k)[2]+"/vt_report.csv")
        os.popen("mkdir -p /data/benign/collection/"+hex(i)[2]+"/"+hex(j)[2]+"/"+hex(k)[2])
        os.popen("touch /data/benign/collection/"+hex(i)[2]+"/"+hex(j)[2]+"/"+hex(k)[2]+"/vt_report.csv")
  
    print i
  
  os.popen("mkdir -p /data/auto/newfile")
  os.popen("mkdir -p /data/auto/download")
  os.popen("mkdir -p /data/auto/temp_file")
  os.popen("chmod -R 777 /data/")

