#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from nltk import ngrams
from nltk.text import TextCollection
from static_count import preprocess, count, tf_idf, draw

json_file = '../data/test_json'
# json_file = '../data/all_title_abstract_keyword_clean.json'
json_obj = preprocess.load_json(json_file)
abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
# print(keyword_list[144])
# print(len(keyword_list[144]))
# print(len(keyword_list))


# # 统计关键词in or not in
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=False, isAnd=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(in_num_list)
# print(out_num_list)
# print(avg_in,avg_out)
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ff1.xlsx')
# print('count_ff1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=False,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ft1.xlsx')
# print('count_ft1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=False)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_tff1.xlsx')
# print('count_tf1 over!')
#
# count_results = count.count_in_all(abstract_list, keyword_list, isPart=True,isStem=True)
# in_num_list, out_num_list, avg_in, avg_out = count.cal_in_out_avg(count_results)
# count_dict = {'in':in_num_list,'out':out_num_list}
# print(count_results)
# print(avg_in,avg_out)
# data=DataFrame(count_dict)  #将字典转换成为数据框
# DataFrame(data).to_excel('count_ttf1.xlsx')
# print('count_tt1 over!')


# 统计每篇文章的count_in_out百分比
# in_out_persent =  count.in_out_persents('./4_25/count_ff1.xlsx')
# in_persent = in_out_persent[0]
# out_persent = in_out_persent[1]
# print(in_persent[:10])
# print(out_persent[:10])
# in_persent_persent = count.get_percentage(in_persent[0:10])
# print(in_persent_persent)


# # 统计关键词长度
# # kw_len= count.count_kw_len(keyword_list[4])
# # print(keyword_list[4])
# # print(np.average(kw_len))
# #
# # print('统计关键词长度......')
# n_kw_len = count.count_n_kw_len(keyword_list)
# # print('exp_num', exp_num)
# flatten =count.flatten_len(n_kw_len)
# # print(len(flatten))
# preprocess.save(flatten,'flatten_len_tokenize_new')
# # data=DataFrame(flatten)
# # DataFrame(data).to_excel('flatten_len.xlsx')

# 统计百分比
# print('统计百分比...')
# flatten_len_tokenize = preprocess.read('flatten_len_tokenize').tolist()
# persents_dict = count.get_percentage(flatten_len_tokenize)
# print(persents_dict)
# preprocess.save(persents_dict, 'persents_len_tokenize')
# data=DataFrame({'length':list(persents_dict.keys()), 'percent':list(persents_dict.values())})
# DataFrame(data).to_excel('persents_len_tokenize.xlsx')

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



# 计算tf-idf
# word为单位：
print("统计tf-idf")
keyword_list =  preprocess.stemming_all_keyword_list(keyword_list)
abstract_list = [preprocess.stemming_list(abs) for abs in abstract_list]

corpus1 = TextCollection(abstract_list)
preprocess.save(corpus1,'corpus1')
print('corpus1构建完成！')
kw_tfidf_dict_list = [tf_idf.tf_idf_kw(kw_list_stem,corpus1) for kw_list_stem in keyword_list]
tf_idf_abs_list = tf_idf.tf_idf_abs_all(abstract_list, corpus1)
# print('kw_tfidf_dict_list: ', kw_tfidf_dict_list)
# print('tf_idf_abs_list[1]: ',tf_idf_abs_list[1])

preprocess.save(tf_idf_abs_list, 'all_abs_tfidf1')
rank_list1 = tf_idf.get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list)
preprocess.save(rank_list1,'tfidf_rank1')
print('rank_list1: ',rank_list1)

