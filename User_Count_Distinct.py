userlist = []
with open('user_list.txt', 'a') as wf:
	with open('repin_users.txt', 'r', encoding='utf8') as rf:
		for line in rf: