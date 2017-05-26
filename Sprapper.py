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
	token = ['Ab3z582fFq-UJGi7J8cq3sCy-LC4FMIG2wMcBa1ECeVcNcAo5QAAAAA',
				'Ae4SFazCrOXR-Ty1HryemIQVoIuhFMIG7hnbsnVECeWEAMBEkgAAAAA',
				'AbQZu3nqOMPLl6Mk2CfDHc_T9wgwFMIJcAywAFtECerGFSA2bwAAAAA',
				'ASfGLgfv3UG5PwpYvh18f4vkNWddFMIJhcbZzaZECerzmYA-rgAAAAA',
				'AewqKq5OrQRrbnvkCkP_zEeKmS2BFMIJsLjjpkNECetNmyA20gAAAAA',
				'ARtz-qfApXDF5qfCCCE63L4JiUNtFMIJwZSFVHJECetxSqBC-wAAAAA',
				'AQ8T3cv1UzNA-XfPMCiFk5ABKbceFMIJzy0hhp9ECeuN_aAo9AAAAAA',
				'ATZXPDHvpiEoENesAVAJRqSddgDLFMIJ22xl27FECeunckAr2gAAAAA',
				'AUq7hJ8HDIkmGL1-KXsB8CPjSs9MFMIJ7jB5CrJECevLG4A7lQAAAAA',
				'AXIF54XnOQESyIDpVSSm5gHv-gpKFMIKAfUjYSJECev4dyA5HQAAAAA',
				'AVGC_FiwmYPcRxcV0Y-6PVrE1xONFMIKEn7nxC1ECewawkBGYgAAAAA',
				'AXUBO4at2phWIp9CAazDLOFlqAewFMIKN9-4-OhECexpIYBHMQAAAAA',
				'ARmiw5l8eOeLvSrl-pHgI-_a2Es0FMIF_SvzuXFECIPk9oA3RAAAAAA',
				'AaWqeeQvj50-OsqMKYhOTeIsgx48FMIGDSHpNwZEBzHKMYBEGQAAAAA',
				'Abds7VdBN0YG3NLBp4Un7BeFPsGWFMIGItMv2zRECePZ3GBCIgAAAAA',
				'AWrpgsLX5DfvXnzX6lehjkygu_3eFMIGMgwyoSdECIYkVgAtZAAAAAA',
				'AZqcp2oo2aLzkPRVemmsmy1cHihtFMIGRQ-f0VRECeQhR8A32AAAAAA',
				'AecAeRpggyDOKMjD5yi2DRiFehtMFMIGVGovPiNECeRBpwA1bwAAAAA',
				'AYidnj6716_1HcgttS0inYrTK8k8FMIGZmtFF6NECeRnTeBGzgAAAAA',
				'AZHSp0gpAUVXZryrhWFCCPxrS5CEFMIGjZA3p6lECeS5tcAx1wAAAAA',
				'AUxhDuK1u2-O-5FGC5z7LHd5cdX1FMIGtKJXeK1ECeULsSAxUAAAAAA',
				'AU2BMJxwTSq5c-aQ1AahI2wsGOuGFMIGx-2ZWZNECeU0BmA7LAAAAAA']
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
	pinLabel = ['diy']
# , 'makeover', 'ideas', 'grey', 'living%20room', 'design',\
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