import json
import re
n = 0
userlist = []
with open('user_list.txt', 'a') as wf:
	with open('repin_users_grp.txt', 'r', encoding='utf8') as rf:
		lines = rf.readlines()
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
				if u not in userlist:
					userlist.append(u)
			n = n + 1
			print(n)
			print(userlist)