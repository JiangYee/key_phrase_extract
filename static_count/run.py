#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from nltk import ngrams
from static_count import preprocess, count,tf_idf

# json_file = '../data/test_json'
json_file = '../data/all_title_abstract_keyword_clean.json'
json_obj = preprocess.load_json(json_file)
abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
# print(keyword_list[144])
# print(len(keyword_list[144]))
# print(len(keyword_list))


# # 统计关键词in or not in
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ff1.xlsx')
# print('count_ff1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ft1.xlsx')
# print('count_ft1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_tf1.xlsx')
# print('count_tf1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_tt1.xlsx')
# print('count_tt1 over!')


# 计算tf-idf
# word为单位：
# corpus0 = tf_idf.get_corpus_word(abstract_list)
# all_tf_idf = tf_idf.tf_idf_abs_all(abstract_list,corpus0)

# data_tf_idf = DataFrame(all_tf_idf)
# data_tf_idf = DataFrame(np.array(all_tf_idf)[:,1])
# DataFrame(data_tf_idf).to_excel('tf-idf_test.xlsx')
# 关键词的tf-idf
# tf_idf_kw = count.tf_idf_kw(keyword_list[0], corpus0)
# print(tf_idf_kw)

# 以n_gram为单位：
# n_grams = tf_idf.n_gram(abstract_list[0],2)
# abs_n_gram_lsit = tf_idf.get_n_gram_list(abstract_list,2)
# tfidf1 = tf_idf.tf_idf_abs_n_gram(n_grams,abs_n_gram_lsit)
# data_tf_idf = DataFrame({'2-gram': n_grams, 'tf-idf':tfidf1})
# DataFrame(data_tf_idf).to_excel('tf-idf_2gram.xlsx')
# print(tfidf1)




# 统计关键词长度
# kw_len= count.count_kw_len(keyword_list[4])
# print(keyword_list[4])
# print(np.average(kw_len))
#
# print('统计关键词长度......')
# n_kw_len = count.count_n_kw_len(keyword_list)
# print('exp_num', exp_num)
# flatten =count.flatten_len(n_kw_len)
# print(len(flatten))
# preprocess.save(flatten,'flatten_len_tokenize')
# data=DataFrame(flatten)
# DataFrame(data).to_excel('flatten_len5.xlsx')

# 统计百分比
print('统计百分比...')
flatten_len_tokenize = preprocess.read('./count_data/flatten_len').tolist()
persents_dict = count.get_percentage(flatten_len_tokenize)
preprocess.save(persents_dict, 'persents_len')
data=DataFrame({'length':persents_dict.keys(), 'percent':persents_dict.values()})
DataFrame(data).to_excel('persents_len.xlsx')

# preprocess.save(n_kw_len,'len')
# data=DataFrame({'keyword': keyword_list, 'len':n_kw_len})
# data=DataFrame(n_kw_len)
# DataFrame(data).to_excel('len0.xlsx')

# print(n_kw_len)
# avgs = [np.average(kw_len) for kw_len in n_kw_len]
# print(avgs)
# print(np.average(avgs))

# len_data = DataFrame(n_kw_len)
# DataFrame(len_data).to_excel('len.xlsx')

# n_grams = count.n_gram(abstract_list[0],2)
# for gram in n_grams:
#     if 'application' in gram:  # keyword中的word存在于n_gram中
#         print(gram)