#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: toddler

import jieba
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def cut_analyze(input_file):
    """
    :param input_file: 输入带切词分析的文本路径
    :return: (list1, list2) list1切词处理后的列表结果, list2输出切词处理排序后的词频结果, 列表-元祖嵌套结果
    """
    cpc_dict_path = u'user_dict/cpc_dictionary.txt'
    stop_words_path = u'user_dict/stopword.txt'

    with open(input_file) as f:
        content = f.read()

    with open(stop_words_path) as sf:
        st_content = sf.readlines()

    jieba.load_userdict(cpc_dict_path)  # 加载针对全国人民代表大会的分词词典

    stop_words = [line.strip().decode('utf-8') for line in st_content]  # 将读取的数据都转为unicode处理

    seg_list = jieba.cut(content, cut_all=False)  # 精确模式

    filter_seg_list = list()

    for seg in seg_list:
        goal_word = ''.join(re.findall(u'[\u4e00-\u9fa5]+', seg)).strip()  # 过滤所有非中文字符内容
        if len(goal_word) != 0 and not stop_words.__contains__(goal_word):  # 过滤分词结果中的停词内容
            # filter_seg_list.append(goal_word.encode('utf-8'))  # 将unicode的文本转为utf-8保存到列表以备后续处理
            filter_seg_list.append(goal_word)  # 将unicode的文本转为utf-8保存到列表以备后续处理

    seg_counter_all = Counter(filter_seg_list).most_common()  # 对切词结果按照词频排序

    # for item in seg_counter_all:
    #     print "词语: {0} - 频数: {1}".format(item[0].encode('utf-8'), item[1])

    return filter_seg_list, seg_counter_all


def main():
    input_file_path = u'input_file/nighteen-cpc.txt'
    cut_data, sort_data = cut_analyze(input_file=input_file_path)
    font = r'E:\Codes\National_Congress_of_ CPC\assets\msyh.ttf'
    wc = WordCloud(collocations=False, font_path=font, width=3600, height=3600, margin=2)
    wc.generate_from_frequencies(dict(sort_data))
    plt.figure()
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()