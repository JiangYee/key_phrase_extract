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


if __name__ == "__main__":

    # # load data
    # # count in/out excel数据
    # in_out_dir = './resulte_data/count_ff.xlsx'
    # in_out_data = preprocess.read_excel_count(in_out_dir)

    # len（pickle）
    len_dir= './resulte_data/len'
    len_data = preprocess.read(len_dir)

    # json_file = '../data/test_json'
    # json_obj = preprocess.load_json(json_file)
    # abstract_list, keyword_list, _ = preprocess.get_info(json_obj)
    # n_kw_len = count.count_n_kw_len(keyword_list)
    # count_results = count.count_in_all(abstract_list, keyword_list, isPart=False, isStem=False)
    # in_num_list, out_num_list, _, _ = count.cal_in_out_avg(count_results)
    #
    # all_data = [in_num_list,out_num_list]

    draw(len_data, 'test_in_out','x','num of keywords',[1,2],['in','out'])

