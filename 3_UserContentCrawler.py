from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import json
import requests
import re
import ast

def save_as_txt(jsonList, path):
	with open(path, 'a') as outfile:
		for line in jsonList:
			outfile.write(str(line) + '\n')

def generate_soup_list(url):
	# driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver = webdriver.Chrome('chromedriver')
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	list = []
	while True:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(4)
		except:
			continue
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



def board_scrp(id):
	url = 'http://www.pinterest.com/pin/' + id + '/repins'
	list = generate_soup_list(url)
	users = '["'
	for a in list:
		if re.match(r'^/', a['href']) and len(a['href'])>4:
			userID = a['href'].lstrip('/').rstrip('/').split('/')[0]
			users = users + userID + '", "'
	users = users.rstrip(', "') + '"]'
	return users

if __name__ == '__main__':
	with open('user_list_sample.csv', 'r') as rf:
		for line in rf:
			line = line.strip()
			line = line.split(',')
			if line[1] != 'UserID':
				url = 'http://www.pinterest.com/' + line[1] + '/boards/'
				souplist = generate_soup_list(url)
				print(souplist)



	# repin_users = []
	# n = 0
	# for line in pins:
	# 	n = n + 1
	# 	print(n)
	# 	jObj = json.loads(line)
	# 	pinID = jObj['pinID']
	# 	pair = '{"pinID": "' + pinID + '", "users": ' + board_scrp(pinID) + '}'
	# 	repin_users.append(pair)
	# # save_as_txt(repin_users, '/Users/jacob/Desktop/Python/Pinterest/repin_users.txt')
	# save_as_txt(repin_users, 'repin_users_GZ.txt')