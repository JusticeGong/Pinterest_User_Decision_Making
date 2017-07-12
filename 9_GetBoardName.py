import os
import json
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

cwd = os.path.dirname(os.path.realpath(__file__))
thread_num = 8
base_url = 'www.pinterest.com/'

def get_boards(thread):
	if thread == thread_num - 1:
		temp_list = user_list[thread * trunk:]
	else:
		temp_list = user_list[thread * trunk : (thread+1) * trunk]

	jList = []
	for user in temp_list:
		url = base_url + user + '/?'
		rsp = requests.request("GET", url)
		soup = BeautifulSoup(rsp.text)

		l = []
		for a in soup.find_all('a', href=True, class_="boardLinkWrapper"):
			l.append(a)
		data = {}
		data[user] = l
		j = json.dump(data)
		jList.append(j)

	with open(os.path.join(cwd, 'user_boards.txt'), 'a') as outfile:
	    for j in jList:
	    	json.dump(j, outfile)

if __name__ == '__main__':
	user_list = []
	with open(os.path.join(cwd, 'user_list_distinct.csv'), 'r') as fh:
		lines = fh.readlines()[1:4]
		for line in lines:
			user_list.append(line.split(',')[1].rstrip('\n'))
	trunk = int(len(user_list)/thread_num)
	p = Pool(thread_num)
	p.map(get_boards, range(thread_num))