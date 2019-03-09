#! /user/bin/evn python
# -*- coding:utf8 -*-

import re
import codecs
import numpy as np
import gensim
from gensim.test.utils import datapath
from numpy import linalg
import operator


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    :param string:
    :return: string
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    # string = re.sub('[_A-Z ]', ' ', string)
    return string.strip().lower()


# 加载词典
def load_vocab(vacab_dir):
    vocab = []
    with codecs.open(filename=vacab_dir, encoding='utf-8') as fp:
        while True:
            line = fp.readline()
            if not line:
                print('get vacab successful!')
                return vocab

            tmp = line.strip().split(' ')
            vocab.append(tmp[0])


def load_all_data(file_path, vocab):
    docs = []
    key_phrases = []
    key_phrase_extracs = []
    line_num = 0
    with codecs.open(filename=file_path, encoding='utf-8') as fp:
        while True:
            line_num += 1
            print(line_num)
            line = fp.readline()
            if not line:
                print('get_headerFile successful!')
                # docs = [clean_str(str(doc)) for doc in docs]
                return [docs, key_phrases, key_phrase_extracs]

            tmp = line.strip().split('\t')
            doc_split = clean_str(tmp[0]).split(' ')
            for i in range(len(doc_split)):
                if not vocab.__contains__(doc_split[i]):
                    doc_split[i] = 'unknown'
            # print(doc_split)
            # print('\n')
            docs.append(doc_split)

            print(tmp)
            key_phrases.append(tmp[1].split(';'))

            extracs_tmp = tmp[2].split(';')
            doc_phrase_weight = {}
            for i in range(len(extracs_tmp)):
                extracs_phrase_weight = extracs_tmp[i].split('|||')
                try:
                    doc_phrase_weight.update({extracs_phrase_weight[1]: float(extracs_phrase_weight[0])})
                except IndexError:
                    print('该行提取的关键术语数据有误：'+ str(tmp[2]))
                    print('具体数据错误：' + str(extracs_phrase_weight))

                else:
                    doc_phrase_weight.update({extracs_phrase_weight[1]: float(extracs_phrase_weight[0])})
                # doc_phrase_weight.update({extracs_phrase_weight[1]: float(extracs_phrase_weight[0])})

            # 按value升序排序
            # doc_phrase_weight = sorted(doc_phrase_weight.items(), key=operator.itemgetter(1))

            # 按value值降序排序 =================转成了list
            # doc_phrase_weight = sorted(doc_phrase_weight.items(), key=lambda d: d[1], reverse=True)
            key_phrase_extracs.append(doc_phrase_weight)

            # print(key_phrase_extracs[:,:,0:3] )
            # print(doc_phrase_weight[0:3] +  '   '+ str(doc_phrase_weight[0][1]))

            # print(tmp[2])
            # print("=====" + str(doc_phrase_weight) + '\n')



# 对每篇文章分词
def get_docs(file_path):
    docs = []
    with codecs.open(filename=file_path, encoding='utf-8') as fp:
        while True:
            line = fp.readline()
            if not line:
                print('get docs successful!')
                return docs

            tmp = line.strip().split('\t')
            # print(tmp[0])
            doc = clean_str(tmp[0])
            doc_split = doc.split(' ')
            docs.append(doc_split)


# 加载词向量/计算文档向量
def doc2vec(vector_dir, docs):
    all_doc_vectors = []
    print('加载词向量模型...')
    word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(fname=vector_dir, binary=False)
    print('词向量模型加载完毕！')
    # v1 = word2vec_model['virtually']
    # print(v1)
    # word2vev_model = gensim.models.keyedvectors._load_word2vec_format(datapath(vector_dir), binary=False)
    for i in range(len(docs)):
        doc = docs[i]
        print(doc)
        vector = np.zeros(300)
        for j in range(len(doc)):
            vector = vector + np.array(word2vec_model[doc[j]])
        # 文档向量：词向量取均值
        doc_vector = vector / len(doc)
        all_doc_vectors.append(doc_vector)
    print('文档向量计算完毕！\n')
    return np.array(all_doc_vectors)


# 计算全部文档两两相似度 并按相似度降序排序
# [[(1,1),(2,0.8),(3,0.5)...],[(1,0.6),(2,1),(3,0.5)...],[]]
def calculate_doc_sim(doc_vectors):
    doc_num = len(doc_vectors)
    # all_doc_sim = np.zeros([doc_num, doc_num])
    all_doc_sim = []
    for i in range(doc_num):
        v1 = doc_vectors[i]
        v1_sim = {}
        for j in range(doc_num):
            v2 = doc_vectors[j]
            v1_v2_dot = np.dot(v1, v2)
            denom = linalg.norm(v1) * linalg.norm(v2)
            cos = v1_v2_dot / denom  # 余弦值
            v1_sim.update({j : cos})
            # all_doc_sim[i][j] = cos
        # 按value值降序排序 ============v1_sim转换成了list
        v1_sim = sorted(v1_sim.items(), key=lambda d: d[1], reverse=True)
        all_doc_sim.append(v1_sim)
    print('文档相似度计算完毕！\n')
    return all_doc_sim


# 抽取所有文档的top n篇相似文档
def get_topN_sim(all_doc_sim, topN):
    return all_doc_sim[:,:,0:topN]  # doc_num * topN


