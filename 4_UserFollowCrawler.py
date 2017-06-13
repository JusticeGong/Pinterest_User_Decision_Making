from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import json
import requests
import re
import ast
import os
from multiprocessing import Pool

numofthreads = 5

def generate_soup_list(url):
	##Block chrome driver to download image to speed the crawling
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chromeOptions.add_experimental_option("prefs", prefs)

	# driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver = webdriver.Chrome('chromedriver', chrome_options=chromeOptions)
	driver.maximize_window()
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	list = []
	while True:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			#Please test if this sleep time is enough to load the webpage
			time.sleep(1)
		except:
			continue
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
	html_source = driver.page_source
	data = html_source.encode('utf-8')
	driver.close()
	soup = BeautifulSoup(data, 'html.parser')
	for a in soup.find_all('a', href=True):
		if a['href'] != "/":
			# print(a)
			# print(a.contents)
			list.append(a)
	# print(list)
	return list

def reformat(list, userid):
	followlist = ''
	followid = []
	for a in list:
		#This print is for testing.
		# print(a)
		uid = a['href']
		uid = uid.split('/')
		uid = uid[1]
		# print(uid)
		if uid != userid:
			followid.append(uid)
		# This print is for testing.
		# print(followid)
	followlist = userid + '\t' + str(followid) + '\n'
	# print(followlist)
	return followlist

def user_crawl(thread_num):
	count_users = 0
	cmd = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(cmd + '/user_list_sample.csv'), 'r', encoding='utf8') as rf:
		#Define you save file path here
		with open (os.path.join(cmd + '/user_followers_' + str(thread_num) + '.txt'), 'a', encoding= 'utf8') as wfer:
			with open(os.path.join(cmd + '/user_following_' + str(thread_num) + '.txt'), 'a', encoding='utf8') as wfing:
				lines = rf.readlines()
				#N = number of thread
				n = numofthreads
				l = int(len(lines) / n)
				print(l)
				lines = lines[thread_num*l : (thread_num+1)*l]
				for line in lines:
					count_users = count_users + 1
					line = line.strip()
					line = line.split(',')
					followerurl = 'http://www.pinterest.com/' + line[1] + '/followers/'
					followingurl = 'http://www.pinterest.com/' + line[1] + '/following/'
					followersoup = generate_soup_list(followerurl)
					followerlist = reformat(followersoup, line[1])
					# print(followerlist)
					wfer.write(followerlist)
					followingsoup = generate_soup_list(followingurl)
					followinglist = reformat(followingsoup, line[1])
					# print(followinglist)
					wfing.write(followinglist)
					print(thread_num, count_users)
		rf.close()

if __name__ == '__main__':
	with Pool(numofthreads) as p:
		p.map(user_crawl, range(0, numofthreads))