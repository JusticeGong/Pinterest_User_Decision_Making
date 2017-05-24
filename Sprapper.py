#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:09:35 2017

@author: jacob
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import json
import requests
import re
import ast

def save_as_txt(jsonList, path):
	with open(path, 'w') as outfile:
		for line in jsonList:
			outfile.write(str(line) + '\n')

def generate_soup_list(url):
	driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	list = []
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(4)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
		html_source = driver.page_source
		data = html_source.encode('utf-8')

		soup = BeautifulSoup(data, 'html.parser')
		for a in soup.find_all('a', href=True):
			list.append(a)
	return list

def pin_scrp(url, label):
	token_index = 0
	token = ['AU3VC0Yq7Z5NXszfD_Q-cinnQjkxFMFeU0dVeQtECIPCvKA7AQAAAAA',
				'AQ2piSk8kl5132aDT2DZ8qKEUPnMFMFemf1JnhVECIPCvKA7AQAAAAA',
				'AS6Pd8eHzRxNdj_LcNHauo6sD5RzFMFeoQ_epx9ECIPCvKA7AQAAAAA',
				'AQusRQQWeWGgZaM9JTRThTHjr-pGFMFeowQAyi9ECIPCvKA7AQAAAAA',
				'AczBXXIby2Tu2bn13jGbLbR6LrsiFMFepHc2rMRECIPCvKA7AQAAAAA',
				'AUde6xxsuNjivtxo5M4SCUKxBUllFMFepcwex5hECIPCvKA7AQAAAAA',
				'AVSeZS_DN_5B9a1Y1HgQRQft5znMFMFepweMIoxECIPCvKA7AQAAAAA',
				'ATrQCmOIUAz6ukkw6kNlQj7SHq4VFMFeqXvhMqdECIPCvKA7AQAAAAA',
				'AVRq4ZbTaAE4q00tq16zC7eTJ8RVFMFeqtAdQ_ZECIPCvKA7AQAAAAA',
				'Af3BKJiwOw9lS5XEs_mWx4RfsSdNFMFerAbtZQ5ECIPCvKA7AQAAAAA',
				'AfMgEoG3qs9vjCHubsnnPnP-gLhjFMFerQKwXJtECIPCvKA7AQAAAAA',
				'AR3ZeR5cDDajJxqqrntLQriXHyw6FMFerw9wFMhECIPCvKA7AQAAAAA',
				'AQIa-PX708ItRjb4piodTXtnag3WFMFesW_j8AVECIPCvKA7AQAAAAA',
				'AfxD29fZCN14CPZgbEYSBm3Hf9lTFMFesnLNs9FECIPCvKA7AQAAAAA',
				'AdSPGm_9zgHmiAQviFSFaoC4tny3FMFeT2JMKqJECIPk9oA3RAAAAAA',
				'AWVr2_IM7jZE-rAO4QWCliJwkesVFMDGrdLs27lEBzHKMYBEGQAAAAA',
				'ATeXIR8_GQ40SWAmaKQvtWPjTrvMFMFem8eReWZECIPk9oA3RAAAAAA',
				'AUssPocFsfa17yR3pmI7Ja4Ks0NCFMFenxO3QCBECIPk9oA3RAAAAAA',
				'AY0Ok6ZzuN9-tRboSAAOTHXqxMrVFMFes2xoSltECIPk9oA3RAAAAAA',
				'ATAzL5cngcJXWfrGxlN5GKS2xCo3FMFeveE2dO9ECIPk9oA3RAAAAAA',
				'AQnKqwG127Jfg5x8oqsb0rBJMP8KFMFeypTZrEpECIPk9oA3RAAAAAA',
				'AW-oPTz61jsBKfhq1dJ1sO37ocVNFMFfLrAXjCVECIW5QaA3KgAAAAA',
				'AeYvhWwuvCsNmdZ-isjmiLK11RgcFMFfNRcU9qVECIW5QaA3KgAAAAA',
				'ASzD9l9ErTGMawNeMyZXio650YO0FMFfREcOVY1ECIW5QaA3KgAAAAA',
				'AauL8lJCRXz9_APUCTJ-BAnmHkYlFMFfRoSjKVRECIW5QaA3KgAAAAA',
				'AcuJ7ZD-vwtLDrOK5hRze7Iz4tkoFMFfSCaclXJECIW5QaA3KgAAAAA',
				'AUG_-wvAgt1XVW6EYnU5orlhSkPRFMFfSdoXwYRECIW5QaA3KgAAAAA',
				'AXW2jgfdX9yCwj-ksyG1945A7_rZFMFfTTVLBQFECIW5QaA3KgAAAAA',
				'AeaFbXVFydB7wQWzvKW6i-GSm38pFMFfYbktddRECIYkVgAtZAAAAAA',
				'ASPSC5TXZiAsZNWoXwQeu-VUpcVeFMFfZBLhxxZECIYkVgAtZAAAAAA',
				'ATrswK40hpYZDVCZFSrJgmZIwAHVFMFfZYKMFDZECIYkVgAtZAAAAAA',
				'ATf9RV5uZm-HXtny64b5e7P6huFqFMFfZx1PViNECIYkVgAtZAAAAAA',
				'Aa4l9MmDkEE_Wv7J-UoraW4DB5IfFMFfeQYcuaJECIYkVgAtZAAAAAA',
				'AUciKZnAnRa6B2ywlj71IVyDjdb7FMFff7w6Jo5ECIYkVgAtZAAAAAA',
				'AegvJViSEwNiZjGbLKxzhT1hwmLWFMFfgexi5yZECIYkVgAtZAAAAAA',
				'AUQetWGs76BXlydaMkz_5iuFq0IIFMFfhFsyf5xECIYkVgAtZAAAAAA',
				'AcfXuWs40DRjgU0CvJFz-A0PN4VZFMFfhpqS2D9ECIYkVgAtZAAAAAA',
				'ATaq-33RlZDpENvRMKY9zh9t5_LYFMFfp0uWfMFECIYkVgAtZAAAAAA',
				'AdIe80E-RxI4CUBkWnvdjwXbVAKeFMFfqzH69YVECIYkVgAtZAAAAAA']
	list = generate_soup_list(url)
	pins = []
	for a in list:
		if re.match(r'^/pin/', a['href']):
			id = a['href'].lstrip('/pin/').rstrip('/')

			while True:
				url = 'https://api.pinterest.com/v1/pins/' + id +\
					'/?access_token=' + token[token_index] + '&fields=id%2Ccreated_at'
				response = requests.get(url).text
				if 'message' not in response:
					break
				else:
					token_index += 1

			tstpStr = json.loads(response)['data']['created_at']
			tstp = datetime.strptime(tstpStr, '%Y-%m-%dT%H:%M:%S')
			if datetime.now() - tstp > timedelta(days=60):
				continue

			img_url = a.img['src']

			jsonStr = '{"pinID": "' + id + '", "img": "' + img_url + '", "label": "'\
						+ label + '", "timestamp": "' + str(tstp) + '"}'
			pins.append(jsonStr)
	return pins

