# coding:utf-8
import jieba
import sys
import time

sys.path.append("../../")
import codecs
import os
import re

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

def LoadStopWordList(filepath):
    """
    创建停用词list
    """
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def FenCi(readfile, outfile, stopwords):
    # r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+0123456789'
    for line in readfile.readlines():
        # 更高效的字符串替换
        # line = re.sub(r, ' ', line)
        newline = jieba.cut(line, cut_all=False)
        outstr_list = list()
        # for word in newline:
        #     if word not in stopwords:
        #         outstr_list.append(word)
        for word in newline:
            outstr_list.append(word)
        str_out = ' '.join(outstr_list)
        # str_out.encode('utf-8')\
        print(str_out)
        print(str_out, file=outfile, end=' ')

def fenci(sample):
    result = jieba.cut(sample,cut_all=False)
    outstr_list = list()
    curpath = os.path.dirname(os.path.realpath(__file__))
    stopwords = LoadStopWordList(curpath + '\\fenci\\stop_words.txt')
    for word in result:
        if word not in stopwords:
            outstr_list.append(word)
    str_out = ' '.join(outstr_list)
    return str_out

if __name__ == '__main__':
    fromdir = "./data/"
    todir = "./fenci/"
    stopWordFile = "stop_words.txt"
    # 一次只能对一个文档进行分词
    # file = "problem.txt"
    file = "procedure.txt"
    infile = open(os.path.join(fromdir, file), 'r', encoding='UTF-8')
    outfile = open(os.path.join(todir, file), 'w+', encoding='UTF-8')
    # 这里加载停用词
    stopwords = [line.strip() for line in open(os.path.join(todir, stopWordFile), 'r', encoding='UTF-8').readlines()]
    FenCi(infile, outfile, stopwords)
    infile.close()
    outfile.close()
