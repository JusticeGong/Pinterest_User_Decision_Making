import os
import sys
import math
import re
from glob import glob
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import argparse
import base64

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

cwd = os.path.dirname(os.path.realpath(__file__))
img_dir = os.path.join(cwd, 'Board_Image')

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

lmtzr = WordNetLemmatizer()

def get_top_objects(fname):
	with open(fname, 'rb') as img:
		image_content = base64.b64encode(img.read())
		# label_batch_request.append()
		label_request = {
			'image': {
				'content': image_content.decode('UTF-8')
			},
			'features': [{
				'type': 'LABEL_DETECTION',
				'maxResults': 10
			}]
		}

	label_output = []
	try:
		label_request = service.images().annotate(body={'requests': label_request})
		label_responses = label_request.execute(num_retries=10)
		responses = label_responses['responses']
		
		if 'labelAnnotations' in responses[0]:
			labels = responses[0]['labelAnnotations']
			for j in range(len(labels)):
				word = lmtzr.lemmatize(labels[j]['description'])
				label_output.append(word.lower())
		
			if len(label_output) > 0:
				fh.write(fname + ':' + ','.join(label_output) + '\n')
	except:
		with open(os.path.join(cwd, 'exceptions.txt'), 'a') as f:
			f.write(fname + '\n')

	return label_output

if __name__ == '__main__':
	with ProcessPoolExecutor() as executor, open('Board_Image_Objects.txt', 'a') as fh:
		os.chdir(img_dir)
		fnames = glob('*')[:24930]
		# print(fnames[0])
		# get_top_objects(fnames)
		for fname, label_output in zip(fnames, executor.map(get_top_objects, fnames)):
			fh.write(fname + ':' + ','.join(label_output) + '\n')
			print(fname)