# 对于一篇文档： 融合其topN篇相似的外部文档的全部key phrase
def get_external(topN_doc_sims, all_original_kp, currunt_docID):
    # topN_doc_sims:[(6,0.9),(10,0.8),(3,0.5)...],topN * 2 一篇文档的相似文档及相似度集合
    # all_original_kp: 所有文档的原始关键术语
    external_key_phrase = {}
    key_phrases = {}  #{'k1':[0.2,0.3]; 'k2':[0.5,0.6,0.8]}
    for i in range(len(topN_doc_sims)):
        # 获取第i篇与本篇doc相似的文档sim
        sim = topN_doc_sims[i][1]
        # 获取第i篇与本篇doc相似的文档id
        sim_docID = topN_doc_sims[i][0]

        # 跳过当前文档
        if sim_docID != currunt_docID :
            # 根据相似文档id获取相似文档的关键术语
            sim_doc_keys = all_original_kp[sim_docID]
            for j in range(len(sim_doc_keys)):
                key = sim_doc_keys[j]
                if not key_phrases.__contains__(sim_doc_keys[j]):
                    key_phrases.update({sim_doc_keys[j]: [sim]})
                else:
                    sim_list = key_phrases[sim_doc_keys[j]]
                    sim_list.append(sim)
                    key_phrases.update({sim_doc_keys[j]: sim_list})

    #  计算每个key phrase的权重均值
    for key in key_phrases:
        sim_array = np.array(key_phrases[key])
        # 融合权重：取均值
        # key_weight = np.average(sim_array)
        # 融合权重：求和
        key_weight = np.sum(sim_array)
        external_key_phrase.update({key : key_weight})
    return external_key_phrase


# 对于一篇文档：融合内外部关键术语
# 目标文档本身权重 p  外部文档权重 1-p
def merge(original_dict, external_dict, p):
    merge_dict = {}
    # all_keys = original_dict.keys() | external_dict.keys()
    for original_key in original_dict:
        # 原文档有 外部文档没有
        if not external_dict.__contains__(original_key):
            weight = p * original_dict[original_key]
        # 原文档有 外部文档也有
        else:
            weight = p * original_dict[original_key] + (1-p)* external_dict[original_key]
        merge_dict.update({original_key: weight})

    # 原文档没有 外部文档有
    for external_key in external_dict:
        if not merge_dict.__contains__(external_key):
            weight = (1-p) * external_dict[external_key]
            merge_dict.update({external_key: weight})

    return merge_dict


def extract_all(all_doc_sim, all_original_kp, topN,  all_kp_extracs, p):
    all_merged_kp = []
    for i in range(len(all_doc_sim)):
        shape = np.array(all_doc_sim).shape
        topN_doc_sims = all_doc_sim[i][:topN+1] # 相似文档里包含里目标文档本身
        external_dict = get_external(topN_doc_sims,all_original_kp, currunt_docID=i)
        original_dict = all_kp_extracs[i]
        one_merge_dict = merge(original_dict,external_dict,p)
        all_merged_kp.append(one_merge_dict)
    return all_merged_kp


def save_merged_results(result_list, save_dir):
    fp = codecs.open(filename=save_dir, mode='w', encoding='utf-8',)
    for i in range(len(result_list)):
        line = str(sorted(result_list[i].items(), key=lambda d: d[1], reverse=True))
        fp.write(line + '\n')
    fp.close()


def evaluate(merged_kp, original_kp):
    precision = []
    recall = []
    doc_num = len(original_kp)
    for i in range(doc_num):
        #  计算每一篇文档的p和r
        correct_num = 0
        for j in range(len(merged_kp)):
            if original_kp.__contains__(merged_kp[i][j]):
                correct_num += 1
        pi = correct_num / len(merged_kp[i])
        ri = correct_num / len(original_kp[i])
        precision.append(pi)
        recall.append(ri)
    # 计算全部文档的平均p和r
    precision = np.array(precision)
    recall = np.array(recall)
    precision_avg = np.average(precision)
    recall_avg = np.average(recall)
    f = (2 * precision_avg * recall_avg) / (precision_avg + recall_avg)

    return precision_avg, recall_avg, f, precision,recall


def save_evaluate_results(result_array, save_dir):
    fp = codecs.open(filename=save_dir, mode='w', encoding='utf-8',)
    for i in range(len(result_array)):
        line = str(result_array[i])
        fp.write(str(i) + ":" + line + '\n')
    fp.close()

if __name__ == '__main__':
    vector_dir = 'sg.word2vec.300d'
    file_path = 'doc_test.txt'
    vocab_dir ='vocab_sg300d.txt'
    merged_results_dir = 'merged_results.txt'
    precision_dir = 'precision.txt'
    recall_dir = 'recall.txt'

    # prepare for data
    vocab = load_vocab(vocab_dir)
    docs, all_original_kp, all_kp_extracs = load_all_data(file_path, vocab)
    all_doc_vectors = doc2vec(vector_dir, docs)
    all_doc_sim = calculate_doc_sim(all_doc_vectors)

    # doc_sim = calculate_doc_sim(all_doc_vectors)
    # for i in range(len(doc_sim)):
    #     print('doc'+ str(i))
    #     print(str(doc_sim[i]))
    #     print('\n')

    # merge:
    all_merged_kp = extract_all(all_doc_sim, all_original_kp, 2, all_kp_extracs,0.6)
    print('内外部融合结果：')
    for i in range(len(all_merged_kp)):
        print(sorted(all_merged_kp[i].items(), key=lambda d: d[1], reverse=True))
    save_merged_results(all_merged_kp, merged_results_dir)

    # evaluate:
    precision_avg, recall_avg, f, precision, recall = evaluate(all_merged_kp, all_original_kp)
    save_evaluate_results(precision, precision_dir)
    save_evaluate_results(recall, recall_dir)
    print('平均检准率： ' + precision_avg)
    print('平均检全率： ' + recall_avg)
    print('F值： ' + f)




