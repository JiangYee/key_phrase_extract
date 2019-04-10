#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from data import data_IO
from data import evaluate

recall_dir = 'oov_recall.txt'
file_path_json = 'rake_extract_keyphrase.json'
merged_dir = '../evaluate_es_10w_doc2vec2/P0/top6/top6_phrases_pickle.txt'

stop_words = data_IO.get_stopword()
_, abstrats, all_doc_keywords,_ = data_IO.load_all_data_json4(file_path_json)  #全量
print('abstract_str_list.len: ' + str(len(all_doc_keywords)))
#  读取merged_results
fr = open(merged_dir,'rb')
merged_10w = pickle.load(fr,encoding='utf-8')
fr.close()

# 计算oov的召回率时，先用get_oov_list,再调用evaluate_stem（oov_list，original_kp， stop_words
kp_10w = all_doc_keywords[0:2]
abstrats_10w = abstrats[0:2]
oov_10w = []
# for i in range(len(kp_10w)):
#     oov_list = evaluate.get_oov_list(kp_10w[i],abstrats[i],stop_words)
#     oov_10w.append(oov_list)
oov_10w = evaluate.get_oov_list(kp_10w,abstrats_10w,stop_words)
precision_avg, recall_avg, f, precision, recall = evaluate.evaluate_stem(merged_10w,oov_10w,stop_words)

evaluate.save_results(recall, recall_dir)
print('oov的recall：',recall_avg)
