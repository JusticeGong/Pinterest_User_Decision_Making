import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_pin_count(user):
	doc = requests.get('https://www.pinterest.com/' + user + '/pins/').text
	soup = BeautifulSoup(doc, 'html.parser')
	try:
		countStat = soup.select('div.countStat')
		pin_num = countStat[0].find('span', class_='value').contents[0]
		pin_num = int(pin_num.replace(',',''))
		return pin_num
	except:
		return 0

cols = ['id','user','url','dscp']

user_pins = []
with open('/Users/jacob/Desktop/Python/Pinterest/user_pins.txt') as f:
	data = f.readlines()
	for line in data:
		if line[:8].isdigit():
			user_pins.append(line)
		else:
			user_pins[-1] = user_pins[-1].rstrip('\n') + line
with open('/Users/jacob/Desktop/Python/Pinterest/user_pins_0.txt', 'w') as f:
	for line in user_pins:
		f.write(line)
   
df_pins = pd.read_csv('/Users/jacob/Desktop/Python/Pinterest/user_pins_0.txt', header=None, names=cols, sep='\t', usecols=['id','user'])         
df_pins = df_pins.groupby(['user']).count()
df_pins['user'] = df_pins.index

df_users = pd.read_csv('/Users/jacob/Desktop/Python/Pinterest/user_list_sample_Jacob.csv')
boolean = df_users['UserID'].isin(df_pins['user'])
missing_user = df_users.loc[~boolean, :]
del missing_user['Unnamed: 0']
missing_user.to_csv('/Users/jacob/Desktop/Python/Pinterest/missing_users.txt', index=False, header=False)

df_pins['real_count'] = df_pins['user'].map(get_pin_count)
df_pins.to_csv('/Users/jacob/Desktop/Python/Pinterest/user_pin_count.csv', index=False)

df_pins = pd.read_csv('/Users/jacob/Desktop/Python/Pinterest/user_pin_count.csv', header=0)
rate = (df_pins['id'] < df_pins['real_count'] * 0.95).mean()
print(rate)