#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import nltk
from nltk.tokenize import WordPunctTokenizer
import pickle
import pandas as pd
import numpy as np
import re


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
        keyword = one['keyword'].lower().split(';')
        if len(keyword) > 10:   # 去除关键词个数大于10的数据
            continue
        abstract_temp = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9-°]', ' ', one['abstract']).lower()  # 去除标点 不包含 '-'
        abstract = (re.sub(r'\s{2,}', ' ', abstract_temp)).strip()  # 消除上述步骤产生的空格
        title = one['title'].lower()
        abstract_list.append(abstract)
        keyword_list.append(keyword)
        title_list.append(title)
    return abstract_list, keyword_list, title_list


def get_keywords(json_obj):
    keyword_list =[]
    keyword_len_list = []
    for one in json_obj:
        keyword = one['keyword'].lower().split(';')
        keyword_len_list.append(len(keyword))
        keyword_list.append(keyword)
    return keyword_list, keyword_len_list





# stemming for a string, use str.split(' ') 使用空格分词  (not remove stopwords)
# return: string
def stemming_str(str):
    # str = re.sub(r'[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+]', '', str) #去掉标点
    # str = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9~!@#$%^&*()_+<>?:,./;’，。、‘：“《》？~！@#￥%……（）]', ' ', str) #去掉标点
    # str = re.sub(r'[,.:;?()[]&!*@#$%]', '', str)  # 去除标点 不包含 '-'
    stemmer = nltk.stem.PorterStemmer()
    str_stem = ''
    for term in str.split(' '):
        if '-' in term:         # 将类似 'soft-in-soft-out' 词组处理为一个keyword
            term_stem = ''
            for sub_term in term.split('-'):
                term_stem = term_stem + '-' + stemmer.stem(sub_term)
            term_stem = term_stem.strip('-')
        else:
            term_stem = stemmer.stem(term)
        str_stem = str_stem + ' ' + term_stem
    return str_stem.strip()


# stemming for a string, use str.split(' ')使用空格分词 (not remove stopwords)
# return: list
def stemming_list(str):
    stem_list = []
    stemmer = nltk.stem.PorterStemmer()
    # words = str.split(' ')
    # for word in words:
    #     word_stem = stemmer.stem(word)
    #     stem_list.append(word_stem)
    for term in str.split(' '):
        if '-' in term:         # 将类似 'soft-in-soft-out' 词组处理为一个keyword
            term_stem = ''
            for sub_term in term.split('-'):
                term_stem = term_stem + '-' + stemmer.stem(sub_term)
            term_stem = term_stem.strip('-')
        else:
            term_stem = stemmer.stem(term)
        stem_list.append(term_stem)

    return stem_list


# 对所有的keyword stemming
def stemming_all_keyword_list(keyword_lists):
    stemming_results = []
    for keyword_list in keyword_lists:
        stemming_results.append([stemming_str(keyword) for keyword in keyword_list])
    print(stemming_results)
    return stemming_results

# # stemming for a string, use tokenizer() (not remove stopwords)
# # return: list
# def stemming_tokenizer(str):
#     stem_list = []
#     stemmer = nltk.stem.PorterStemmer()
#     tokenzer = WordPunctTokenizer()
#     words = tokenzer.tokenize(str)
#     # english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
#     for word in words:
#         # if word in english_punctuations:  # 去除标点 不包含 '-'
#         #     continue
#         word_stem = stemmer.stem(word)
#         stem_list.append(word_stem)
#     return stem_list


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
