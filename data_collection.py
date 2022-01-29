import requests
import time
import random
import os

global_data_collect = {}


def read_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        for lines in f:
            l = lines.strip()
            global_data_collect[l] = True


def write_in_file(file_name):
    w = open(file_name, 'w', encoding='utf-8')
    for key in global_data_collect:
        w.write(key + '\n')


def collect_data(file_name):
    url = 'https://word.tips/five-letter-words/'
    for i in range(270, 500):
        url = 'https://v3.wordfinderapi.com/api/search?page_size=100&page_token={}&length=5&dictionary=wwf'.format(
            str(i))
        try:
            data = requests.get(url, timeout=60).json()
            print(data['word_pages'][0]['word_list'])
            print(len(data['word_pages'][0]['word_list']))
            for j in range(0, len(data['word_pages'][0]['word_list'])):
                word = data['word_pages'][0]['word_list'][j]['word']
                global_data_collect[word] = True
            write_in_file(file_name)
            print("{} done".format(i))
            time.sleep(random.randint(0, 50))
        except Exception as e:
            print(e)


read_data(file_name=os.path.join('data_5_length.txt'))
collect_data(file_name=os.path.join('data_5_length.txt'))
