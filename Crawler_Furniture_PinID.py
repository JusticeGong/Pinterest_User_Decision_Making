from bs4 import BeautifulSoup
import requests
import re


url = "www.pinterest.com/search/pins/?q=furniture&rs=rs&eq=&etslf=2284&term_meta[]=furniture%7Crecentsearch%7Cundefined"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

a = soup.find_all('a')


print(a)

# urlname = []
# schoolname = []
#
# a = soup.find_all(href=re.compile("/cbb/schools/*"))
#
# for i in range(2, 479):
#     # print("Found the URL:", a['href'].split('/')[3])
#     # print(a.contents)
#     urlname.append(a[i]['href'].split('/')[3])
#     schoolname = schoolname + a[i].contents
# print(urlname)
# print(schoolname)
#
# year = []
#
#
# for a in soup.find_all('tr'):
#     b = a.find_all('td')
#     if b:
#         year = year + b[3].contents
# print(year)
#
# m = 0
# for i in year:
#     if int(i) < 2017:
#         urlname[m] = ''
#         schoolname[m] = ''
#     m = m + 1
#
# print(urlname)
# print(schoolname)
#
# urlname = [x for x in urlname if x]
# schoolname = [x for x in schoolname if x]
#
# print(urlname)
# print(schoolname)
#
# print(len(urlname))
# print(len(schoolname))
#
# with open('urlname.txt', 'w', encoding="utf8") as fu:
#     fu.write(str(urlname))
# fu.close()
#
# with open('schoolname.txt', 'w', encoding="utf8") as fs:
#     fs.write(str(schoolname))
# fs.close()
#
# # for i in range(1, len(schoolname)):
# #     school = dict(str[schoolname[i]],str(urlname[i]))
# #
# # print(school)
#
#
# ### Fina <a>
# # a = soup.find_all(href=re.compile("/cbb/schools/*"))
# # print(a)
# #
# # for i in range(1,len(a)):
# #     print(a[i].contents)
# #     print('-----------------------' + str(i))
# ###
#
#
# # for link in soup.find_all('a'):
# #     print(link.get('href'))