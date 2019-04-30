#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from nltk.tokenize import WordPunctTokenizer
from nltk.text import TextCollection
from nltk import ngrams, FreqDist
import math


# 构造tf-idf corpus (word为单位)
def get_corpus_word(all_abs):
    all_abs = [abs.split(' ') for abs in all_abs]  # 对所有摘要分词
    corpus = TextCollection(all_abs)
    return corpus


# 计算一篇摘要的所有词的tf-idf (以word为单位)
def tf_idf_abs(abstract, corpus):
    # abstract = set(abstract.split(' ')) # 对摘要分词
    abstract = set(abstract) # 对摘要分词

    tf_idf_list = [corpus.tf_idf(word, corpus) for word in abstract]

    return tf_idf_list


# 计算n篇摘要的所有词的tf-idf (以word为单位)
def tf_idf_abs_all(all_abstract, corpus):
    all_tf_idf = [tf_idf_abs(abs, corpus) for abs in all_abstract]
    return all_tf_idf

    # tokenzer = WordPunctTokenizer()
    # all_abstract = [tokenzer.tokenize(abs) for abs in all_abstract]  # 对所有摘要分词
    # for abs in all_abstract:
    #     tf_idf_list = []
    #     for word in abs:
    #         # tf = corpus.tf(word,corpus)
    #         # idf = corpus.idf(word)
    #         tf_idf = corpus.tf_idf(word,corpus)
    #         # print(word,': tf=',tf,' idf=',idf,' tf-idf=',tf_idf)
    #         tf_idf_list.append(tf_idf)
    #     # all_tf_idf.append([abs,tf_idf_list])
    #     all_tf_idf.append(tf_idf_list)
    # return all_tf_idf


# 统计一篇文档的关键词(整个词组)的tf—idf corpus以word为单位
def tf_idf_kw(keywords, corpus):
    tf_idf_dict = {}
    for kw in keywords:
        tf_idf = corpus.tf_idf(kw,corpus)
        tf_idf_dict.update({kw : tf_idf})
    return tf_idf_dict


# n_gram
# 获取单文本的n_gram
# text：分词后的结果
def n_gram(text,n):
    # text = text.split(' ')
    n_grams = ngrams(text,n)
    return [n_gram for n_gram in n_grams]


# 获取n篇摘要的n_gram
def get_n_gram_list(abs_list, n):
    return [n_gram(abs,n) for abs in abs_list]


# 构造corpus n_gram
def get_corpus_ngram(n_gram_list):
    return TextCollection(n_gram_list)


# 计算一篇摘要的所有词的tf-idf (以n_gram为单位)
def tf_idf_abs_n_gram(abs_n_grams, corpus_ngram):
    return [corpus_ngram.tf_idf(n_gram, corpus_ngram) for n_gram in set(abs_n_grams)]



# 计算n篇摘要的所有词的tf-idf (以n_gram为单位)
def tf_idf_abs_all_n_gram(abs_n_gram_list, corpus_ngram):
    return [tf_idf_abs_n_gram(abs_n_grams,corpus_ngram) for abs_n_grams in abs_n_gram_list]


# 统计一篇文档的关键词(整个词组)的tf—idf corpus以n_gram为单位
# ('This', 'paper') ======kw处理成这种格式
def tf_idf_kw_n_gram(keywords, corpus_ngram):
    tf_idf_dict = {}
    for kw in keywords:
        kw = tuple([term for term in kw.split(' ')])
        tf_idf = corpus_ngram.tf_idf(kw,corpus_ngram)
        tf_idf_dict.update({kw : tf_idf})
    return tf_idf_dict


#  获取一篇文档的关键词在摘要中的tf-idf排名
def get_kw_rank(kw_tfidf_dict, tf_idf_abs):
    kw_rank_dict = {}
    # abstract中词的tf - idf去重
    tf_idf_abs = list(set(tf_idf_abs))
    # abstract中词的tf-idf值降序排序
    tf_idf_abs.sort(reverse=True)
    for keyword in kw_tfidf_dict:
        rank = 0
        kw_tfidf = kw_tfidf_dict.get(keyword)
        if kw_tfidf not in tf_idf_abs:
            for tfidf in tf_idf_abs:
                if tfidf > kw_tfidf:
                    continue
                else:
                    rank = tf_idf_abs.index(tfidf) + 1  #  取第一个比关键词小的index+1作为其rank
                    break
        else:
            rank = tf_idf_abs.index(kw_tfidf) + 1
        kw_rank_dict.update({keyword: rank})
    return kw_rank_dict


#  获取n篇文档的关键词在摘要中的tf-idf排名
def get_kw_rank_all(kw_tfidf_dict_list,tf_idf_abs_list):
    for i in range(len(kw_tfidf_dict_list)):
        try:
            get_kw_rank(kw_tfidf_dict_list[i], tf_idf_abs_list[i])
        except ValueError :
            print(kw_tfidf_dict_list[i])
            print(tf_idf_abs_list[i])

    return [get_kw_rank(kw_tfidf_dict_list[i], tf_idf_abs_list[i]) for i in range(len(tf_idf_abs_list))]


# 获取n篇abstract的tfidf set的长度
def get_abs_tfidf_set_num(tf_idf_abs_list):
    return [len(set(tfidf_abs)) for tfidf_abs in tf_idf_abs_list]



# 自定义tf-idf
# # 以n_gram为单位计算tf
# def tf(word, n_grams):
#     count = FreqDist(n_grams)
#     return count[word] / sum(count.values())
#
#
# # 以n_gram为单位计算df
# def n_containing(word, n_gram_list):
#     count_list = [FreqDist(n_grams) for n_grams in n_gram_list]
#     return sum(1 for count in count_list if word in count)
#
#
# # 以n_gram为单位计算idf
# def idf(word, n_gram_list):
#     count_list = [FreqDist(n_grams) for n_grams in n_gram_list]
#     return math.log(len(count_list) / (1 + n_containing(word, count_list)))
#
# # 以n_gram为单位计算tf-idf
# def tfidf(word, n_grams, n_gram_list):
#     return tf(word, n_grams) * idf(word, n_gram_list)
#
#
# # 计算一篇摘要的所有词的tf-idf (以n_gram为单位)
# def tf_idf_abs_n_gram(abs_n_grams, abs_n_gram_list):
#     return [tfidf(n_gram, abs_n_grams, abs_n_gram_list) for n_gram in abs_n_grams]
#
#
# # 计算n篇摘要的所有词的tf-idf (以n_gram为单位)
# def tf_idf_abs_all_n_gram(abs_n_gram_list):
#     return [tf_idf_abs_n_gram(abs_n_grams,abs_n_gram_list) for abs_n_grams in abs_n_gram_list]
#
#
# # 统计一篇文档的关键词(整个词组)的tf—idf corpus以n_gram为单位
# def tf_idf_kw_n_gram(keywords, abs_n_grams,abs_n_gram_list):
#     tf_idf_dict = {}
#     for kw in keywords:
#         tf_idf = tfidf(kw,abs_n_grams,abs_n_gram_list)
#         tf_idf_dict.update({kw : tf_idf})
#     return tf_idf_dict