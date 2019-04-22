#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import nltk
from nltk.tokenize import WordPunctTokenizer
import pickle
import pandas as pd
import numpy as np

def load_json(path):
    with open(path, 'r', encoding='utf8') as fin:
        json_line = fin.readline()  # just one line
        json_obj = json.loads(json_line)
    return json_obj


def get_info(json_obj):
    abstract_list =[]
    keyword_list =[]
    title_list =[]
    for one in json_obj:
        keyword = one['keyword'].split(';')
        if len(keyword) > 10:   # 去除关键词个数大于10的数据
            continue
        abstract = one['abstract']
        title = one['title']
        abstract_list.append(abstract)
        keyword_list.append(keyword)
        title_list.append(title)
    return abstract_list, keyword_list, title_list


# stemming for a string, use str.split()  (not remove stopwords)
# return: string
def stemming_str(str, split_token):
    # str = re.sub(r'[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+]', '', str) #去掉标点
    # str = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9~!@#$%^&*()_+<>?:,./;’，。、‘：“《》？~！@#￥%……（）]', ' ', str) #去掉标点
    stemmer = nltk.stem.PorterStemmer()
    str_stem = ''
    for term in str.split(split_token):
        term_stem = stemmer.stem(term)
        str_stem = str_stem + ' ' + term_stem
    return str_stem.strip()


# stemming for a string, use str.split() (not remove stopwords)
# return: list
def stemming_list(str, split_token):
    stem_list = []
    stemmer = nltk.stem.PorterStemmer()
    words = str.split(split_token)
    for word in words:
        word_stem = stemmer.stem(word)
        stem_list.append(word_stem)
    return stem_list


# stemming for a string, use tokenizer() (not remove stopwords)
# return: list
def stemming_tokenizer(str):
    stem_list = []
    stemmer = nltk.stem.PorterStemmer()
    tokenzer = WordPunctTokenizer()
    words = tokenzer.tokenize(str)
    for word in words:
        word_stem = stemmer.stem(word)
        stem_list.append(word_stem)
    return stem_list


# pickle读取数据
def read(data_path):
    fr = open(data_path,'rb')
    data = pickle.load(fr)
    fr.close()
    return data

# pickle存储数据
def save(data, save_path):
    # fp = open(file=save_dir, mode='w', encoding='utf-8')
    fw = open(save_path, 'wb')
    pickle.dump(data, fw)
    fw.close()

# 读取存放在excel中的in or not数据（作图）
def read_excel_count(data_path):
    df = pd.read_excel(data_path, usecols=[1, 2], header=0)
    in_data = df.get('in')
    out_data = df.get('out')
    return [in_data, out_data]

if __name__ == '__main__':
    in_out_dir = './resulte_data/count.xlsx'
    in_out_data = read_excel_count(in_out_dir)
    in_data = np.array(in_out_data[0])
    out_data = np.array(in_out_data[1])
    total_data = in_data + out_data
    in_persents = []
    for i in range(len(in_data)):
        in_num = in_data[i]
        total = total_data[i]
        in_persent = in_num / total
        in_persents.append(in_persent)
    print(in_persents)
    print(in_out_data)
