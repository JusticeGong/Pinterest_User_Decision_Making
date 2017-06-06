import pandas as pd
import numpy as np
import re

#取所有user转成dataframe csv
n = 0
userlist = []
with open('user_list.csv', 'w') as wf:
	with open('repin_users_grp.txt', 'r', encoding='utf8') as rf:
		lines = rf.readlines()
		wf.write('UserID\n')
		for line in lines:
			line = line.rstrip('\n')
			line = line.split('\t')
			ul = line[1]
			ul = ul.replace('[', '')
			ul = ul.replace(']', '')
			ul = ul.replace(' ', '')
			ul = ul.replace("'", '')
			ul = ul.split(',')
			for u in ul:
				wf.write(u)
				wf.write('\n')
			n = n + 1
			print(n)
		rf.close()
	wf.close()

#去重
df = pd.read_csv('user_list.csv')
df = df.drop_duplicates(keep='first')
df.to_csv('user_list_distinct.csv')

#Sample
sample = df.sample(n=100)
sample.to_csv('user_list_sample.csv')

# with open('user_list_sample.csv', 'r') as rf:
# 	with open('user_list_sample.txt', 'w') as wf:
# 		for line in rf:
# 			line = line.strip()
# 			line = line.split(',')
# 			if line[1] != 'UserID':
# 				wf.write(line[1])
# 				wf.write('\n')
# 		wf.close()
# 	rf.close()