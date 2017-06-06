#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:09:35 2017

@author: jacob
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime, timedelta
import json
import requests
import re
import pandas as pd

def save_as_txt(jsonList, path):
	with open(path, 'a') as outfile:
		for line in jsonList:
			outfile.write(str(line) + '\n')

def generate_soup_list(url):
	# driver = webdriver.Chrome('/Users/jacob/chromedriver')
	driver = webdriver.Chrome('chromedriver')
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	list = []
	while True:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(4)
		except:
			continue
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
		html_source = driver.page_source
		data = html_source.encode('utf-8')

		soup = BeautifulSoup(data, 'html.parser')
		for a in soup.find_all('a', href=True):
			list.append(a)
	return list

def pin_scrp(url, label):
	token_index = 0
	token = ['Afz32BRh8gNvTk-kLK_8XlvzbuNIFMMv_bRRVKtEDFR_pSBBMwAAAAA',
				'AddzTdtGlkXHm5lK7aVqx94TBKZHFMMwDoaS4etEDFSitkA3owAAAAA',
				'Aan1IEOgH47TgvEtGXODh57yc1bdFMMwHIAXq8xEDFTAF0AswgAAAAA',
				'Ab-gP7-2LCoqghJbF6UxmeYHthKoFMMwKe8kQdVEDFTca6A4pwAAAAA',
				'AfK9cdnzwzVBUS638Wj_alpY6ERSFMMwN-nuf4VEDFT5tMApvQAAAAA',
				'AUzaKCx95hV3-atoA5ckeFcXP4m3FMMwR8coDVZEDFUa8oAqmwAAAAA',
				'ATj09G6hf_bVieT1Hs-Ar1xfIixOFMMwXl5OOy9EDFVKKoA--QAAAAA',
				'AafJZm0-fDBn5SIdgjX18aDxv2VpFMMwaTlCtEJEDFVhFaA6ugAAAAA',
				'ATqraQmLhZ8qHoDyFO1I1G1Qh57CFMMwcZw7uPdEDFVyqUA61AAAAAA',
				'AaksVMGlb1cwB00fw1j-QALPzI-dFMMweiK9L6FEDFWEn0AoLgAAAAA',
				'AelGfWVWzfBiKUOHYbvcmXPIZiL7FMMwgYUPGA5EDFWUGUA4rwAAAAA',
				'AU2dWLD3V2U5qAvCr3a2JPTPKHCwFMMwi_garx5EDFWp5KA0lwAAAAA',
				'AdCZjVrf81WfBV312gRlDtsmO3b6FMMwk_0Emt5EDFW6zuApVQAAAAA',
				'AbxLUGnpaB9ctrYw1eOQz44WT0t_FMMwm0XW1wtEDFXJ2IBH-QAAAAA',
				'AWgNMKUQl5s6I2FxbhPhrVmkpx1mFMMwpFF0CVZEDFXc-iA7TQAAAAA',
				'AZB-ORxXpd8CiuGlUnP3_nfNHAq2FMMwrSZNz41EDFXvmcAoXgAAAAA',
				'AR9RJuSGRT1IBWOhUcKSHrwKShVAFMMws9scjwFEDFX9f8AtgwAAAAA',
				'AVhDP76IYvJUkyxpZXiAAbP8VGPEFMMwveRzrC5EDFYSdEAv5wAAAAA',
				'AYbUQ8UfHmxALLGWoM038ySrf5ztFMMwxQKjOfBEDFYhe6At3AAAAAA',
				'AfivjwA4ylwzMv0utM_5BR4SXfsCFMMwzdGT-QVEDFYz2yA27QAAAAA',
				'Ab3z582fFq-UJGi7J8cq3sCy-LC4FMIG2wMcBa1ECeVcNcAo5QAAAAA',
				'Ae4SFazCrOXR-Ty1HryemIQVoIuhFMIG7hnbsnVECeWEAMBEkgAAAAA',
				'AbQZu3nqOMPLl6Mk2CfDHc_T9wgwFMIJcAywAFtECerGFSA2bwAAAAA',
				'ASfGLgfv3UG5PwpYvh18f4vkNWddFMIJhcbZzaZECerzmYA-rgAAAAA',
				'AewqKq5OrQRrbnvkCkP_zEeKmS2BFMIJsLjjpkNECetNmyA20gAAAAA',
				'ARtz-qfApXDF5qfCCCE63L4JiUNtFMIJwZSFVHJECetxSqBC-wAAAAA',
				'AQ8T3cv1UzNA-XfPMCiFk5ABKbceFMIJzy0hhp9ECeuN_aAo9AAAAAA',
				'ATZXPDHvpiEoENesAVAJRqSddgDLFMIJ22xl27FECeunckAr2gAAAAA',
				'AUq7hJ8HDIkmGL1-KXsB8CPjSs9MFMIJ7jB5CrJECevLG4A7lQAAAAA',
				'AXIF54XnOQESyIDpVSSm5gHv-gpKFMIKAfUjYSJECev4dyA5HQAAAAA',
				'AVGC_FiwmYPcRxcV0Y-6PVrE1xONFMIKEn7nxC1ECewawkBGYgAAAAA',
				'AXUBO4at2phWIp9CAazDLOFlqAewFMIKN9-4-OhECexpIYBHMQAAAAA',
				'ARmiw5l8eOeLvSrl-pHgI-_a2Es0FMIF_SvzuXFECIPk9oA3RAAAAAA',
				'AaWqeeQvj50-OsqMKYhOTeIsgx48FMIGDSHpNwZEBzHKMYBEGQAAAAA',
				'Abds7VdBN0YG3NLBp4Un7BeFPsGWFMIGItMv2zRECePZ3GBCIgAAAAA',
				'AWrpgsLX5DfvXnzX6lehjkygu_3eFMIGMgwyoSdECIYkVgAtZAAAAAA',
				'AZqcp2oo2aLzkPRVemmsmy1cHihtFMIGRQ-f0VRECeQhR8A32AAAAAA',
				'AecAeRpggyDOKMjD5yi2DRiFehtMFMIGVGovPiNECeRBpwA1bwAAAAA',
				'AYidnj6716_1HcgttS0inYrTK8k8FMIGZmtFF6NECeRnTeBGzgAAAAA',
				'AZHSp0gpAUVXZryrhWFCCPxrS5CEFMIGjZA3p6lECeS5tcAx1wAAAAA',
				'AUxhDuK1u2-O-5FGC5z7LHd5cdX1FMIGtKJXeK1ECeULsSAxUAAAAAA',
				'AU2BMJxwTSq5c-aQ1AahI2wsGOuGFMIGx-2ZWZNECeU0BmA7LAAAAAA',
				'Ad5ijnA3hBRb7daeiHP22mDtb4HHFMN4_Yita_lEB_x18aAu5wAAAAA',
				'AQYCTmkcnT_hLexiwV7pYMJaXcczFMN5QEGYxBhEDO4inCA-WQAAAAA',
				'AaOzR1MG8tWr81SgVLXofqyEvb58FMN5q9HR-29EDO8EL4BF_QAAAAA',
				'AWAvX9EbhkAqcVaoTuGLrDaC1VYqFMN5-Ko22IVEDO-lb8BDKgAAAAA',
				'AVb3430LMe0Rfs4PaBtPReKPtJ-OFMN6iNy2vUtEDPAO36A_5gAAAAA',
				'AYsd4nyxPSdD8XSgQKfNuZFLRVKWFMN6s8vmXBJEDPEt70Ax0QAAAAA',
				'AVplmT5y2eFb9hLWqoEdCF-NtE1mFMN66I5FCllEDPGcd6A0qQAAAAA',
				'AbJ64ZlcPIHc0PzIiB-LjlNdSSilFMN7BAXBKixEDPHWCwBFNQAAAAA',
				'Af-6RjNfet5d3Vx9j24Hc9DJ4ba4FMN7G_cWLQVEDPIIbeBA4QAAAAA',
				'AWBsBHGuKSedkNtvM9jHOlrpUA1PFMN7PHvnEy5EDPJMpWBAhQAAAAA',
				'AXF6GUDPEjzN20jzxDQBBWP3INpGFMN7UxaqMWtEDPJ79yA6yAAAAAA',
				'AcqGgj_KPDcvffNEnt8LmoQLQpwTFMN7bv0pSzVEDPK2fUBCKQAAAAA',
				'AYLAjX9w_g6ifdCgbkPIoE2M34I3FMN7gpPe1LVEDPLfqUA4AgAAAAA',
				'ATEkKCj6IMbA8TBv2k4uViNLZiI7FMN7l9l2Z7VEDPML-2BHfQAAAAA',
				'ARZ-5IBj2dgSc3jdVtI3E8admpTkFMN7qas3ppdEDPMxiKAykQAAAAA',
				'AeHqUmGn-QdS_HUPvFgwzBcXEkAeFMN7uoRX6wtEDPNUhuA_YwAAAAA',
				'AYEKm0mMtIvnV30QnnjIeFCXrw5iFMN7zv1iZjZEDPN_o6A-iwAAAAA',
				'ATcmTR26iIsnDeT9srHrGuf25F8oFMONVvn8RbNEDRhDlCA2hQAAAAA',
				'AQkrfiAklRilskyDwTVTK-3TXcfFFMONYyY9vCVEDRhdYyBAuQAAAAA',
				'AZBd_S6vs5imGHIuP-wL6aOFni7jFMONa5mIb55EDRhuzuBGrQAAAAA']
	list = generate_soup_list(url)
	pins = []
	for a in list:
		if re.match(r'^/pin/', a['href']):
			id = a['href'].lstrip('/pin/').rstrip('/')

			while True:
				url = 'https://api.pinterest.com/v1/pins/' + id +\
					'/?access_token=' + token[token_index] + '&fields=id%2Ccreated_at'
				response = requests.get(url).text
				if 'message' not in response:
					break
				else:
					token_index += 1

			try:
				tstpStr = json.loads(response)['data']['created_at']
			except:
				continue
			tstp = datetime.strptime(tstpStr, '%Y-%m-%dT%H:%M:%S')
			if tstp < datetime(year=2017, month=3, day=1) or tstp >= datetime(year=2017, month=6, day=1):
				continue

			img_url = a.img['src']

			jsonStr = '{"pinID": "' + id + '", "img": "' + img_url + '", "label": "'\
						+ label + '", "timestamp": "' + str(tstp) + '"}'
			pins.append(jsonStr)
	return pins

