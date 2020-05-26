import gensim
import jieba
import math
import numpy as np
import os


def sentence_vector(model, s):
    size = model.layer1_size
    words = []
    try:
        words = [x for x in jieba.cut(s, cut_all=True) if x != '']
    except:
        return np.zeros(size)
    v = np.zeros(size)
    length = len(words)
    for word in words:
        try:
            v += model[word]
        except:
            length -= 1
    if length != 0:
        v /= length
    return v


def text_feature_to_vector(result_list):
    curpath = os.path.dirname(os.path.realpath(__file__))
    father_path = os.path.dirname(curpath)
    model = gensim.models.Word2Vec.load(father_path + '\\word2vec_model\\bugdata_format_model_100')
    vectors_list = []
    for result in result_list:
        procedure_vector = []
        problem_vector = []
        procedure_list = result['procedures_list']
        problem_widget = result['problem_widget']
        problem_list = result['problems_list']
        for procedure in procedure_list:
            procedure_vector.append(sentence_vector(model, procedure))
        for problem in problem_list:
            problem_vector.append(sentence_vector(model, problem))
        widget_vector = sentence_vector(model, problem_widget)
        vector_total = {'procedure_vector': procedure_vector, 'widget_vector': widget_vector,
                        'problem_vector': problem_vector}
        vectors_list.append(vector_total)
    print('-----text feature to vector success-----')
    return vectors_list
