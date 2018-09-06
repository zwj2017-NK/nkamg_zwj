#-*- coding: utf-8 -*-

from multiprocessing import Process
import json
import pandas as pd
import multiprocessing as mp
import os
import sys
import shutil
from core.settings import DATA_FOLDER
from core.settings import MALWARE_FOLDER
from core.settings import BENIGN_FOLDER
from core.settings import VT_ERROR_REPORT 
from core.settings import get_malware_dir
from core.settings import get_benign_dir

reload(sys)
sys.setdefaultencoding('utf-8') 
 
columns = ['sha256','sha1','md5','type','scan_date','positives','Bkav','ahnlab','TotalDefense','MicroWorld-eScan','nProtect','CMC','CAT-QuickHeal',\
           'eTrust-Vet','McAfee','Malwarebytes','VIPRE','Prevx','Paloalto','TheHacker','BitDefender','K7GW','K7AntiVirus','Invincea',\
           'Baidu','Agnitum','F-Prot','SymantecMobileInsight','Symantec','Norman','ESET-NOD32','TrendMicro-HouseCall','Avast','eSafe',\
           'ClamAV','Kaspersky','Alibaba','NANO-Antivirus','ViRobot','AegisLab','ByteHero','Rising','Ad-Aware','Trustlook','Sophos',\
           'Comodo','F-Secure','DrWeb','Zillya','AntiVir','TrendMicro','McAfee-GW-Edition','NOD32','VirusBuster','Emsisoft','SentinelOne',\
           'Cyren','Jiangmin','Webroot','Avira','PCTools','Fortinet','Antiy-AVL','Kingsoft','Endgame','Arcabit','SUPERAntiSpyware',\
           'ZoneAlarm','Avast-Mobile','Microsoft','Commtouch','AhnLab-V3','ALYac','AVware','MAX','VBA32','Cylance','WhiteArmor',\
           'Baidu-International','eScan','Zoner','Tencent','Yandex','Ikarus','eGambit','GData','AVG','Cybereason','Panda','CrowdStrike',\
           'Qihoo-360']

def check(filepath, sha256):
  df = pd.read_csv(filepath, sep=',')
  list_sha256 = list(df['sha256'])
  if sha256 in list_sha256:
    return False
  else:
    return True

def write_malware(list_dict):
  for dict_csv in list_dict:
    try:
      prex = dict_csv['sha256'][0][:3]
      file_path = get_malware_dir(prex)+'vt_report.csv'
    except Exception,e:
#      print str(e) + '读sha256失败'
      pass
    try:
      df = pd.DataFrame(dict_csv, columns=columns)
      if os.path.exists(file_path):
        if check(file_path, dict_csv['sha256'][0]):
          df.to_csv(file_path, index=False, sep=',', mode='a', header=False, columns = columns)
      else:
        df.to_csv(file_path, index=False, sep=',', mode='a', columns = columns)
    except Exception,e:
#      print str(e)
      pass
    print str(os.getpid()) +  '$$$$$$$$$$$$' + dict_csv['sha256'][0] + ' succeed ' + file_path

def write_benign(list_dict):
  for dict_csv in list_dict:
    try:
      prex = dict_csv['sha256'][0][:3]
      file_path = get_benign_dir(prex)+'vt_report.csv'
    except Exception,e:
#      print str(e) + '读sha256失败'
      pass
    try:
      df = pd.DataFrame(dict_csv, columns=columns)
      if os.path.exists(file_path):
        if check(file_path, dict_csv['sha256'][0]):
          df.to_csv(file_path, index=False, sep=',', mode='a', header=False, columns = columns)
      else:
        df.to_csv(file_path, index=False, sep=',', mode='a', columns = columns)
    except Exception,e:
      pass
#      print str(e)
    print str(os.getpid()) +  '$$$' + dict_csv['sha256'][0] + ' succeed ' + file_path

#writing the result of vt to vt_report.csv which is located in the dir(benign/malware)
def write_csv(temp,n=16):
  #temp = [(json,sha256)]
  count_mal = 0
  count_ben = 0
  malware_res = []
  benign_res = []
  for i in temp:
    dict_csv = {'sha256':[],'sha1':[],'md5':[],'type':[],'scan_date':[],'positives':[],'ahnlab':[],'TotalDefense':[],'MicroWorld-eScan':[],'nProtect':[],\
                'CMC':[],'CAT-QuickHeal':[],'eTrust-Vet':[],'McAfee':[],'Malwarebytes':[],'VIPRE':[],'Prevx':[],'Paloalto':[],'TheHacker':[],\
                'BitDefender':[],'K7GW':[],'K7AntiVirus':[],'Invincea':[],'Baidu':[],'Agnitum':[],'F-Prot':[],'SymantecMobileInsight':[],'Symantec':[],\
                'Norman':[],'ESET-NOD32':[],'TrendMicro-HouseCall':[],'Avast':[],'eSafe':[],'ClamAV':[],'Kaspersky':[],'Alibaba':[],'NANO-Antivirus':[],\
                'ViRobot':[],'AegisLab':[],'ByteHero':[],'Rising':[],'Ad-Aware':[],'Trustlook':[],'Sophos':[],'Comodo':[],'F-Secure':[],'DrWeb':[],\
                'Zillya':[],'AntiVir':[],'TrendMicro':[],'McAfee-GW-Edition':[],'NOD32':[],'VirusBuster':[],'Emsisoft':[],'SentinelOne':[],'Cyren':[],\
         	'Jiangmin':[],'Webroot':[],'Avira':[],'PCTools':[],'Fortinet':[],'Antiy-AVL':[],'Kingsoft':[],'Endgame':[],'Arcabit':[],'SUPERAntiSpyware':[],\
                'ZoneAlarm':[],'Avast-Mobile':[],'Microsoft':[],'Commtouch':[],'AhnLab-V3':[],'ALYac':[],'AVware':[],'MAX':[],'VBA32':[],'Cylance':[],\
                'WhiteArmor':[],'Baidu-International':[],'eScan':[],'Zoner':[],'Tencent':[],'Yandex':[],'Ikarus':[],'eGambit':[],'GData':[],'AVG':[],\
        	'Cybereason':[],'Panda':[],'CrowdStrike':[],'Qihoo-360':[],'Bkav':[]}
    try:
      dict_csv['sha256'].append(i[1][:64])                              
      dict_csv['sha1'].append(i[0]['sha1'])                                 
      dict_csv['md5'].append(i[0]['md5'])                                    
      dict_csv['scan_date'].append(i[0]['scan_date'])                        
      dict_csv['positives'].append(i[0]['positives'])
      dict_csv['type'].append('apk')
      flag = 0
      for j in columns[6:]:
        if j in i[0]['scans'].keys():
          if i[0]['scans'][j]['result'] == None:
            dict_csv[j].append(u'')
          else:
            flag = 1
            dict_csv[j].append(i[0]['scans'][j]['result'])
        else:
          dict_csv[j].append(u'')
    except Exception,e:
      with open(VT_ERROR_REPORT,'a') as d:
        d.write(i[1] + '\n')
      continue
    if flag == 1:
      malware_res.append(dict_csv)
    else:
      benign_res.append(dict_csv)

  write_malware(malware_res)
  write_benign(benign_res)
 
#  count_mal = count_mal + len(malware_res)
#  count_ben = count_ben + len(benign_res)

#  with open(DATA_FOLDER+'result.txt','a') as gh:
#    gh.write(str(count_mal) + '  ' + str(count_ben) + '\n')