n_gram_lists = tf_idf.get_n_gram_list(abstract_list,2)
corpus2 = TextCollection(n_gram_lists)
preprocess.save(corpus2,'corpus2')
print('corpus2构建完成！')
kw_tfidf_dict_list = [tf_idf.tf_idf_kw_n_gram(kw_list_stem,corpus2) for kw_list_stem in keyword_list]
tf_idf_abs_list = tf_idf.tf_idf_abs_all_n_gram(n_gram_lists, corpus2)
# print('kw_tfidf_dict_list[1]: ', kw_tfidf_dict_list[1])
# print('tf_idf_abs_list[1]: ',tf_idf_abs_list[1])
preprocess.save(tf_idf_abs_list, 'all_abs_tfidf2')
rank_list2 = tf_idf.get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list)
# # abstract中词的tf - idf去重
# tf_idf_abs = list(set(tf_idf_abs_list[1]))
# # abstract中词的tf-idf值降序排序
# tf_idf_abs.sort(reverse=True)
# print('tf_idf_abs_list[1]: ',tf_idf_abs)
preprocess.save(rank_list2,'tfidf_rank2')
print('rank_list2: ',rank_list2)

n_gram_lists = tf_idf.get_n_gram_list(abstract_list,3)
corpus3 = TextCollection(n_gram_lists)
preprocess.save(corpus3,'corpus3')
print('corpus3构建完成！')
kw_tfidf_dict_list = [tf_idf.tf_idf_kw_n_gram(kw_list_stem,corpus3) for kw_list_stem in keyword_list]
tf_idf_abs_list = tf_idf.tf_idf_abs_all_n_gram(n_gram_lists, corpus3)
preprocess.save(tf_idf_abs_list, 'all_abs_tfidf3')
rank_list3 = tf_idf.get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list)
preprocess.save(rank_list3,'tfidf_rank3')
print('rank_list3: ',rank_list3)

n_gram_lists = tf_idf.get_n_gram_list(abstract_list,4)
corpus4 = TextCollection(n_gram_lists)
preprocess.save(corpus4,'corpus4')
print('corpus4构建完成！')
kw_tfidf_dict_list = [tf_idf.tf_idf_kw_n_gram(kw_list_stem,corpus4) for kw_list_stem in keyword_list]
tf_idf_abs_list = tf_idf.tf_idf_abs_all_n_gram(n_gram_lists, corpus4)
preprocess.save(tf_idf_abs_list, 'all_abs_tfidf4')
rank_list4 = tf_idf.get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list)
preprocess.save(rank_list4,'tfidf_rank4')
print('rank_list4: ',rank_list4)

n_gram_lists = tf_idf.get_n_gram_list(abstract_list,5)
corpus5 = TextCollection(n_gram_lists)
preprocess.save(corpus5,'corpus5')
print('corpus5构建完成！')
kw_tfidf_dict_list = [tf_idf.tf_idf_kw_n_gram(kw_list_stem,corpus5) for kw_list_stem in keyword_list]
tf_idf_abs_list = tf_idf.tf_idf_abs_all_n_gram(n_gram_lists, corpus5)
preprocess.save(tf_idf_abs_list, 'all_abs_tfidf5')
rank_list5 = tf_idf.get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list)
preprocess.save(rank_list5,'tfidf_rank5')
print('rank_list5: ',rank_list5)




# tf_idf1 = tf_idf.tf_idf_abs(abstract_list[0], corpus1)
# print('abstract的tf-ifd计算完毕')
# keyword_list1 = [preprocess.stemming_str(keyword) for keyword in keyword_list[0]] #keyword_list已经stemming
# print(keyword_list1)
# print(abstract_list[0])
# kw_tf_idf1 = tf_idf.tf_idf_kw(keyword_list1,corpus1)
# tf_idf1.sort(reverse=True)
# # print(tf_idf1)
# print(kw_tf_idf1)
# for keyword in kw_tf_idf1:
#     print(keyword, tf_idf1.index(kw_tf_idf1.get(keyword)))



# corpus1 = tf_idf.get_corpus_word(abstract_list)
# all_tf_idf1 = tf_idf.tf_idf_abs_all(abstract_list,corpus1)

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