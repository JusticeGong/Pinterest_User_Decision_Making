import os
import pandas as pd
from multiprocessing import Pool, cpu_count

cwd = os.path.dirname(os.path.realpath(__file__))

def filter(thread):
	if thread == cpu_count() - 1:
		df_temp = df_original.iloc[thread * trunk:, :]
	else:
		df_temp = df_original.iloc[thread * trunk : (thread+1) * trunk, :]

	for index, value in df_temp.iterrows():
		temp = df_repin.loc[df_repin['board_id']==value['board_id'], :]
		temp = temp.loc[temp['timestamp']<value['newTimestamp'], :]
		temp.to_csv('/Users/jacob/Downloads/12_board_pins_filtered_'+str(thread)+'.txt', sep='\t', header=False, index=False, mode='a')

if __name__ == '__main__':
	df_original = pd.read_csv(os.path.join(cwd, 'Data/8_sample_repins_board.txt'), sep='\t', header=0,
							  encoding='utf-8', usecols=['board_id', 'newTimestamp'], dtype={'board_id':str, 'newTimestamp':str})
	df_original['newTimestamp'] = pd.to_datetime(df_original['newTimestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
	df_repin = pd.read_csv(os.path.join(cwd, 'Data/11_board_pins_timestamp.txt'), sep='\t', encoding='utf-8',
						   names=['board_id', 'repin_id', 'img_url', 'dscp', 'timestamp'], dtype={'board_id':str, 'timestamp':str})
	df_repin['timestamp'] = pd.to_datetime(df_repin['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

	trunk = int(df_original.shape[0] / cpu_count())

	p = Pool(cpu_count())
	p.map(filter, range(cpu_count()))