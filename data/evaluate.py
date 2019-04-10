#! /user/bin/evn python
# -*- coding:utf8 -*-

import codecs
import numpy as np
import nltk
import time,datetime
import pickle

# 获取每篇文档的topK个融合的关键术语
def get_topK_kp(all_merged_kp, k):
    start_time = time.time()
    topK_merged_kp = []
    for i in range(len(all_merged_kp)):
        sorted_list = sorted(all_merged_kp[i].items(), key=lambda d: d[1], reverse=True)
        one_doc_kp_list = []
        for j in range(k):
            if j < len(sorted_list):
            # try:
                one_doc_kp_list.append(sorted_list[j][0])
            else:
                print('k='+ str(k) + '=====len(sorted_list)=' + str(len(sorted_list)))
                print('当前文章的rake：'+ str(sorted_list))
                print('one_doc_kp_list.append: ' + str(one_doc_kp_list))
                break
            # except (Exception) as e:
            #     print(e)
            #     print(str(j))
            #     print(str(sorted_list))
        topK_merged_kp.append(one_doc_kp_list)

    end_time = time.time()
    time_used = datetime.timedelta(seconds=int(round(end_time - start_time)))
    print('get_topK_kp()耗时： ', str(time_used))
    return topK_merged_kp


def evaluate(topK_merged_kp, original_kp):
    precision = []
    recall = []
    # k可能小于标准关键术语个数
    doc_num = len(topK_merged_kp)
    for i in range(doc_num):
        #  计算每一篇文档的p和r
        correct_num = 0
        for j in range(len(topK_merged_kp[i])):
            if original_kp[i].__contains__(topK_merged_kp[i][j]):
                correct_num += 1
        pi = correct_num / len(topK_merged_kp[i])
        ri = correct_num / len(original_kp[i])
        precision.append(pi)
        recall.append(ri)
    # 计算全部文档的平均p和r
    precision = np.array(precision)
    recall = np.array(recall)
    precision_avg = np.average(precision)
    recall_avg = np.average(recall)
    f = (2 * precision_avg * recall_avg) / (precision_avg + recall_avg)

    return precision_avg, recall_avg, f, precision, recall


# 去停用词和词干提取
def stemming(kp_list, stop_words):
    stemmer = nltk.stem.PorterStemmer()
    all_stem_result = []
    for i in range(len(kp_list)):
        one_stem_result = []
        for j in range(len(kp_list[i])):
            one_kp_split = kp_list[i][j].split(' ')
            one_stem_kp = stemmer.stem(one_kp_split[0])
            for k in range(1, len(one_kp_split)):
                if not stop_words.__contains__(one_kp_split[k]):
                    one_stem_kp = one_stem_kp + ' ' + stemmer.stem(one_kp_split[k])
            one_stem_result.append(one_stem_kp)
        all_stem_result.append(one_stem_result)
    return all_stem_result

#
# def stemming_merge_info(all_merge_info, stop_words):
#     start_time = time.time()
#
#     stemmer = nltk.stem.PorterStemmer()
#     all_merge_info_stem = []
#     for merge_info in all_merge_info:
#         merge_info_stem = {}
#         for keyprase in merge_info:
#             score = merge_info.get(keyprase)
#             one_kp_split = keyprase.split(' ')
#             one_stem_kp = stemmer.stem(one_kp_split[0])
#             for k in range(1,len(one_kp_split)) :
#                 if not stop_words.__contains__(one_kp_split[k]):
#                     one_stem_kp = one_stem_kp + ' ' + stemmer.stem(one_kp_split[k])
#             merge_info_stem.update({one_stem_kp: score})
#         all_merge_info_stem.append(merge_info_stem)
#
#     end_time = time.time()
#     time_used = datetime.timedelta(seconds=int(round(end_time - start_time)))
#     print('stemming_merge_info()耗时： ', str(time_used))
#     return all_merge_info_stem


def evaluate_stem(topK_merged_kp, original_kp, stop_words):
    start_time = time.time()
    topK_merged_kp = stemming(topK_merged_kp, stop_words)
    original_kp = stemming(original_kp, stop_words)
    end_time = time.time()
    time_used = datetime.timedelta(seconds=int(round(end_time - start_time)))
    print('stemming()耗时： ', str(time_used))

    precision = []
    recall = []
    # k可能小于标准关键术语个数
    doc_num = len(topK_merged_kp)
    for i in range(doc_num):
        # print('关键术语topK: ' + str(topK_merged_kp[i]))
        # print('原始关键术语：' + str(original_kp[i]))
        #  计算每一篇文档的p和r
        correct_num = 0
        for j in range(len(topK_merged_kp[i])):
            if original_kp[i].__contains__(topK_merged_kp[i][j]):
                correct_num += 1
        pi = correct_num / len(topK_merged_kp[i])
        ri = correct_num / len(original_kp[i])
        precision.append(pi)
        recall.append(ri)
    # 计算全部文档的平均p和r
    precision = np.array(precision)
    recall = np.array(recall)
    precision_avg = np.average(precision)
    recall_avg = np.average(recall)
    f = (2 * precision_avg * recall_avg) / (precision_avg + recall_avg)

    end_time = time.time()
    time_used = datetime.timedelta(seconds=int(round(end_time - start_time)))
    print('evaluate_stem()耗时： ', str(time_used))

    return precision_avg, recall_avg, f, precision, recall


# 获取n篇文档的out of vocabulary
def get_oov_list(kp_list, abstract_list, stop_words):
    stemmer = nltk.stem.PorterStemmer()
    kp_stem_lists = stemming(kp_list, stop_words) #n篇文档的所有kp
    oov_lists = []
    for abstract in abstract_list:
        abs_spilt = abstract.split(' ')
        abs_stem = stemmer.stem(abs_spilt[0])
        for i in range(1, len(abs_spilt)):
            if not stop_words.__contains__(abs_spilt[i]):
                abs_stem = abs_stem + ' ' + stemmer.stem(abs_spilt[i])
        # 统计未登录词个数
        for kp_stem_list in kp_stem_lists: #一篇文档的关键词list
            oov_list = []
            for i in range(len(kp_stem_list)):
                num = count_word_num(abs_stem, kp_stem_list[i])
                if num == 0:
                #  key:   未做stemming的关键词
                    oov_list.append(kp_list[i])
            oov_lists.append(oov_list)
    return oov_lists


# 统计一个字符串str中某个word出现的频次  
def count_word_num(str, word):
    num = 0
    try:
        num = len(str.split(word)) - 1
        print('str=====', str)
        print('word=====', word)
    except (ValueError) as e:
        print(e)
        print('str=====',str)
        print('word=====',word)
    return num

def save_results(result_array, save_path):
    # fp = open(file=save_dir, mode='w', encoding='utf-8')
    fp = codecs.open(filename=save_path, mode='w', encoding='utf-8')
    for i in range(len(result_array)):
        line = str(result_array[i])
        fp.write(str(i) + ":" + line + '\n')
    fp.close()


# 对融合的全部结果排序后写入文件
def save_all_merged_results(result_list, save_dir):
    fp = codecs.open(filename=save_dir, mode='w', encoding='utf-8')
    for i in range(len(result_list)):
        line = str(sorted(result_list[i].items(), key=lambda d: d[1], reverse=True))
        fp.write(line + '\n')
    fp.close()


def save_results_pickle(result_array, save_path):
    # fp = open(file=save_dir, mode='w', encoding='utf-8')
    fw = open(save_path, 'wb')
    pickle.dump(result_array, fw)
    fw.close()

