#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime

cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)

df_img = pd.read_csv('Data/1_source_pins.txt', sep='\t', header=0, names=['url', 'pinID', 'time', 'label'], usecols=['pinID', 'time'])
df_img['time'] = pd.to_datetime(df_img['time'])
df_img = df_img.loc[df_img['time'] <= datetime(year=2017, month=5, day=15), :]
pin_list = list(df_img['pinID'])

with open('Data/2_repin_users.txt') as f:
	lines = f.read().splitlines()[1:]

d = {}
for line in lines:
	pinID, temp = line.split('\t')
	temp = temp.lstrip('[').rstrip(']')
	temp = temp.replace("'", '')
	users = temp.split(', ')
	if pinID in pin_list:
		d.update({pinID: users})

fh = open('Data/5TwoAndHalfMonths.txt', 'w')
keys = list(d)
for i in range(len(keys)):
	for j in range(i+1, len(keys)):
		l_left = d[keys[i]]
		l_right = d[keys[j]]
		intersect = list(set(l_left) & set(l_right))
		fh.write(keys[i] + '|' + keys[j] + ':' + str(len(intersect)) + '\n')
		fh.write(keys[j] + '|' + keys[i] + ':' + str(len(intersect)) + '\n')
fh.close()