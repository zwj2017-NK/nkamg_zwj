# -*- coding: utf-8 -*-  
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd 
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import FuncFormatter, MaxNLocator 
import random

df1 = pd.read_csv('svm.csv', sep=',')
df2 = pd.read_csv('xgboost.csv', sep=',')
labels = list(df1['time'])
x = [i for i in range(36)]

def format_fn(tick_val, tick_pos):
    if int(tick_val) in x:
        return labels[int(tick_val)]
    else:
        return ''

y = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

y_p_m_svm = list(df1['precision_m'])
y_r_m_svm = list(df1['recall_m'])
y_f_m_svm = list(df1['f1-score_m'])
y_p_g_svm = list(df1['precision_g'])
y_r_g_svm = list(df1['recall_g'])
y_f_g_svm = list(df1['f1-score_g'])

y_p_m_xgb = list(df2['precision_m'])
y_r_m_xgb = list(df2['recall_m'])
y_f_m_xgb = list(df2['f1-score_m'])
y_p_g_xgb = list(df2['precision_g'])
y_r_g_xgb = list(df2['recall_g'])
y_f_g_xgb = list(df2['f1-score_g'])


fig = plt.figure(figsize=(300,200)) 
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(x)
plt.yticks(y)
plt.ylim(0.0,1.0)

plt.plot(x,y_p_m_svm, marker='o',mec='g',linestyle=':', label=u'Precision(m_svm)',linewidth=1)   
plt.plot(x,y_r_m_svm, marker='v', mec='g', linestyle=':', label=u'Recall(m_svm)',linewidth=1)   
plt.plot(x,y_f_m_svm, marker='x', mec='g', linestyle=':' , label=u'F-score(m_svm)',linewidth=1)   

#---------------------------------------------------------------------------------

plt.plot(x,y_p_g_svm, marker='o', mec='y', linestyle=':', label=u'Precision(g_svm)',linewidth=1)   
plt.plot(x,y_r_g_svm, marker='v', mec='y', linestyle=':', label=u'Recall(g_svm)',linewidth=1)   
plt.plot(x,y_f_g_svm, marker='x', mec='y', linestyle=':',  label=u'F-score(g_svm)',linewidth=1)

#---------------------------------------------------------------------------------

plt.plot(x,y_p_m_xgb, marker='+',mec='b', linestyle='-.', label=u'Precision(m_xgb)',linewidth=2)   
plt.plot(x,y_r_m_xgb, marker='*', mec='b', linestyle='-.', label=u'Recall(m_xgb)',linewidth=2)   
plt.plot(x,y_f_m_xgb, marker='s', mec='b', linestyle='-.', label=u'F-score(m_xgb)',linewidth=2)   

#---------------------------------------------------------------------------------

plt.plot(x,y_p_g_xgb, marker='+', mec='k', linestyle='-.', label=u'Precision(g_xgb)',linewidth=2)   
plt.plot(x,y_r_g_xgb, marker='*', mec='k', linestyle='-.',  label=u'Recall(g_xgb)',linewidth=2)   
plt.plot(x,y_f_g_xgb, marker='s', mec='k', linestyle='-.',  label=u'F-score(g_xgb)',linewidth=2)

#---------------------------------------------------------------------------------

plt.legend()
plt.gcf().autofmt_xdate()
plt.xlabel("Sample Time")  
plt.ylabel("Parameter Value")  
plt.title("SVM vs XGBOOST")  
plt.show()


