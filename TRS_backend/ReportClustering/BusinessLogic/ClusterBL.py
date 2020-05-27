from TRS_backend.ReportClustering.FunctionClass.FeatureTransformation import ChangeReportFeature as CReport
from TRS_backend.ReportClustering.FunctionClass.FeatureTransformation import FeatureExtraction as FExtraction
from TRS_backend.ReportClustering.Bean.ReportTree import *
from TRS_backend.ReportClustering.FunctionClass.AlgorithmExecution import AlgorithmEngine as AEngine
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.FunctionClass.FileProduction import ProduceReport as PReport
from TRS_backend.ReportClustering.FunctionClass.FileProduction import FormatTransformation as FTrans
from TRS_backend.ReportClustering.Dao.ClusteringDao import *
import numpy as np
from TRS_backend.ReportClustering.Util.Transformation import *
import json

# 该方法通过工作ID将原始报告特征转化为聚类统一使用的向量
# param:    workid 该操作的工作id
#           reduction 图片降维的方式，再Reduction枚举类中有定义
# return:   dict {good_features,bad_features} 转化后符合要求的特征向量数组与转化后不符合要求的特征向量数组
def featureTransformation(workid, reduction):
    #1 先从数据库中把该次执行所需的特征数据提取出来
    good_features,bad_features=FExtraction.getFeaturesContent(workid)

    #2 将刚才提取出来的特征数据进行向量化
    good_vectors=FExtraction.getFeaturesVector(good_features)
    bad_vectors=FExtraction.getFeaturesVector(bad_features)

    #3 将得到的向量根据聚类的统一要求进行格式转化
    good_data=CReport.changeReoprtFeature(good_vectors,reduction)
    #bad_data=CReport.changeReoprtFeature(bad_vectors,reduction)

    #4 返回转化后的数据
    return good_data,bad_features

# 该方法通过featureTransformation方法得到的返回值与用户的配置作为输入进行算法的执行操作
# param:    features: ReportVector
#           choices: list
#           choices包括了用户选择的所有聚类相关内容 是一个多层级的数组 每个数组项choice包含了如下内容
#           *choice['relevant_data']是一个枚举类数组，里面包括了这次聚类需要的输入数据，可能是procedure_vector或procedure_vector和widget_vector的结合
#           *choice['algorithm_chosen']是一个枚举项，表示该轮聚类采用什么算法
#           *choice['parameters']是一个字典，根据不同的算法，进行相应的参数设置
# return    ReportTree 一棵完成了聚类任务的测试报告树
def algorithmExecution(features,choices):
    #1 建立一棵报告树，用初始坐标表示
    indexes=[]
    for i in range(0, len(features)):
        indexes.append(i)
    root=ReportTree(indexes)

    #2 将用户的配置与符合要求的特征向量以及树传递给AlgorithmEngine进行聚类操作
    for choice in choices:
        # 2.1 把需要的数据从多个向量组织为多个一维向量
        relevant_data=choice['relevant_data']
        data=[]
        for i in range(0,len(features)):
            data.append([])

        for item in relevant_data:
            if changeChineseToEnum(item)==InputData.PROCEDURE_VECTOR:
                for i in range(0,len(features)):
                    data[i].extend(features[i].procedure_vector.tolist())

            elif changeChineseToEnum(item)==InputData.WIDGET_VECTOR:
                for i in range(0, len(features)):
                    data[i].extend(features[i].widget_vector.tolist())

            elif changeChineseToEnum(item)==InputData.PROBLEM_VECTOR:
                for i in range(0, len(features)):
                    data[i].extend(features[i].problem_vector.tolist())

            elif changeChineseToEnum(item)==InputData.PROBLEM_WIDGET_VECTOR:
                for i in range(0, len(features)):
                    data[i].extend(features[i].problem_widget_vector.tolist())

            elif changeChineseToEnum(item)==InputData.OTHER_WIDGET_VECTOR:
                for i in range(0,len(features)):
                    data[i].extend(features[i].other_widget_vector.tolist())

        # 2.2 根据选择的算法和填写的参数进行聚类操作
        for i in range(0,len(data)):
            data[i]=np.array(data[i])
        for param in choice['parameters']:
            if choice['parameters'][param]=='None':
                choice['parameters'][param]=None
            elif choice['parameters'][param]=='True':
                choice['parameters'][param]=True
            elif choice['parameters'][param]=='False':
                choice['parameters'][param]=False
        AEngine.doAlgorithm(root,changeChineseToEnum(choice['algorithm_chosen']),choice['parameters'],data)

    #3 返回报告树
    return root

# 该方法将结果报告树打印出来
# param:    workid 该操作的工作id
#           tree 结果报告树
#           choices: list
#           choices包括了用户选择的所有聚类相关内容 是一个多层级的数组 每个数组项choice包含了如下内容
#           *choice['relevant_data']是一个枚举类数组，里面包括了这次聚类需要的输入数据，可能是procedure_vector或procedure_vector和widget_vector的结合
#           *choice['algorithm_chosen']是一个枚举项，表示该轮聚类采用什么算法
#           *choice['parameters']是一个字典，根据不同的算法，进行相应的参数设置
#           good_features: 合规的特征向量数据集
#           bad_features: 不合规的特征向量数据集
#           reduction: 图片向量的降维方式，定义在Reduction枚举类中
#           create_time: 用户创建聚类操作的时间
# return:   /
def fileProduction(srid,workid, tree, choices, reduction, good_features, bad_features, create_time, choice_file):
    text=PReport.produceReport(workid,choices,reduction,tree,good_features,bad_features,True)
    fileName='\TRS\TRS_backend\ReportClustering\DataFile\ClusteringFile\\' + str(srid) +'_clustering_report.md';
    file = open(fileName, 'w', encoding='utf-8')
    file.write(text)
    file.close()

    saveClusteringReport(srid,workid,create_time,reduction,choice_file,fileName,State.FINISH.value)


# 该方法将结果报告下载到用户本地，将文件传递给前端
# param:    workid 该操作的工作id
#           format 需要的文件形式，定义在FileFormat枚举类中
# return:   文件
def downloadFile(workid,format):
    md_file=''
    if format == FileFormat.PDF:
        return FTrans.markdownToPDF(md_file)
    elif format == FileFormat.WORD:
        return FTrans.markdownToWord(md_file)

