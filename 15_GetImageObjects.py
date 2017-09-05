import os
import sys
import math
import re
from glob import glob

import argparse
import base64

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

cwd = os.path.dirname(os.path.realpath(__file__))

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

lmtzr = WordNetLemmatizer()

def get_top_objects(photo_dir, fnames):
	label_batch_request = []
	for f in fnames:
		filename = os.path.join(photo_dir, f)
		with open(filename,'rb') as img:
			image_content = base64.b64encode(img.read())
			label_batch_request.append({
				'image': {
					'content': image_content.decode('UTF-8')
				},
				'features': [{
					'type': 'LABEL_DETECTION',
					'maxResults': 10
				}]
			})

	label_request = service.images().annotate(body={'requests': label_batch_request})
	label_responses = label_request.execute(num_retries=10)
	responses = label_responses['responses']
	
	fh = open(os.path.join(cwd, 'Original_Image_Objects.txt'), 'a')
	for i in range(1, len(responses)):
		fname = fnames[i - 1]

		label_output = []
		if 'labelAnnotations' in responses[i]:
			labels = responses[i]['labelAnnotations']
			for j in range(len(labels)):
				word = lmtzr.lemmatize(labels[j]['description'])
				label_output.append(word.encode('utf8').lower())

			if len(label_output) > 0:
				fh.write(fname + ':' + ','.join(label_output) + '\n')
	return 0

if __name__ == '__main__':
	img_dir = os.path.join(cwd, 'Original_Image')
	os.chdir(img_dir)
	fnames = glob('*')
	get_top_objects(img_dir, fnames)