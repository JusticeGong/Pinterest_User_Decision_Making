import requests
import os
from multiprocessing import Pool
import time

numofthreads = 160

def downloader(thread_num):
	start = time.clock()
	cmd = os.path.dirname(os.path.realpath(__file__))
	f = open(os.path.join(cmd, 'image_list_Zheng.txt'))
	img_list = f.readlines()
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
		try:
			img_result = requests.get(url)
			filename = url.split('/')[-1]
			path = os.path.join(cmd, 'Images', user)
			if (not os.path.exists(path)):
				os.makedirs(path)
			with open(os.path.join(path, filename), 'wb') as file:
				file.write(img_result.content)
				file.close()
		except:
			with open('D:/Workplace/Pinterest_User_Decision_Making/ImageException/img_exceptions_' + str(thread_num) + '.txt', 'a') as file:
				file.write(line)
				file.close()
		n = n + 1
		print(thread_num, n)
	elapsed = (time.clock() - start)
	with open('D:/Workplace/Pinterest_User_Decision_Making/Thread_Time.txt', 'a') as file:
		record = str(numofthreads) + '\t' + str(trunk) + '\t' + str(elapsed) + '\n'
		file.write(record)
		file.close
	print("Done")

if __name__ == '__main__':
	p = Pool(numofthreads)
	p.map(downloader, range(0, numofthreads))