import pandas as pd

count = []
trunksize = 1932
with open('board_pins_record.txt', 'r', encoding='utf8') as rf:
	for line in rf:
		line = line.replace('\n', '')
		line = line.split('\t')
		n = int(line[0]) * trunksize + int(line[1]) - 1
		count.append(n)
	print(len(count))
	rf.close()

df = pd.read_csv(('sample_repins_board_1.txt'), dtype=object, sep='\t', header=0)
df1 = df.drop(df.index[count])

print(df1.shape[0])
df1.to_csv('sample_repins_board_2.txt', sep='\t', header=True, index=False, encoding='utf-8')
# with open('sample_repins_board.txt', 'r', encoding='utf8') as rf:
# 	with open('sample_repins_board_1.txt', 'w', encoding='utf8') as wf:
# 		for line in rf: