#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import nltk
from nltk.tokenize import WordPunctTokenizer
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
        keyword = one['keyword'].split(';')
        if len(keyword) > 10:   # 去除关键词个数大于10的数据
            continue
        abstract = one['abstract']
        title = one['title']
        abstract_list.append(abstract)
        keyword_list.append(keyword)
        title_list.append(title)
    return abstract_list, keyword_list, title_list


# stemming for a string (not remove stopwords)
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

# stemming for a string (not remove stopwords)
# return: list
def stemming_list(str, split_token):
    stem_list = []
    stemmer = nltk.stem.PorterStemmer()
    tokenzer = WordPunctTokenizer()
    words = tokenzer.tokenize(str)
    for word in words:
        word_stem = stemmer.stem(word)
        stem_list.append(word_stem)
    return stem_list

