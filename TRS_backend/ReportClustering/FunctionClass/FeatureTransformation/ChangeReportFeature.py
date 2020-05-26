import numpy as nu
from sklearn.decomposition import PCA
from TRS_backend.ReportClustering.Util.Enumeration import *

# 将某单份报告的特征向量数据转化为聚类需要的格式，其中图片的向量通过加和求平均的方式统一格式
def changeSingleReportUseAverage(data):
    # 1. 将多个procedure vector进行加和求平均
    original_procedure_vector=data.procedure_vector
    if len(original_procedure_vector)==0:
        return []
    new_procedure_vector=nu.zeros([len(original_procedure_vector[0]),])
    for vector in original_procedure_vector:
        new_procedure_vector=nu.add(vector,new_procedure_vector)
    new_procedure_vector=new_procedure_vector*1.0/len(original_procedure_vector)
    data.procedure_vector=new_procedure_vector

    # 2. 将多个problem vector进行加和求平均
    original_problem_vector=data.problem_vector
    if len(original_problem_vector)==0:
        return []
    new_problem_vector=nu.zeros([len(original_problem_vector[0]),])
    for vector in original_problem_vector:
        new_problem_vector=nu.add(new_problem_vector,vector)
    new_problem_vector=new_problem_vector*1.0/len(original_problem_vector)
    data.problem_vector=new_problem_vector

    # 3. 将problem widget vector进行加和求平均
    problem_widget_vector=data.problem_widget_vector
    if len(problem_widget_vector)==0:
        return []
    new_problem_widget_vector = nu.zeros([128,])
    for vector in problem_widget_vector:
        new_problem_widget_vector=nu.add(new_problem_widget_vector,vector)
    new_problem_widget_vector=new_problem_widget_vector*1.0/len(problem_widget_vector)
    data.problem_widget_vector=new_problem_widget_vector

    # 4. 将other widget vector进行加和求平均
    other_widget_vector=data.other_widget_vector
    if len(other_widget_vector)==0:
        return []
    new_other_widget_vector=nu.zeros([128,])
    none_num=0
    for item in other_widget_vector:
        if item is None:
            none_num=none_num+1
            continue
        temp=nu.zeros([128,])
        for inner in item:
            temp=nu.add(temp,inner)
        temp=temp*1.0/len(item)
        new_other_widget_vector=nu.add(new_other_widget_vector,temp)
    new_other_widget_vector=new_other_widget_vector*1.0/(len(other_widget_vector)-none_num)
    data.other_widget_vector=new_other_widget_vector


    return data

# 将某单份报告的特征向量数据转化为聚类需要的格式，其中图片的向量通过PCA降维至统一格式
def changeSingleReportUseReduction(data):
    # 1. 将多个procedure vector降维
    original_procedure_vector = data.procedure_vector
    new_procedure_vector = dimensionalityReduction(original_procedure_vector)
    data.procedure_vector = new_procedure_vector

    # 2. 将多个problem vector降维
    original_problem_vector = data.problem_vector
    new_problem_vector = dimensionalityReduction(original_problem_vector)
    data.problem_vector = new_problem_vector

    # 3. 将problem widget vector降维
    problem_widget_vector = data.problem_widget_vector
    new_problem_widget_vector = dimensionalityReduction(problem_widget_vector)
    data.problem_widget_vector = new_problem_widget_vector

    # 4. 将other widget vector降维
    other_widget_vector = data.other_widget_vector
    new_matrix=[]
    for item in other_widget_vector:
        if item is None:
            continue
        temp = dimensionalityReduction(item)
        new_matrix.append(temp)
    new_other_widget_vector = dimensionalityReduction(new_matrix)
    data.other_widget_vector = new_other_widget_vector

    return data

# 将 m * n 的数据降维至 1 * n
# param:    data 需要转化的矩阵
def dimensionalityReduction(data):
    data=nu.transpose(data)
    # 1 先针对每行降维
    model_pca_c = PCA(n_components=1)  # n_components设置降维后的维度
    pca = model_pca_c.fit(data).transform(data)

    # 2 按均值转化为1维
    result = nu.transpose(pca)

    return result[0]

# 将数据库中存储的特征数据转化的特征向量转化为聚类的统一格式
# param:    data 转化的特征向量数据列表
#           reduction 图片统一降维时使用的方式，定义在Reduction枚举类中
# return：  返回转化后的合理特征向量数据列表
def changeReoprtFeature(data,reduction):
    # 1. 对每个报告进行转化
    result=[]
    if reduction==Reduction.AVERAGE:
        for item in data:
            result.append(changeSingleReportUseAverage(item))
    elif reduction==Reduction.DIMENSIONAL:
        for item in data:
            result.append(changeSingleReportUseReduction(item))

    # 2. 返回转化结果
    return result
