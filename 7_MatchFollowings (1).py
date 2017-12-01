import pandas as pd
import os
import json
import requests
from datetime import datetime

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
	df_repins = pd.read_csv(os.path.join(cmd, 'sample_repins.txt'), header=0, sep='\t')
	
	nList = []
	with open(os.path.join(cmd, 'sample_user_following.txt')) as f:
		lines = f.readlines()
		for line in lines:
			user, followings = line.split('\t')
			if followings == '\n':
				continue
			else:
				followings = followings.rstrip('\n')
				fList = followings.split(',')
				for f in fList:
					nList.append([user,f])
	df_network = pd.DataFrame(nList, columns=['user', 'following'])
	df_match = pd.merge(df_repins, df_network, on=['user'], how='left')
	
	df_user_pins = pd.read_csv(os.path.join(cmd, 'user_pins.txt'), header=None,
						    names=['fNewID','following','img','fDiscprition'], sep='\t')
	df_user_pins['img'] = df_user_pins['img'].map(trunk_img_url)
	df_new = pd.merge(df_match, df_user_pins, on=['following','img'], how='inner')
	df_new['fTimeStamp'] = df_new['fNewID'].map(find_timestamp)
	df_new['newTimestamp'] = pd.to_datetime(df_new['newTimestamp'], format='%Y-%m-%d %H:%M:%S')
	df_new['fTimeStamp'] = pd.to_datetime(df_new['fTimeStamp'], format='%Y-%m-%d %H:%M:%S')
	boolean = df_new['newTimestamp'] > df_new['fTimeStamp']
	df_new = df_new.loc[boolean, :]