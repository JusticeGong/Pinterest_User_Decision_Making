#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from concurrent.futures import ProcessPoolExecutor

cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)

def text_generator(pinID):
	url = 'https://www.pinterest.com/pin/' + pinID
	try:
		response = requests.get(url).text
		soup = BeautifulSoup(response, 'html.parser')
		first_pin = soup.find('a', href='/pin/'+pinID+'/')
		img = first_pin.find('img')
		dscp = ''
		dscp += img['alt'].replace('\t', ' ').replace('\n', ' ')
		
		temp = df_repins.loc[df_repins['pinID']==pinID, ['description']]
		temp = [d.replace('\t', ' ').replace('\n', ' ') for d in list(temp['description'])]
		temp = [d for d in temp if fuzz.partial_ratio(d, dscp) < 80]
		dscp += ' '.join(temp)

		return dscp
	except:
		return ''
	
if __name__ == '__main__':
	df_original = pd.read_csv('Data/1_source_pins.txt', sep='\t', header=None, names=['url', 'pinID', 'time', 'label'],
							usecols=['pinID'])
	original_pins = list(df_original['pinID'])
	df_repins = pd.read_csv('Data/8_sample_repins_board.txt', sep='\t', header=0, usecols=['pinID', 'description'])
	
	with ProcessPoolExecutor() as executor, open('Data/14_original_text.txt', 'w') as fh:
		for pin, dscp in zip(original_pins, executor.map(text_generator, original_pins)):
			fh.write(pin + '|' + dscp + '\n')
			print(pin)