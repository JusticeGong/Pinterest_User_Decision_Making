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

def generate_soup_list(url):
	##Block chrome driver to download image to speed the crawling
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chromeOptions.add_experimental_option("prefs", prefs)

	# driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver = webdriver.Chrome('chromedriver', chrome_options=chromeOptions)
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

	soup = BeautifulSoup(data, 'html.parser')
	for a in soup.find_all('a', href=True, class_="pinLink pinImageWrapper"):
		# print(a.contents)
		list.append(a)
	# print(list)
	return list

def reformat(list, userid):
	jsonlist = ''
	for a in list:
		#This print is for testing.
		# print(a)
		pinid = a['href']
		pinid = pinid.split('/')
		pinid = pinid[2]
		# This print is for testing.
		# print(pinid)

		b = BeautifulSoup(str(a), "lxml")
		b = b.find_all('img')
		c = b[0]
		# print(c['alt'])
		# print(c['src'])
		img_alt = c['alt']
		img_src = c['src']
		item = pinid + '\t' + userid + '\t'+ img_src + '\t' + img_alt +'\n'
		jsonlist = jsonlist + item
	# print(jsonlist)
	return jsonlist

def user_crawl(thread_num):
	count_users = 0
	cmd = os.path.dirname(os.path.realpath(__file__))
	#Define your userlist source path here, dont forget to reomove the first line of the csv file
	with open(os.path.join(cmd + '/user_list_sample_1.csv'), 'r', encoding= 'utf8') as rf:
		#Define you save file path here
		with open (os.path.join(cmd + '/user_pins_' + str(thread_num) + '.txt'), 'a', encoding= 'utf8') as wf:
			with open (os.path.join(cmd + '/user_pins_exceptions.txt'), 'a', encoding= 'utf8') as ef:
				lines = rf.readlines()
				#N = number of thread
				n = 2
				l = int(len(lines) / n)
				lines = lines[thread_num*l+1 : (thread_num+1)*l+1]
				for line in lines:
					count_users = count_users + 1
					line = line.strip()
					line = line.split(',')
					url = 'http://www.pinterest.com/' + line[1] + '/pins/'
					try:
						pinlist = generate_soup_list(url)
						jsonlist = reformat(pinlist, line[1])
						# print(souplist)
						wf.write(jsonlist)
						print(thread_num, count_users)
					except:
						ef.write(line[1])
						ef.write('\n')
						print("Exception = ", thread_num, count_users)
			wf.close()
		rf.close()

if __name__ == '__main__':
	with Pool(2) as p:
		p.map(user_crawl, range(0, 2))
