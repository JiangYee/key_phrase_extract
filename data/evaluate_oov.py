#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from data import data_IO
from data import evaluate
import random

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
num = 0
id_list = []
merged_2w = []
kp_2w = []
abstrats_2w = []
id = random.randint(0, 99999)
id_list.append(id)
while num < 20000:
    id = random.randint(0, 99999)
    if not id_list.__contains__(id):
        id_list.append(id)
        merged_2w.append(merged_10w[id])
        kp_2w.append(all_doc_keywords[id])
        abstrats_2w.append(abstrats[id])
        num += 1

# merged_2w = merged_10w[0:20000]
# kp_2w = all_doc_keywords[0:20000]
# abstrats_2w = abstrats[0:20000]
print('merged_2w:', len(merged_2w))
print('kp_2w:', len(kp_2w))
print('abstrats_2w:',len(abstrats_2w))

# oov_10w = []
oov_2w = evaluate.get_oov_list(kp_2w,abstrats_2w,stop_words)
print('oov_2w:', len(oov_2w))
# for i in range(len(kp_10w)):
#     oov_list = evaluate.get_oov_list(kp_10w[i],abstrats[i],stop_words)
#     oov_10w.append(oov_list)
recall_avg, recall = evaluate.evaluate_oov_recall(merged_2w,oov_2w,stop_words)

evaluate.save_results(recall, recall_dir)
print('oov的recall：',recall_avg)
