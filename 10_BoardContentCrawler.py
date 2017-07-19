from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import numpy as np
import pandas as pd
import os
from multiprocessing import Pool

cwd = os.path.dirname(os.path.realpath(__file__))
numofthreads = 8

def generate_soup_list(url):
	##Block chrome driver to download image to speed the crawling
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chromeOptions.add_experimental_option("prefs", prefs)

	# driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver = webdriver.Chrome(os.path.join(cwd, 'chromedriver'), chrome_options=chromeOptions)
	driver.maximize_window()
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	
	while True:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			#Please test if this sleep time is enough to load the webpage
			time.sleep(2)
		except:
			continue
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
	html = driver.page_source
	data = html.encode('utf-8')
	driver.close()
	soup = BeautifulSoup(data, 'html.parser')
	list = []
	for a in soup.find_all('a', href=True):
		if re.match(r'^/pin/', a['href']):
			list.append(a)
	return list

def reformat(list, board):
	result = ''
	for a in list:
		pinid = a['href'].lstrip('/pin/').rstrip('/')

		b = BeautifulSoup(str(a), "lxml")
		b = b.find_all('img')[0]
		img_alt = c['alt'].replace('\n', '')
		img_src = c['src']
		item = board + '\t' + pinid + '\t'+ img_src + '\t' + img_alt +'\n'
		result = result + item
	return result

def user_crawl(thread):
	if thread == numofthreads - 1:
		temp= df.iloc[thread * trunk:, :]
	else:
		temp = df.iloc[thread * trunk : (thread+1) * trunk, :]
	
	rf = open(os.path.join(cwd, 'board_pins.txt'), 'a', encoding='utf8')
	ef = open(os.path.join(cwd, 'board_pins_exceptions.txt'), 'a', encoding= 'utf8')
	for index, value in temp.iterrows():
		try:
			if value['board_id'] == np.nan:
				continue
			else:
				l = generate_soup_list(value['board_url'])
				result = reformat(l, value['board_id'])
				rf.write(result)
				del result
		except:
			ef.write(value['board_id'] + '\n')
			print("Exception =", thread, value['board_id'])

	del temp['board_url']
	return temp

if __name__ == '__main__':	
	df = pd.read_csv(os.path.join(cwd, 'sample_repins_board.txt'), sep='\t', header=0)
	df = df[['board_id', 'board_url']]
	df['board_pin'] = np.nan
	df['board_id'] = df['board_id'].astype(str)

	trunk = int(df.shape[0]/numofthreads)
	with Pool(numofthreads) as p:
		p.map(user_crawl, range(numofthreads))

	df_bp = pd.concat(df_list, axis=0)
	df_bp.to_csv(os.path.join(cwd, 'board_pins.txt'), index=False, header=True, sep='\t')
