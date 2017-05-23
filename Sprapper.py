#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:09:35 2017

@author: jacob
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time 
import requests
import re

def save_as_txt(jsonList, path):
    with open(path, 'w') as outfile:
        for line in jsonList:
            outfile.write(line + '\n')

def generate_soup_list(url):
    driver = webdriver.Chrome('/Users/jacob/chromedriver')
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    list = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
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

def pin_scrp(url):
    list = generate_soup_list(url)
    ids = []
    for a in list:
        if re.match(r'^/pin/', a['href']):
            id = a['href'].lstrip('/pin/').rstrip('/')
            # url = 'https://api.pinterest.com/v1/pins/' + id +\
            #     '/?access_token=AWVr2_IM7jZE-rAO4QWCliJwkesVFMDGrdLs27lEBzHKMYBEGQAAAAA&fields=id%2Ccreated_at%2Cimage'
            # response = requests.get(url)
            ids.append(id)
            # text.append(response.text)
    return ids#, text

def board_scrp(url):
    list = generate_soup_list(url)
    boards = []
    for a in list:
        if re.match(r'^/', a['href']) and len(a['href'])>4:
            boards.append(a['href'])
    return boards

if __name__ == '__main__':
    pinLabel = ['diy']
#, 'makeover', 'ideas', 'grey', 'living%20room', 'design',\
        # 'repurposed', 'pallet', 'modern', 'bedroom', 'unique', 'rustic', 'patio',\
        # 'outdoor', 'vintage', 'industrial', 'wood', 'refinishing'
    for label in pinLabel:
        # url = 'https://www.pinterest.com/search/pins/?q=furniture%20' + label
        # ids= pin_scrp(url)
        # save_as_txt(ids, '/Users/jacob/Desktop/Python/Pinterest/pinID/' + re.sub('%20','',label) + '_ids.txt')
        infile = open('/Users/jacob/Desktop/Python/Pinterest/pinID/' + re.sub('%20','',label) + '_ids.txt')
        ids = infile.readlines()
        infile.close()
        repins = {}
        for id in ids:
            boards = board_scrp('http://www.pinterest.com/pin/' + id + '/repins')
            repins.update({id: []})
            for board in boards:
                repins.setdefault(id,[]).append(board)
        with open('/Users/jacob/Desktop/Python/Pinterest/repins/' + re.sub('%20','',label) + '_repins.txt') as f:
            f.write(str(repins))