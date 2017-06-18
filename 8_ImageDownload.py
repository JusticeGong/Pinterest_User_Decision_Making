import requests
import os
from multiprocessing import Pool

def downloader(thread):
	if thread == thread_num - 1:
		temp_list = img_list[thread * trunk:]
	else:
		temp_list = img_list[thread * trunk : (thread+1) * trunk]
	for line in temp_list:
		user, url = line.split(',')
		url = url.rstrip('\n')
		img_result = requests.get(url)
		filename = url.split('/')[-1]
		path = os.path.join(cmd, 'Images', user)
		if (not os.path.exists(path)):
			os.makedirs(path)
		with open(os.path.join(path, filename), 'wb') as file:
			file.write(img_result.content)

if __name__ == '__main__':
	cmd = os.path.dirname(os.path.realpath(__file__))
	f = open(os.path.join(cmd, 'image_list.txt'))
	img_list = f.readlines()[1:]
	f.close()
	
	thread_num = 6
	trunk = int(len(img_list)/thread_num)
	p = Pool(thread_num)
	p.map(downloader, range(thread_num))