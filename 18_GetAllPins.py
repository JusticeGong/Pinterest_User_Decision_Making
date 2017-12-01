from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import requests
import numpy as np
import pandas as pd
import re
import os
import concurrent.futures

from Tokens import token

token_index = 0
cwd = os.path.dirname(os.path.realpath(__file__))

def board_scrapper(url):
	global token_index
	while True:
		response = requests.get(url).text
		if 'message' not in response:
			break
		else:
			token_index = 0 if (token_index == len(token) - 1) else token_index+1

	d = {}
	j_rsps = json.loads(response)
	for j_pin in j_rsps['data']:
		img = j_pin['image']['original']['url']
		img = img.split('/')[-1]
		d.update({j_pin['id']: img})
	next_page = j_rsps['page']['next']
	return d, next_page

def generate_soup_list(url):
	##Block chrome driver to download image to speed the crawling
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chromeOptions.add_experimental_option("prefs", prefs)

	driver = webdriver.Chrome(os.path.join(cwd, 'chromedriver'), chrome_options=chromeOptions)
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	list = []

	html_source = driver.page_source
	data = html_source.encode('utf-8')
	driver.close()
	soup = BeautifulSoup(data, 'html.parser')
	board_wrapper = soup.find('div', class_='Grid')
	for a in board_wrapper.find_all('a', href=True, class_="boardLinkWrapper"):
		# print(a.contents)
		list.append(a['href'])
	# print(list)
	return list

def get_user_pins(user):
	global token_index
	url = 'https://www.pinterest.com/{}/boards/'.format(user)
	board_list = generate_soup_list(url)
	pins = {}
	for board in board_list[:1]:
		sub_url = 'https://api.pinterest.com/v1/boards{}pins/?access_token={}&fields=id%2Cimage'.format(board, token[token_index])
		d, next_page = board_scrapper(sub_url)
		pins.update(d)
		while next_page != None:
			d, next_page = board_scrapper(next_page)
			pins.update(d)
	return pins

def find_match(ori_img, users):
	newPins = {}
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for user, pins in zip(users, executor.map(get_user_pins, users)):
			for k, v in pins.items():
				if v == ori_img:
					newPins.update({user: k})
					break
	return newPins

def choose_longest_list(l):
	longest = []
	for i in l:
		if len(i) > len(longest):
			longest = i
	return longest

if __name__ == '__main__':
	df_repins = pd.read_csv(os.path.join(cwd, 'Data', '2_repin_users.txt'), header=0, sep='\t',
						   dtype={'pinID': str, 'users':str}, nrows=1)
	df_repins['users'] = df_repins['users'].map(lambda x: x.strip("[']").split("', '"))
	grouped = pd.DataFrame(df_repins.groupby(['pinID'])['users'].apply(list))
	grouped['users'] = grouped['users'].apply(choose_longest_list)
	grouped['pinID'] = grouped.index
	df_repins = grouped[['pinID', 'users']]
	del grouped
	df_repins['users'] = df_repins['users'].map(lambda x: list(set(x)))

	df_ori_pins = pd.read_csv(os.path.join(cwd, 'Data', '1_source_pins.txt'), header=None, sep='\t',
							  names=['img', 'pinID', 'timestamp', 'type'], usecols=['pinID', 'img'])
	df = df_repins.merge(df_ori_pins, on='pinID')

	df['img'] = df['img'].map(lambda url: url.split('/')[-1])

	df['newPins'] = np.vectorize(find_match)(df['img'], df['users'])
	del df['users']
	df.to_csv('/Users/jacob/Downloads/Pin_Match.txt', sep='\t', header=True, index=False)
