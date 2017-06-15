import pandas as pd
import numpy as np
import os
import json
import requests
from datetime import datetime
from multiprocessing import Pool

def find_exiting(l):
	intersect = list(set(l).intersection(sample_list))
	return intersect

def choose_longest_list(l):
    longest = []
    for i in l:
        if len(i) > len(longest):
            longest = i
    return i

# Trunk original image url into filename
def trunk_img_url(url):
	fname = url.split('/')[-1]
	return fname

def find_timestamp(id):
	token_index = 0
	token = ['ARmiw5l8eOeLvSrl-pHgI-_a2Es0FMIF_SvzuXFECIPk9oA3RAAAAAA',
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
	while True:
		url = 'https://api.pinterest.com/v1/pins/' + str(id) +\
			  '/?access_token=' + token[token_index] + '&fields=created_at'
		response = requests.get(url).text
		if ('message' not in response) | ('Pin not found' in response):
			break
		else:
			token_index += 1
	try:
		tstpStr = json.loads(response)['data']['created_at']
		tstp = datetime.strptime(tstpStr, '%Y-%m-%dT%H:%M:%S')
		# time.sleep(1)
		return tstp
	except:
		return None

if __name__ == '__main__':
	cmd = os.path.dirname(os.path.realpath(__file__))
	df_repins = pd.read_csv(os.path.join(cmd, 'repin_users.txt'), header=0, sep='\t')
	df_repins = pd.read_json('/Users/jacob/Desktop/Python/Pinterest/repin_users.txt',
						   dtype={"pinID":str, "users":list}, lines=True, encoding='utf-8')
	df_sample = pd.read_csv(os.path.join(cmd, 'user_list_20000_sample.csv'), header=None,
							names=['index','userID'], usecols=['userID'])
	sample_list = list(df_sample.userID)
	df_repins['users'] = df_repins['users'].map(find_exiting)
	grouped = pd.DataFrame(df_repins.groupby(['pinID'])['users'].apply(list))
	grouped['users'] = grouped['users'].apply(choose_longest_list)
	grouped['pinID'] = grouped.index
	df_repins = grouped[['pinID', 'users']]
	del grouped
	
	df = pd.DataFrame(columns=['pinID', 'user'])
	dict_repins = df_repins.to_dict(orient='index')
	i = 0
	for key, value in dict_repins.items():
		for u in value['users']:
			temp = pd.DataFrame({'pinID':value['pinID'], 'user':u}, index=[i])
			df = pd.concat([df, temp])
	df_ori_pins = pd.read_csv(os.path.join(cmd, 'source_ids.txt'), header=0, sep='\t')
	df = pd.merge(df.reset_index(), df_ori_pins.reset_index(), on=['pinID'])
	del df['index_x']
	del df['index_y']
	df['img'] = df['img'].map(trunk_img_url)
	
	df_user_pin = pd.read_csv(os.path.join(cmd, 'user_pins.txt'), header=None,
						    names=['newID','user','img','discription'], sep='\t')
	df_user_pin['img'] = df_user_pin['img'].map(trunk_img_url)
	df = pd.merge(df, df_user_pin, on=['user','img'], how='inner')
	
	df['newTimestamp'] = df['newID'].map(find_timestamp)
	df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
	df['delta'] = df['newTimestamp'] - df['timestamp']

	df.to_csv(os.path.join(cmd, 'sample_repins.txt'), index=False, header=True, sep='\t')