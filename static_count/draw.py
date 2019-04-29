#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from static_count import preprocess,count

# x_ticks: [1,2,3]
def draw(data, title, x_name, y_name, x_ticks,  x_ticklabels):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    fig = plt.figure(figsize=(8, 6))

    axes[0].violinplot(data, showmeans=False, showmedians=True)
    axes[0].set_title(title)

    axes[1].boxplot(data,)
    axes[1].set_title(title)
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks(x_ticks )
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
    plt.setp(axes, xticks=x_ticks,xticklabels=x_ticklabels,)
    plt.show()


def draw_violin(data, title, x_name, y_name, x_ticks,  x_ticklabels):
    # plt.boxplot(data,
    #             notch=False,  # box instead of notch shape
    #             sym='rs',  # red squares for outliers
    #             vert=True)  # vertical box aligmnent
    plt.grid()
    plt.violinplot(data, showmeans=False, showmedians=True)
    plt.xticks(x_ticks, x_ticklabels)
    plt.ylabel(y_name)
    plt.title(title)
    plt.show()


# 条形图
def draw_bar(label_list, num_list, title, color, x_label):
    # 设置中文字体和负号正常显示
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(num='fig1', figsize=(12, 9), dpi=75, facecolor='#FFFFFF', edgecolor='#0000FF')
    x = range(len(label_list))
    # rects1 = plt.bar(x=x, height=num_list, width=0.4, alpha=0.8, color=color)
    rects1 = plt.bar(x=x, height=num_list, width=0.5, color=color)
    plt.ylabel("document_num")  # 文档数

    plt.xticks(x, label_list)
    plt.xlabel(x_label)  #  count_num:单篇文档的统计数目  persent: 单篇文档的in/out的概率
    plt.title(title)
    # plt.legend()  # 设置题注
    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()


def draw_bar_2(label_lists, num_lists, title, x_lable):
    # 设置中文字体和负号正常显示
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(num='fig1', figsize=(12, 9), dpi=75, facecolor='#FFFFFF', edgecolor='#0000FF')

    x1 = range(len(label_lists[0]))
    x2 = range(len(label_lists[1]))

    rects1 = plt.bar(x=x1, height=num_lists[0], width=0.4, color='#6295FF', label="in")
    rects2 = plt.bar(x=[i + 0.4 for i in x2], height=num_lists[1], width=0.4, color='#FFAE50', label="out")
    plt.ylabel("document_num")   # 文档数

    x = range(max(len(x1),len(x2)))
    plt.xticks([index + 0.2 for index in x], label_lists[1])
    plt.xlabel(x_lable)
    plt.title(title)
    plt.legend()  # 设置题注
    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()


def draw_pie(persent, labels, title):

    fig = plt.figure(num='fig1', figsize=(12, 9), dpi=75, facecolor='#FFFFFF', edgecolor='#0000FF')
    explode = np.zeros(len(persent))  # 0.1 凸出这部分，
    # explode[0] = 0.1
    plt.axes(aspect=1)  # 设置为圆形

    # patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
    patches, l_text, p_text= plt.pie(x=persent, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.7)

    plt.title(title)
    # plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    plt.show()


