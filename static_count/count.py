#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.text import TextCollection
from nltk import ngrams
from nltk import FreqDist
from nltk.tokenize import  word_tokenize
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from static_count import preprocess


# abstract: tokenzer.tokenize(abstract)
# keyphrase: keyphrase.split(' ')
# 统计单篇文档的关键词(整个词组)在摘要中出现/未出现的个数 keyword(stemming)
def count_in_stem(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    abs_stem = preprocess.stemming_list(abstract)

    for keyword in keyword_list:
        kd_stem = preprocess.stemming_str(keyword)
        if kd_stem in abs_stem:
            in_num += 1
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(整个词组)在摘要中出现/未出现的个数 (keyword 原始数据)
def count_in(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    # tokenzer = WordPunctTokenizer()
    # abs_words = tokenzer.tokenize(abstract)
    abs_words = abstract.split(' ')

    for keyword in keyword_list:
        if keyword in abs_words:
            in_num += 1
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数 keyword(stemming) or
# soft-in 处理成一个word
def count_part_in_stem_or(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    abs_stem = preprocess.stemming_list(abstract)
    print(abs_stem)
    print(keyword_list)
    for keyword in keyword_list:
        kw_stem_words = preprocess.stemming_list(keyword)
        print(kw_stem_words)
        for word_stem in kw_stem_words:
            if word_stem in abs_stem:
                in_num += 1
                break
    print('================')
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数（keyword 原始数据） or
# # soft-in 处理成一个word
def count_part_in_or(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    # tokenzer = WordPunctTokenizer()
    # abs_words = tokenzer.tokenize(abstract)
    abs_words = abstract.split(' ')

    for keyword in keyword_list:
        kw_words = keyword.split(' ')
        for word in kw_words:
            if word in abs_words:
                in_num += 1
                break
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数 keyword(stemming) or
# soft-in 处理成一个word     e.g. soft-in，information 为2个词
def count_part_in_stem_and(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    abs_stem = preprocess.stemming_list(abstract)

    for keyword in keyword_list:
        all_in = True
        kw_stem_words = preprocess.stemming_list(keyword)
        for word_stem in kw_stem_words:
            if not word_stem in abs_stem:
                all_in = False
                break
        if all_in:   #  该keyphrase的所有word都在abstract中出现时，认为该keyphrase在摘要中出现
            in_num += 1
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数（keyword 原始数据） or
# # soft-in 处理成一个word
def count_part_in_and(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    # tokenzer = WordPunctTokenizer()
    # abs_words = tokenzer.tokenize(abstract)
    abs_words = abstract.split(' ')

    for keyword in keyword_list:
        all_in = True
        kw_words = keyword.split(' ')
        for word in kw_words:
            if not word in abs_words:
                all_in = False
                break
        if all_in:
            in_num += 1     #   该keyphrase的所有word都在abstract中出现时，认为该keyphrase在摘要中出现
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# n篇文档count_in（）(整个词组)
def count_in_all(abstract_list, keyword_lists, isPart, isStem, isAnd):
    result = []
    for i in range(len(abstract_list)):
        abstract = abstract_list[i]
        keyword_list = keyword_lists[i]
        if isPart:  # 以word为单位
            if isAnd:   # and
                if isStem:
                    result.append(count_part_in_stem_and(abstract, keyword_list))
                else:
                    result.append(count_part_in_and(abstract,keyword_list))
            else:   # or
                if isStem:
                    result.append(count_part_in_stem_or(abstract,keyword_list))
                else:
                    result.append(count_part_in_or(abstract,keyword_list))
        else:   # 以整个phrase为单位
            if isStem:
                result.append(count_in_stem(abstract,keyword_list))
            else:
                result.append(count_in(abstract,keyword_list))
    return result

# 统计in/out num_list; 计算n篇文档关键词出现与否的平均值
def cal_in_out_avg(count_results):
    in_num_list = []
    out_num_list = []
    for result in count_results:
        in_num_list.append(result[0])
        out_num_list.append(result[1])
    in_num_list = np.array(in_num_list)
    out_num_list = np.array(out_num_list)
    avg_in = np.average(in_num_list)
    avg_out = np.average(out_num_list)
    return in_num_list, out_num_list, avg_in, avg_out


def in_out_persents(excel_dir):
    in_out_data = preprocess.read_excel_count(excel_dir)
    in_data = np.array(in_out_data[0])
    out_data = np.array(in_out_data[1])
    total_data = in_data + out_data
    in_persents = []
    out_persents = []
    for i in range(len(in_data)):
        in_num = in_data[i]
        out_num = out_data[i]
        total = total_data[i]
        in_persent = in_num / total
        out_persent = out_num / total
        in_persents.append(in_persent)
        out_persents.append(out_persent)

    return [in_persents,out_persents]


# ====================================================
# 统计一篇文档的关键词长度
# return length array
def count_kw_len(keyword_list):
    tokenzer = WordPunctTokenizer()
    len_kw = []
    for keyword in keyword_list:
        kw_words = tokenzer.tokenize(keyword)
        # kw_words = keyword.split(' ')
        # if len(kw_words)> 5:
        #     print(len(kw_words), kw_words)
        #     continue
        len_kw.append(len(kw_words))
    len_kw = np.array(len_kw)

    return len_kw


# 统计长度的同时，统计异常数据量
# def count_kw_len(keyword_list):
#     tokenzer = WordPunctTokenizer()
#     len_kw = []
#     exception_num = 0
#     for keyword in keyword_list:
#         kw_words = tokenzer.tokenize(keyword)
#         if "-" in kw_words:
#             print(kw_words)
#             exception_num += 1
#         len_kw.append(len(kw_words))
#     len_kw = np.array(len_kw)
#
#     return len_kw, exception_num



# def count_kw_len(keyword_list):
#     tokenzer = WordPunctTokenizer()
#     len_kw = [len(tokenzer.tokenize(keyword)) for keyword in keyword_list]
#     # len_kw = [len(keyword.split()) for keyword in keyword_list]
#     exp_data = []
#     for i in range(len(len_kw)):
#         if len_kw[i] > 10:
#             print(len_kw[i], '=====', keyword_list[i])
#             exp_data.append(keyword_list[i])
#             # for kw in keyword_list[i].split():
#                 # print(kw,' ***')
#     if(len(exp_data)>0):
#         print(exp_data)
#     # data = DataFrame(exp_data)
#     # DataFrame(data).to_excel('len_morethan10_data.xlsx')
#     return len_kw


# 统计n篇文档的关键词长度
def count_n_kw_len(keyword_lists):
    n_kw_len = [count_kw_len(keyword_list) for keyword_list in keyword_lists]
    return n_kw_len
    # n_kw_len = []
    # exp_sum = 0
    # for keyword_list in keyword_lists:
    #     kw_len, exception_num = count_kw_len(keyword_list)
    #     exp_sum += exception_num
    #     n_kw_len.append(kw_len)
    # return n_kw_len, exp_sum


def flatten_len(n_kw_len):
    flatten =[]
    for kw_len in n_kw_len:
        flatten = np.concatenate([flatten,kw_len])
    return flatten


def count_n_kw_len_dict(keyword_lists):
    n_kw_len_dict = {}
    for i in range(len(keyword_lists)):
        n_kw_len_dict.update({i: count_kw_len(keyword_lists[i])})
    return n_kw_len_dict


# 统计list中各数据所占的比例
def get_percentage(count_list):
    count_set = set(count_list)
    total_num = len(count_list)
    persents = {}

    for num in count_set:
        percent = count_list.count(num) / total_num
        persents.update({num: percent})
    return persents





# ====================================================
# 统计一个字符串str中某个word出现的频次  
def count_word_num(str,word):
    return len(str.split(word)) - 1


# 统计一篇文档中关键词在abstract中出现和未出现的关键词个数 （关键词和abstract均进行stemming,去除stopwords）
def count_in_oov_stem(kp_list, abstract, stop_words):
    stemmer = nltk.stem.PorterStemmer()
    # kp stemming
    kp_stem_list = []
    for i in range(len(kp_list)):
        one_kp_split = kp_list[i].split(' ')  # kp_list[i]一篇文章的一条关键词
        one_stem_kp = stemmer.stem(one_kp_split[0])
        for k in range(1, len(one_kp_split)):
            if not stop_words.__contains__(one_kp_split[k]):
                one_stem_kp = one_stem_kp + ' ' + stemmer.stem(one_kp_split[k])
        kp_stem_list.append(one_stem_kp)
    # abs stemming
    abs_spilt = abstract.split(' ')
    abs_stem  = stemmer.stem(abs_spilt[0])
    for i in range(1, len(abs_spilt)):
        if not stop_words.__contains__(abs_spilt[i]):
            abs_stem = abs_stem + ' ' + stemmer.stem(abs_spilt[i])

    # 统计出现/未出现词的个数
    in_num = 0
    oov_num = 0
    for kp_stem in len(kp_stem_list):
        num = count_word_num(abs_stem,kp_stem)
        if num > 0:
            in_num += 1
        else:
            oov_num += 1
    return in_num, oov_num


# 统计一篇文档中关键词在abstract中出现和未出现的关键词个数(不做stem)
def count_in_oov(kp_list, abstract):
    in_num = 0
    oov_num = 0
    for kp in kp_list:
        num = abstract.count(kp)
        if num > 0:
            in_num += 1
        else:
            oov_num += 1
    return in_num, oov_num


if __name__ == '__main__':
    abs = 'This paper proposes using virtual reality to enhance the perception of actions by distant users on a ' \
          'shared application. Here, distance may refer either to space ( e.g. in a remote synchronous collaboration)' \
          ' or time ( e.g. during playback of recorded actions). Our approach consists in immersing the application' \
          ' in a virtual inhabited 3D space and mimicking user actions by animating avatars. We illustrate this' \
          ' approach with two applications, the one for remote collaboration on a shared application and the other' \
          ' to playback recorded sequences of user actions. We suggest this could be a low cost enhancement' \
          ' for telepresence.'
    keyword_list = ['telepresence','animation','avatars','application sharing','collaborative virtual environments']
    print(count_in_stem(abs,keyword_list))
    print(count_in(abs,keyword_list))
    print(count_part_in_stem(abs,keyword_list))
    print(count_part_in(abs,keyword_list))
    str = 'thi paper propos use virtual realiti to enhanc the percept of action by distant user on a share ' \
          'application. here, distanc may refer either to space ( e.g. in a remot synchron collaboration) or ' \
          'time ( e.g. dure playback of record actions). our approach consist in immers the applic in a virtual' \
          ' inhabit 3D space and mimick user action by anim avatars. We illustr thi approach with two applications,' \
          ' the one for remot collabor on a share applic and the other to playback record sequenc of user actions.' \
          ' We suggest thi could be a low cost enhanc for telepresence.'
    stem_list = ['telepres','anim','avatar','applic share','collabor virtual environ']
    # for stem in stem_list:
    #     print(stem,stem in abs)
    # print('==========')
    # for keyword in keyword_list:
    #     print(keyword, keyword in abs)

    kw_lists = []
    kw_lists.append(keyword_list)
    kw_lists.append(keyword_list)
    abs_list = [abs,abs]
    print(count_in_all(abs_list,kw_lists,isPart=False,isStem=True))
    print(count_in_all(abs_list,kw_lists,isPart=True,isStem=False))
