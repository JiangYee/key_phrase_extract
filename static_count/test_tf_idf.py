#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.text import TextCollection
from nltk import ngrams
from nltk import FreqDist
import numpy as np
import math
from static_count import preprocess,count,tf_idf

json_file = '../data/test_json'
json_obj = preprocess.load_json(json_file)
abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
# tokenizer = WordPunctTokenizer()
# n_grams = count.n_gram(abstract_list[0],2)
# corpus = count.get_corpus_ngram(n_grams)
# n_gram_list = [n_gram for n_gram in n_grams]
# for keyword in keyword_list:
#     tf_idf = corpus.tf_idf(keyword,n_gram_list)
#     print(keyword, tf_idf)


def count_f(n_grams):
    return FreqDist(n_grams)

def tf(word, count):
    return count[word] / sum(count.values())

def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)

def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))

def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

if __name__ == '__main__':
    # n_grams0 = count.n_gram(abstract_list[1], 2)
    # count0 = count_f(n_grams0)
    #
    # n_grams = count.n_gram(abstract_list[0], 2)
    # n_gram_list = [n_gram for n_gram in n_grams]
    # count = count_f(n_gram_list)
    # print(count.most_common(5))
    # print(count.keys())
    # print(count[('This', 'paper')])
    # print(count.values())
    # print(tf(('This', 'paper'), count))
    # print(n_containing(('This', 'paper'),[count0,count]))
    # print(idf(('This', 'paper'),[count0,count]))
    # print(tfidf(('This', 'paper'),count,[count0,count]))
    n_grams = tf_idf.n_gram(abstract_list[0],2)
    abs_n_gram_lsit = tf_idf.get_n_gram_list(abstract_list,2)
    tfidf1 = tf_idf.tf_idf_abs_n_gram(n_grams,abs_n_gram_lsit)
    print(tfidf1)

