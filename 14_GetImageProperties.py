import os
from glob import glob
import concurrent.futures

import cv2
import pandas as pd
import numpy as np
from scipy.stats import itemfreq

cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)

def feature_extraction(fname):
	try:
		img = cv2.imread(fname, cv2.IMREAD_UNCHANGED)
		
		# Image dimension
		height, width, _ = img.shape
		
		# Average color
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		avg_color = [img[:, :, i].mean() for i in range(img.shape[-1])]
		avg_r, avg_g, avg_b = list(map(int, avg_color))
		
		# Dominant color
		arr = np.float32(img)
		pixels = arr.reshape((-1, 3))
		
		n_colors = 5
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
		flags = cv2.KMEANS_RANDOM_CENTERS
		_, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
		
		palette = np.uint8(centroids)
		quantized = palette[labels.flatten()]
		quantized = quantized.reshape(img.shape)
		dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
		dmn_r, dmn_g, dmn_b = list(map(int, dominant_color))
		
		# Lightness
		img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
		avg_LAB = [img[:, :, i].mean() for i in range(img.shape[-1])]
		lightness, _, _ = list(map(int, avg_LAB))
		
		# HSV
		img = cv2.cvtColor(img, cv2.COLOR_LAB2RGB)
		img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
		avg_HSV = [img[:, :, i].mean() for i in range(img.shape[-1])]
		hue, saturation, intensity = list(map(int, avg_HSV))

		features = [height, width, avg_r, avg_g, avg_b, dmn_r, dmn_g, dmn_b, lightness, hue, saturation, intensity]	
		return features
	except:
		print("Failed to read image : %s" % (fname))
		return [None, None, None, None, None, None, None, None, None, None, None, None]

if __name__ == '__main__':
	with concurrent.futures.ProcessPoolExecutor() as executor, open('Board_Image_List.txt', 'w') as f:
		os.chdir(os.path.join(cwd, 'Board_Image'))
		ori_img_list = glob('*')
		f.write('img|height|width|avg_r|avg_g|avg_b|dmn_r|dmn_g|dmn_b|lightness|hue|saturation|intensity\n')

		for ori_img, features in zip(ori_img_list, executor.map(feature_extraction, ori_img_list)):
			f.write(ori_img + '|')
			for i in range(len(features)):
				if i == len(features) - 1:
					f.write(str(features[i]) + '\n')
				else:
					f.write(str(features[i]) + '|')
			print(ori_img)