if __name__ == "__main__":

    # load data
    # count in/out excel数据
    in_out_dir = './4_25/count_ttt1.xlsx'
    # in_out_data = preprocess.read_excel_count(in_out_dir)
    #
    # in_data = list(in_out_data[0])
    # out_data = list(in_out_data[1])
    # label_in = set(in_data)
    # label_out = set(out_data)
    # count_in_list = [in_data.count(num) for num in label_in]
    # count_out_list = [out_data.count(num) for num in label_out]

    # # 条形图 count_in_out count_num
    # x_lable = 'count_num'  # 单篇文档的统计数目
    # color_in = '#6295FF'
    # color_out = '#FFAE50'
    # draw_bar(label_in, count_in_list, 'isPart:1 isStem:1 isAnd:1    IN', color_in, x_lable)
    # draw_bar(label_out, count_out_list, 'isPart:1 isStem:1 isAnd:1  OUT', color_out, x_lable)
    # draw_bar_2([label_in, label_out], [count_in_list,count_out_list],'isPart:1 isStem:1 isAnd:1',x_lable)
    #
    # # 饼图 count_in_out_num_persent 统计57w篇文档中各count_num所占的比例
    # in_persent_data = count.get_percentage(in_data)
    # out_persent_data = count.get_percentage(out_data)
    # persent_in = list(in_persent_data.values())
    # persent_out = list(out_persent_data.values())
    # keys_in = list(in_persent_data.keys())
    # keys_out = list(out_persent_data.keys())
    #
    # print('in_num_persent:', in_persent_data)
    # print('out_num_persent: ',out_persent_data)
    # draw_pie(persent_in, keys_in, 'isPart:0 isStem:0 isAnd:-   in')
    # draw_pie(persent_out, keys_out, 'isPart:0 isStem:0 isAnd:-   out')


    # 统计每篇文档的in（out）在该篇文档的关键词总数中所占的比例（2（in），3（out），2/5，3/5）
    # 该比例在所有文档的比例数据中的比例
    in_out_persent = count.in_out_persents('./4_25/count_ft1.xlsx')
    # in_persent = in_out_persent[0]
    # out_persent = in_out_persent[1]
    # print(in_persent[:10])
    # print(out_persent[:10])
    # in_persent_persent = count.get_percentage(in_persent[0:10])
    # print(in_persent_persent)


    in_data = list(in_out_persent[0])
    # out_data = list(in_out_persent[1])

    # 全部的percent值作为横坐标
    # label_in = sorted(set(in_data))
    # print(label_in)
    # # label_out = sorted(set(out_data))
    # # print(label_out)
    # count_in_list = [in_data.count(num) for num in label_in]
    # # count_out_list = [out_data.count(num) for num in label_out]
    print('开始统计区间数据。。。')

    # 统一区间长度 横坐标：[0,0.1](0.1,0.2](0.2,0.3]...[0.9,1.0]
    # 直接统计
    # interval_dict = count.divde_interval(in_data)
    # label_in = list(interval_dict.keys())
    # count_in_list = list(interval_dict.values())
    # print(interval_dict)
    # 先count in 再划分
    percent_list = list(sorted(set(in_data)))
    count_in_all = [in_data.count(num) for num in percent_list]
    interval_num_dict = count.get_interval_num(percent_list)
    print('切分区间后各个区间的percent数目',interval_num_dict)
    label_in = list(interval_num_dict.keys())
    interval_num_list = list(interval_num_dict.values())
    count_in_list = count.devide_interval(interval_num_list, count_in_all)
    # start_id = 0
    # count_in_list = []
    # for num in interval_num_list:
    #     end_id = int(start_id + num)
    #     print(start_id,'  ', end_id)
    #     percent_sum = sum(count_in_all[start_id:end_id])
    #     count_in_list.append(percent_sum)
    #     start_id = end_id

    # 条形图 count_in_out count_persent
    x_lable = 'persent'  # 单篇文档的in/out的概率
    color_in = '#6295FF'
    color_out = '#FFAE50'
    draw_bar(label_in, count_in_list, 'isPart:0 isStem:1 isAnd:-    persent_IN', color_in, x_lable)
    # draw_bar(label_out, count_out_list, 'isPart:0 isStem:0 isAnd:-  persent_OUT', color_out, x_lable)
    # draw_bar_2([label_in, label_out], [count_in_list,count_out_list],'isPart:0 isStem:0 isAnd:-', x_lable)

    # 饼图  各比例在所有文档的比例数据中的比例
    in_persent_data = count.get_percentage(in_data)
    # # out_persent_data = count.get_percentage(out_data)
    # persent_in = list(in_persent_data.values())
    # # persent_out = list(out_persent_data.values())
    # keys_in = list(in_persent_data.keys())
    # # keys_out = list(out_persent_data.keys())

    # dict按key降序排序
    persent_in_data = sorted(in_persent_data.items(), key=lambda d:d[0])
    print(persent_in_data)
    persent_in_sorted = [item[1] for item in persent_in_data]
    persent_in = count.devide_interval(interval_num_list, persent_in_sorted)
    print(persent_in)
    keys_in = label_in
    # print('in_persent_persent:', in_persent_data)
    # print('out_persent_persent: ',out_persent_data)
    draw_pie(persent_in, keys_in, 'isPart:0 isStem:1 isAnd:-   in_persent')
    # draw_pie(persent_out, keys_out, 'isPart:0 isStem:0 isAnd:-   out_persent')


    # #   饼图 统计关键词个数的百分比
    # json_obj = preprocess.load_json('../data/all_title_abstract_keyword_clean.json')
    # _, keyword_len_list = preprocess.get_keywords(json_obj)
    # num_persent_dict = count.get_percentage(keyword_len_list)
    # num_persent = list(num_persent_dict.values())
    # print(sum(num_persent[:10]))
    # num_persent_new = num_persent[0:10]
    # more_than_10 = 0
    # for percent in num_persent[10:]:
    #     more_than_10 += percent
    # print(more_than_10)
    # num_persent_new.append(more_than_10)
    # lables = list(num_persent_dict.keys())[0:10]
    # lables.append('>10')
    # draw.draw_pie(num_persent_new, lables, 'persent of number of key phrase')
    #
    # # 条形图 count_in_out count_persent
    # x_lable = 'number of key phrase'
    # color_in = '#6295FF'
    # color_out = '#FFAE50'
    # number_set = list(set(keyword_len_list))
    # count_list = [keyword_len_list.count(number) for number in number_set[0:10]]
    # over_10 = 0
    # for number in number_set[10:]:
    #     over_10 += keyword_len_list.count(number)
    # count_list.append(over_10)
    # draw.draw_bar(lables, count_list, 'count for the number of key phrase', color_in, x_lable)
    #


    # 关键词单词个数(关键词长度)百分比统计 persent（pickle）
    # flatten_len_tokenize = preprocess.read('./4_24/persent_len_new')
    # persent = list(flatten_len_tokenize.values())
    # labels = list(flatten_len_tokenize.keys())
    # draw_pie(persent, labels, 'persent_len')


    # json_file = '../data/test_json'
    # json_obj = preprocess.load_json(json_file)
    # abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
    # n_kw_len = count.count_n_kw_len(keyword_list)
    # count_results = count.count_in_all(abstract_list, keyword_list, isPart=False, isStem=False)
    # in_num_list, out_num_list, _, _ = count.cal_in_out_avg(count_results)
    # all_data = [in_num_list,out_num_list]

    # draw(in_out_data, 'isPart:0 isStem:0 isAnd:-','x','num of keywords',[1,2],['in','out'])


    # draw(in_out_persents, 'in_out_persents_tt','','persents',[1,2],['in','out'])
    # draw_violin(in_out_persents[0],'violin plot: in_persents_ft','','persents',[1],['in'])
    # draw(len_data, 'length of keyphrase','x','length of keyphrase',[1],['x1'])


