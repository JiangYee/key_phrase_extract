#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from static_count import preprocess,count

# x_ticks: [1,2,3]
def draw(data, title, x_name, y_name, x_ticks,  x_ticklabels):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    fig = plt.figure(figsize=(8, 6))

    axes[0].violinplot(data, showmeans=False, showmedians=True)
    axes[0].set_title('violin plot: ' + title)

    axes[1].boxplot(data,)
    axes[1].set_title('box plot: ' + title)
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

if __name__ == "__main__":

    # # load data
    # # count in/out excel数据
    # in_out_dir = './resulte_data/count_ft1.xlsx'
    # in_out_data = preprocess.read_excel_count(in_out_dir)

    # count_in_out_persents
    # in_out_persents = count.in_out_persents(in_out_dir)
    # in_persents = [num for num in in_out_persents[0] if num < 4]

    # len（pickle）
    print(len(preprocess.read('flatten_len')))
    len_dir= 'flatten_len10'
    len_data = preprocess.read(len_dir)
    print(len(len_data))
    len_data = [data for data in len_data if data < 6]
    print(len(len_data))
    print(max(len_data))

    # json_file = '../data/test_json'
    # json_obj = preprocess.load_json(json_file)
    # abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
    # n_kw_len = count.count_n_kw_len(keyword_list)
    # count_results = count.count_in_all(abstract_list, keyword_list, isPart=False, isStem=False)
    # in_num_list, out_num_list, _, _ = count.cal_in_out_avg(count_results)
    #
    # all_data = [in_num_list,out_num_list]

    # draw(in_out_data, 'in_out_ft','x','num of keywords',[1,2],['in','out'])
    # draw(in_out_persents, 'in_out_persents_tt','','persents',[1,2],['in','out'])
    # draw_violin(in_out_persents[0],'violin plot: in_persents_ft','','persents',[1],['in'])
    # draw(len_data, 'length of keyphrase','x','length of keyphrase',[1],['x1'])

