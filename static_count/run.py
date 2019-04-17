#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from nltk import ngrams
from static_count import preprocess, count

json_file = '../data/test_json'
# json_file = '../data/all_title_abstract_keyword_clean.json'
json_obj = preprocess.load_json(json_file)
abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
# print(keyword_list[144])
# print(len(keyword_list[144]))
# print(len(keyword_list))
# 统计关键词in or not in
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ff.xlsx')
# print('count_ff over!')

# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ft.xlsx')
# print('count_ft over!')

# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_tf.xlsx')

# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# #
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_tt.xlsx')



# 计算tf-idf
# word为单位：
corpus0 = count.get_corpus_word(abstract_list)
all_tf_idf = count.tf_idf_abs_all(abstract_list,corpus0)
data_tf_idf = DataFrame(all_tf_idf)
# data_tf_idf = DataFrame(np.array(all_tf_idf)[:,1])
DataFrame(data_tf_idf).to_excel('tf-idf_test.xlsx')
# 关键词的tf-idf
# tf_idf_kw = count.tf_idf_kw(keyword_list[0], corpus0)
# print(tf_idf_kw)

# 以n_gram为单位：
# n_grams = count.n_gram(abstract_list[0],2)
# corpus = count.get_corpus_ngram(n_grams) #只是单篇的n_gram？？？
# all_tf_idf = count.tf_idf_abs_all(abstract_list,corpus)
# data_tf_idf = DataFrame(all_tf_idf)
# DataFrame(data_tf_idf).to_excel('tf-idf_ngram.xlsx')
# print(corpus.tf_idf('this paper',corpus))


# 统计关键词长度
# kw_len= count.count_kw_len(keyword_list[4])
# print(keyword_list[4])
# print(np.average(kw_len))
#
n_kw_len = count.count_n_kw_len(keyword_list)
data=DataFrame(n_kw_len)
DataFrame(data).to_excel('len.xlsx')

# print(n_kw_len)
# avgs = [np.average(kw_len) for kw_len in n_kw_len]
# print(avgs)
# print(np.average(avgs))

# len_data = DataFrame(n_kw_len)
# DataFrame(len_data).to_excel('len.xlsx')

# n_grams = count.n_gram(abstract_list[0],2)
# for gram in n_grams:
#     if 'application' in gram:
#         print(gram)