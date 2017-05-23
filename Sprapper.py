#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:09:35 2017

@author: jacob
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time 
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

def pin_scrp(url):
    list = generate_soup_list(url)
    pins = []
    for a in list:
        if re.match(r'^/pin/', a['href']):
            id = a['href'].lstrip('/pin/').rstrip('/')
            img_url = a.img['src']
            # url = 'https://api.pinterest.com/v1/pins/' + id +\
            #     '/?access_token=AWVr2_IM7jZE-rAO4QWCliJwkesVFMDGrdLs27lEBzHKMYBEGQAAAAA&fields=id%2Ccreated_at%2Cimage'
            # response = requests.get(url)
            pins.append({id:img_url})
            # text.append(response.text)
    return pins#, text

def board_scrp(url):
	list = generate_soup_list(url)
	boards = []
	for a in list:
		if re.match(r'^/', a['href']) and len(a['href'])>4:
			boards.append(a['href'])
	return boards

if __name__ == '__main__':
	pinLabel = ['diy', 'makeover', 'ideas', 'grey', 'living%20room', 'design',\
		'repurposed', 'pallet', 'modern', 'bedroom', 'unique', 'rustic', 'patio',\
		'outdoor', 'vintage', 'industrial', 'wood', 'refinishing']

	for label in pinLabel:
		# url = 'https://www.pinterest.com/search/pins/?q=furniture%20' + label
		# pins= pin_scrp(url)
		# save_as_txt(pins, '/Users/jacob/Desktop/Python/Pinterest/pinIDs/' + re.sub('%20','',label) + '_ids.txt')

		infile = open('/Users/jacob/Desktop/Python/Pinterest/pinIDs/' + re.sub('%20','',label) + '_ids.txt')
		pins = infile.readlines()
		infile.close()
		repins = {}
		for pin in pins:
			for key in ast.literal_eval(pin):
				id = key
			boards = board_scrp('http://www.pinterest.com/pin/' + id + '/repins')
			repins.update({id: []})
			for board in boards:
				repins.setdefault(id,[]).append(board)
		with open('/Users/jacob/Desktop/Python/Pinterest/repins/' + re.sub('%20','',label) + '_repins.txt') as f:
			f.write(str(repins))