def board_scrp(id):
	url = 'http://www.pinterest.com/pin/' + id + '/repins'
	list = generate_soup_list(url)
	users = '["'
	for a in list:
		if re.match(r'^/', a['href']) and len(a['href'])>4:
			userID = a['href'].lstrip('/').rstrip('/').split('/')[0]
			users = users + userID + '", "'
	users = users.rstrip(', "') + '"]'
	return users

if __name__ == '__main__':
	pinLabel = ['diy', 'makeover', 'ideas', 'grey', 'living%20room', 'design',\
		'repurposed', 'pallet', 'modern', 'bedroom', 'unique', 'rustic', 'patio',\
		'outdoor', 'vintage', 'industrial', 'wood', 'refinishing', 'painted',\
		'cheap', 'distressed', 'arrangement', 'antique', 'redo'\
		'restoration', 'upcycled', 'black', 'white', 'office', 'ashley',\
		'farmhouse', 'old', 'apartment', 'cool', 'hasks', 'art%20deco',\
		'recycled', 'ikea', 'decoupage', 'laminate', 'victorian', 'mirrored',\
		'baby', 'cardboard', 'urban', 'scandinavian', 'retro', 'modular',\
		'french', 'sofa', 'garden', 'table', 'chair', 'classic', 'store', 'logo',\
		'showroom', 'luxury', 'contemporary', 'metal', 'drawing', 'blue',
		'green', 'leather', 'brown', 'display']
	for label in pinLabel:
		l = re.sub('%20','',label)
		url = 'https://www.pinterest.com/search/pins/?q=furniture%20' + label
		pins= pin_scrp(url, l)
		p = list(set(pins))
		save_as_txt(p, 'source_ids.txt')

	infile = open('source_ids_GZ.txt')
	pins = infile.readlines()
	infile.close()

	repin_users = []
	n = 0
	for line in pins:
		n = n + 1
		print(n)
		jObj = json.loads(line)
		pinID = jObj['pinID']
		pair = '{"pinID": "' + pinID + '", "users": ' + board_scrp(pinID) + '}'
		repin_users.append(pair)
	save_as_txt(repin_users, 'repin_users_GZ.txt')

	sourceDF = pd.read_json('/Users/jacob/Desktop/Python/Pinterest/source_ids.txt', lines=True, encoding='utf-8')
	sourceDF['timestamp'] = pd.to_datetime(sourceDF['timestamp'])
	grouped = sourceDF.groupby(['pinID'])['label'].apply(list)
	del sourceDF['label']
	sourceDF = sourceDF.drop_duplicates()
	sourceDF = sourceDF.join(grouped, on='pinID')
	sourceDF.to_csv('/Users/jacob/Downloads/source_ids.txt', sep='\t', index=False)            
	            
	repins = pd.read_json('/Users/jacob/Desktop/Python/Pinterest/repin_users.txt',\
	                      dtype={"pinID":str, "users":list}, lines=True, encoding='utf-8')
	grouped = pd.DataFrame(repins.groupby(['pinID'])['users'].apply(list))
	grouped['users'] = grouped['users'].apply(choose_longest_list)
	grouped['pinID'] = grouped.index
	grouped = grouped[['pinID', 'users']]
	grouped.to_csv('/Users/jacob/Downloads/repin_users_grp.txt', sep='\t', index=False)