import pandas as pd
import os
import shutil

os.chdir(os.path.dirname(os.path.realpath(__file__)))

df_original = pd.read_csv('Data/8_sample_repins_board.txt', sep='\t', header=0, usecols=['img'])
print(df_original.shape[0])
df_original = df_original.drop_duplicates()
img_list = df_original['img']
print(len(img_list))

df_board = pd.read_csv('Data/12_board_pins_filtered.txt', sep='\t', header=0, usecols=['img_url'])
df_board['img'] = df_board['img_url'].map(lambda x:  x.split('/')[-1])
del df_board['img_url']
df_board = df_board.drop_duplicates()
print(df_board.shape[0])
img_list_2 = df_board['img']

img_list = set(img_list)
for dirname, dirnames, filenames in os.walk('/Volumes/KZ-backup/Images'):
    temp = list(img_list & set(filenames))
    for t in temp:
        shutil.copy2(os.path.join(dirname, t), '/Users/jacob/Desktop/Python/Pinterest/Original_Image')

img_list_2 = set(img_list_2)
for dirname, dirnames, filenames in os.walk('/Volumes/KZ-backup/Images'):
    temp = list(img_list_2 & set(filenames))
    for t in temp:
        shutil.copy2(os.path.join(dirname, t), '/Users/jacob/Desktop/Python/Pinterest/Board_Image')