def board_scrp(url):
	list = generate_soup_list(url)
	boards = []
	for a in list:
		if re.match(r'^/', a['href']) and len(a['href'])>4:
			boards.append(a['href'])
	return boards

if __name__ == '__main__':
	pinLabel = ['diy', 'makeover', 'ideas']
# , 'grey', 'living%20room', 'design',\
# 		'repurposed', 'pallet', 'modern', 'bedroom', 'unique', 'rustic', 'patio',\
# 		'outdoor', 'vintage', 'industrial', 'wood', 'refinishing'
	for label in pinLabel:
		l = re.sub('%20','',label)
		url = 'https://www.pinterest.com/search/pins/?q=furniture%20' + label
		pins= pin_scrp(url, l)
		save_as_txt(pins, '/Users/jacob/Desktop/Python/Pinterest/pinID/' + l + '_ids.txt')

		# infile = open('/Users/jacob/Desktop/Python/Pinterest/pinIDs/' + l + '_ids.txt')
		# pins = infile.readlines()
		# infile.close()
		# repins = {}
		# for pin in pins:
		# 	for key in ast.literal_eval(pin):
		# 		id = key
		# 	boards = board_scrp('http://www.pinterest.com/pin/' + id + '/repins')
		# 	repins.update({id: []})
		# 	for board in boards:
		# 		repins.setdefault(id,[]).append(board)
		# with open('/Users/jacob/Desktop/Python/Pinterest/repins/' + l + '_repins.txt') as f:
		# 	f.write(str(repins))