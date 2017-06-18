import requests
import os
from multiprocessing import Pool

numofthreads = 8

def downloader(thread_num):
	cmd = os.path.dirname(os.path.realpath(__file__))
	f = open(os.path.join(cmd, 'image_list_Zheng.txt'))
	img_list = f.readlines()[1:]
	f.close()
	trunk = int(len(img_list) / numofthreads)
	if thread_num == numofthreads - 1:
		img_list = img_list[thread_num * trunk:]
	else:
		img_list = img_list[thread_num * trunk : (thread_num+1) * trunk]
	n = 0
	for line in img_list:
		user, url = line.split(',')
		url = url.rstrip('\n')
		img_result = requests.get(url)
		filename = url.split('/')[-1]
		path = os.path.join(cmd, 'Images', user)
		if (not os.path.exists(path)):
			os.makedirs(path)
		try:
			with open(os.path.join(path, filename), 'wb') as file:
				file.write(img_result.content)
				file.close()
		except:
			with open('img_exceptions.txt', 'a') as file:
				file.write(line)
				file.close()
		n = n + 1
		print(thread_num, n)

if __name__ == '__main__':
	p = Pool(numofthreads)
	p.map(downloader, range(0, numofthreads))

