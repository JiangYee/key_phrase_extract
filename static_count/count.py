#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.text import TextCollection
from nltk import ngrams
from nltk import FreqDist
from nltk.tokenize import  word_tokenize
import numpy as np
from static_count import preprocess

# 统计单篇文档的关键词(整个词组)在摘要中出现/未出现的个数 keyword(stemming)
def count_in_stem(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    abs_stem = preprocess.stemming_list(abstract, ' ')
    # print(abs_stem)

    for keyword in keyword_list:
        kd_stem = preprocess.stemming_str(keyword, ' ')
        # print(kd_stem)
        if kd_stem in abs_stem:
            in_num += 1
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(整个词组)在摘要中出现/未出现的个数 (keyword 原始数据)
def count_in(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    tokenzer = WordPunctTokenizer()
    # abs_words = nltk.tokenize.word_tokenize(abstract)
    abs_words = tokenzer.tokenize(abstract)
    # print(abs_words)

    for keyword in keyword_list:
        # print(keyword)
        if keyword in abs_words:
            in_num += 1
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数 keyword(stemming)
def count_part_in_stem(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    abs_stem = preprocess.stemming_list(abstract, ' ')
    # print(abs_stem)

    for keyword in keyword_list:
        kd_stem_words = preprocess.stemming_list(keyword, ' ')
        # part_in = False
        for word_stem in kd_stem_words:
            if word_stem in abs_stem:
                in_num += 1
                break
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# 统计单篇文档的关键词(以word为单位)在摘要中出现/未出现的个数（keyword 原始数据）
def count_part_in(abstract, keyword_list):
    in_out_list = []
    in_num = 0
    tokenzer = WordPunctTokenizer()
    abs_words = tokenzer.tokenize(abstract)
    # print(abs_words)

    for keyword in keyword_list:
        kd_words = tokenzer.tokenize(keyword)
        for word in kd_words:
            if word in abs_words:
                in_num += 1
                break
    in_out_list.append(in_num)
    in_out_list.append(len(keyword_list) - in_num)
    return in_out_list


# n篇文档count_in（）(整个词组)
def count_in_all(abstract_list, keyword_lists, isPart, isStem):
    result = []
    for i in range(len(abstract_list)):
        abstract = abstract_list[i]
        keyword_list = keyword_lists[i]
        if isPart:  # 以word为单位
            if isStem:
                result.append(count_part_in_stem(abstract,keyword_list))
            else:
                result.append(count_part_in(abstract,keyword_list))
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


# ====================================================
# 统计一篇文档的关键词长度
# return length array
def count_kw_len(keyword_list):
    tokenzer = WordPunctTokenizer()
    len_kw = []
    for keyword in keyword_list:
        kw_words = tokenzer.tokenize(keyword)
        len_kw.append(len(kw_words))
    len_kw = np.array(len_kw)
    return len_kw


# 统计n篇文档的关键词长度
def count_n_kw_len(keyword_lists):
    n_kw_len = [count_kw_len(keyword_list) for keyword_list in keyword_lists]
    return n_kw_len


# 获取单文本的n_gram
def n_gram(text,n):
    tokenzer = WordPunctTokenizer()
    text = tokenzer.tokenize(text)
    n_grams = ngrams(text,n)
    return n_grams


# 获取n篇摘要的n_gram
def get_n_gram_list(abs_list, n):
    return [n_gram(abs) for abs in abs_list]


# 统计词频
def count_tf(n_grams):
    fdist = FreqDist(n_grams)



# 构造tf-idf corpus (word为单位)
def get_corpus_word(all_doc):
    tokenzer = WordPunctTokenizer()
    all_doc = [tokenzer.tokenize(doc) for doc in all_doc]  # 对所有摘要分词
    corpus = TextCollection(all_doc)
    return corpus

# # 构造tf-idf corpus (n_gram为单位)
# def get_corpus_ngram(n_grams):
#     n_gram_list = [n_gram for n_gram in n_grams]
#     return TextCollection(n_gram_list)


# 计算一篇摘要的所有词的tf-idf (以word为单位)
def tf_idf_abs(abstract, corpus):
    tokenzer = WordPunctTokenizer()
    abstract = tokenzer.tokenize(abs)  # 对摘要分词
    tf_idf_list = []
    for word in abstract:
        tf_idf = corpus.tf_idf(word,corpus)
        tf_idf_list.append(tf_idf)
    return tf_idf_list


# 计算n篇摘要的所有词的tf-idf (以word为单位)
def tf_idf_abs_all(all_abstract, corpus):
    all_tf_idf = []
    tokenzer = WordPunctTokenizer()
    all_abstract = [tokenzer.tokenize(abs) for abs in all_abstract]  # 对所有摘要分词
    for abs in all_abstract:
        tf_idf_list = []
        for word in abs:
            # tf = corpus.tf(word,corpus)
            # idf = corpus.idf(word)
            tf_idf = corpus.tf_idf(word,corpus)
            # print(word,': tf=',tf,' idf=',idf,' tf-idf=',tf_idf)
            tf_idf_list.append(tf_idf)
        # all_tf_idf.append([abs,tf_idf_list])
        all_tf_idf.append(tf_idf_list)
    return all_tf_idf


# 统计一篇文档的关键词(整个词组)的tf—idf corpus以word为单位
def tf_idf_kw(keywords, corpus):
    tf_idf_dict = {}
    for kw in keywords:
        tf_idf = corpus.tf_idf(kw,corpus)
        tf_idf_dict.update({kw : tf_idf})
    return tf_idf_dict





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
