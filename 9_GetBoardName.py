import os
import time
from datetime import datetime
import json
import requests
import pandas as pd
import numpy as np

cwd = os.path.dirname(os.path.realpath(__file__))
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

def get_board(pinID):
	global token_index
	while True:
		url = 'https://api.pinterest.com/v1/pins/' + str(pinID) + '/?access_token=' +\
			  token[token_index] + '&fields=board'
		response = requests.get(url).text
		if 'You have exceeded your rate limit' not in response:
			break
		else:
			print(response)
			token_index += 1
			print(token_index)
	try:
		board = json.loads(response)['data']['board']
		id = board['id']
		name = board['name']
		burl = board['url']

		while True:
			url = 'https://api.pinterest.com/v1/boards/' + board['id'] +\
				  '?access_token=' + token[token_index] + '&fields=description%2Ccreated_at'
			response = requests.get(url).text
			if 'You have exceeded your rate limit' not in response:
				break
			else:
				print(response)
				token_index += 1
				print(token_index)
		board_info = json.loads(response)['data']
		ts = datetime.strptime(board_info['created_at'], '%Y-%m-%dT%H:%M:%S')
		dscrp = board_info['description']
		time.sleep(2)
		return pd.Series({'board_id':id, 'board_name':name, 'board_url':burl, 'board_dscrp':dscrp, 'board_timesatamp':ts})
	except:
		time.sleep(2)
		return pd.Series({'board_id':np.nan, 'board_name':np.nan, 'board_url':np.nan, 'board_dscrp':np.nan, 'board_timesatamp':np.nan})

if __name__ == '__main__':
	fh = open(os.path.join(cwd, 'repin_users.txt'))
	lines = fh.readlines()
	fh.close()

	pins = []
	for line in lines:
		j = json.loads(line)
		pins.append(str(j['pinID']))

	df = pd.read_csv(os.path.join(cwd, 'sample_repins.txt'), header=0, sep='\t')
	df_board = df['pinID'].apply(get_board)
	df = pd.concat([df, df_board], axis=1)

	df.to_csv(os.path.join(cwd, 'sample_repins_board.txt'), header=True, index=False, sep='\t')
