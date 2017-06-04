import json
import re
n = 0
userlist = []
with open('user_list.txt', 'a') as wf:
	with open('repin_users.txt', 'r', encoding='utf8') as rf:
		lines = rf.readlines()
		for line in lines:
			line = line.rstrip('\n')
			line = re.sub('"users" ', '"users": ', line)
			line = line.replace('["]', '[]')
			line = json.loads(line)
			n = n + 1
			print(n)
			print(line['users'][0])