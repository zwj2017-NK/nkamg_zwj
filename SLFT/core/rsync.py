#-*- coding: utf-8 -*-

from settings import VT_FOLDER
import subprocess
import shutil
import os

def rsync(src_ip, src_path, src_backup, des_username='nkamg', des_password='############', des_ip='###########', des_port='123456666666', des_path='/data/daily_json/'):
  path_json = os.listdir(VT_FOLDER)
  for o in path_json:
    if len(o) > 8 and 'json' in o:
      shutil.move(VT_FOLDER + o, src_path)
      os.rename(src_path + o, src_path + o[:-5] + '_' + src_ip.split('.')[-1] + '.json')
  cmd = 'sshpass -p \'' + des_password + '\' rsync -av --progress -e \'ssh -p ' + des_port + '\' ' + src_path + ' ' + des_username + '@' + des_ip + ':' + des_path
  print cmd
  subprocess.call(cmd, shell=True)
  os.popen('mv ' + src_path + '*.json ' + src_backup)

if __name__ == '__main__':
  rsync('192.168.0.115', '/data/vt/experiment/','/data/vt/backup/')
