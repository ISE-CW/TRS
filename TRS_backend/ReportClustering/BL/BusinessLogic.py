from TRS_backend.ReportClustering.FunctionClass.FeatureTransformation import ChangeSingleReportFeature as CReport
from TRS_backend.ReportClustering.FunctionClass.FeatureTransformation import FeatureExtraction as FExtraction
from TRS_backend.ReportClustering.Bean import ReportTree
from TRS_backend.ReportClustering.FunctionClass.AlgorithmExecution import AlgorithmEngine as AEngine
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.FunctionClass.FileProduction import ProduceReport as PReport
from TRS_backend.ReportClustering.FunctionClass.FileProduction import FormatTransformation as FTrans
import numpy as np

# 该方法通过工作ID将原始报告特征转化为聚类统一使用的向量
# param:    workid 该操作的工作id
# return:   dict {good_features,bad_features} 转化后符合要求的特征向量数组与转化后不符合要求的特征向量数组
def featureTransformation(workid):
    #1 先从数据库中把该次执行所需的特征数据提取出来
    good_features,bad_features=FExtraction.getFeaturesContent(workid)

    #2 将刚才提取出来的特征数据进行向量化
    good_vectors=FExtraction.getFeaturesVector(good_features)
    bad_vectors=FExtraction.getFeaturesVector(bad_features)

    #3 将得到的向量根据聚类的统一要求进行格式转化
    good_data=[]
    bad_data=[]
    for i in range(0,len(good_vectors)):
        good_data.append(CReport.changeSingleReport(good_vectors[i]))

    for i in range(0,len(bad_vectors)):
        bad_data.append(CReport.changeSingleReport(bad_vectors[i]))

    #4 返回转化后的数据
    return {
        'good_features':good_data,
        'bad_features':bad_data
    }

# 该方法通过featureTransformation方法得到的返回值与用户的配置作为输入进行算法的执行操作
# param:    features:dict {good_features,bad_features}
#           choices: list
#           choices包括了用户选择的所有聚类相关内容 是一个多层级的数组 每个数组项choice包含了如下内容
#           *choice['relevant_data']是一个枚举类数组，里面包括了这次聚类需要的输入数据，可能是procedure_vector或procedure_vector和widget_vector的结合
#           *choice['algorithm_chosen']是一个枚举项，表示该轮聚类采用什么算法
#           *choice['parameters']是一个字典，根据不同的算法，进行相应的参数设置
# return    ReportTree 一棵完成了聚类任务的测试报告树
def algorithmExecution(features,choices):
    #1 建立一棵报告树，用初始坐标表示
    good_features=features['good_features']
    bad_features=features['bad_features']
    indexes=[]
    for i in range(0, len(good_features)):
        indexes.append(i)
    root=ReportTree(indexes)

    #2 将用户的配置与符合要求的特征向量以及树传递给AlgorithmEngine进行聚类操作
    for choice in choices:
        # 2.1 把需要的数据从多个向量组织为多个一维向量
        relevant_data=choice['relevant_data']
        data=[]
        for i in range(0,len(good_features)):
            data.append([])

        for item in relevant_data:
            if item==InputData.PROCEDURE_VECTOR:
                for i in range(0,len(good_features)):
                    data[i].extend(good_features[i]['procedure_vector'].tolist())

            elif item==InputData.WIDGET_VECTOR:
                for i in range(0, len(good_features)):
                    data[i].extend(good_features[i]['widget_vector'].tolist())

            elif item==InputData.PROBLEM_VECTOR:
                for i in range(0, len(good_features)):
                    data[i].extend(good_features[i]['problem_vector'].tolist())

            elif item==InputData.IMAGE_VECTOR:
                for i in range(0, len(good_features)):
                    data[i].extend(good_features[i]['image_vector'].tolist())

        # 2.2 根据选择的算法和填写的参数进行聚类操作
        for i in range(0,len(data)):
            data[i]=np.array(data[i])
        AEngine.doAlgorithm(root,choice['algorithm_chosen'],choice['parameters'],data)

    #3 返回报告树
    return root

def fileProduction(workid, tree, choices, good_features, bad_features, format):
    text=PReport.produceReport(workid,choices,tree,good_features,bad_features,1,1)
    fileName='\TRS\TRS_backend\ReportClustering\DataFile\ClusteringFile\\' + workid + '_clustering_report.md';
    if format==FileFormat.PDF:
        text=FTrans.markdownToPDF(text)
        fileName='\TRS\TRS_backend\ReportClustering\DataFile\ClusteringFile\\' + workid + '_clustering_report.pdf'
    elif format==FileFormat.WORD:
        text=FTrans.markdownToWord(text)
        fileName='\TRS\TRS_backend\ReportClustering\DataFile\ClusteringFile\\' + workid + '_clustering_report.word'

    file = open(fileName, 'w')
    file.write(text)
    file.close()
