#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Nankai University Information Security
#QiuKF 1055419050@qq.com
#create url upload classify data

from flask import Flask
import os
app=Flask(__name__)

@app.route('/count161.csv')
def get_class_new():
    csv_file=open('class_new_new.csv','r')
    data=csv_file.read()
    return data

if __name__=='__main__':
    app.run(debug=True,host='192.168.0.161')


