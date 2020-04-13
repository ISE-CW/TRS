from TRS_backend.ReportClustering.FunctionClass.SolveFile import getInitClusteringData
from TRS_backend.ReportClustering.FunctionClass.SolveFile import produceReport
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.FunctionClass.ReportTree import *
from TRS_backend.ReportClustering.Algorithm.Partition.KMeansAlgorithm import *
import numpy as np

# work_id表示该次聚类操作的id号
# choices包括了用户选择的所有聚类相关内容 是一个多层级的数组 每个数组项choice包含了如下内容
# *choice['relevant_data']是一个枚举类数组，里面包括了这次聚类需要的输入数据，可能是procedure_vector或procedure_vector和widget_vector的结合
# *choice['algorithm_chosen']是一个枚举项，表示该轮聚类采用什么算法
# *choice['parameters']是一个字典，根据不同的算法，进行相应的参数设置
def doClustering(workid, choices):
    # 1.获取报告聚类的初始数据
    cluster_data=getInitClusteringData(workid)
    good_reports=cluster_data['good_reports']
    bad_reports=cluster_data['bad_reports']

    # 2.初始化一个聚类结果数组，标号为正规报告的顺序编号,并将其存储到报告树的根节点处
    indexes=[]
    for i in range(0,len(good_reports)):
        indexes.append(i)
    root=ReportTree(indexes)

    # 3.分批次 按照用户要求进行聚类操作
    for choice in choices:
        # 1. 把需要的数据从多个向量组织为多个一维向量
        relevant_data=choice['relevant_data']
        data=[]
        for i in range(0,len(good_reports)):
            data.append([])

        for item in relevant_data:
            if item==InputData.PROCEDURE_VECTOR:
                for i in range(0,len(good_reports)):
                    data[i].extend(good_reports[i]['procedure_vector'].tolist())

            elif item==InputData.WIDGET_VECTOR:
                for i in range(0, len(good_reports)):
                    data[i].extend(good_reports[i]['widget_vector'].tolist())

            elif item==InputData.PROBLEM_VECTOR:
                for i in range(0, len(good_reports)):
                    data[i].extend(good_reports[i]['problem_vector'].tolist())

            elif item==InputData.IMAGE_VECTOR:
                for i in range(0, len(good_reports)):
                    data[i].extend(good_reports[i]['image_vector'].tolist())

        # 2. 根据选择的算法和填写的参数进行聚类操作
        for i in range(0,len(data)):
            data[i]=np.array(data[i])
        doAlgorithm(root,choice['algorithm_chosen'],choice['parameters'],data)

    # 4.生成特定形式的选择报告
    return produceReport(workid,choices,root,good_reports,bad_reports,1,1)

# 用来针对某个数据集用特定算法进行特定的聚类操作
# data为以下数据的集合：将某份报告中的内容全部转化为一维向量，然后根据用户选择的数据拼接用一个向量来表示一份报告
# indexes为该聚类需要用到的报告索引
# algorithm为该次聚类选择的算法
# parameters为该次聚类需要的参数
def doAlgorithm(tree,algorithm, parameters,good_report_features):
    # 1.如果不是叶节点，即表示该节点已经做过聚类，遍历下面的子节点进行聚类操作
    if not tree.isLeave():
        sons=tree.sons
        for son in sons:
            doAlgorithm(son,algorithm,parameters,good_report_features)
    else:
        # 1.先将需要的（也就是该叶节点中values所包括的）good_report_features提取出来
        features=[]
        values=tree.values
        for i in values:
            features.append(good_report_features[i])

        # 2.根据算法要求进行聚类操作，返回聚类的列表（聚类列表是features列表的索引号数据）
        clusters=[]
        if algorithm == ClusteringAlgorithm.BIRCH:
            print('BIRCH')
        elif algorithm == ClusteringAlgorithm.DBSCAN:
            print('DBSCAN')
        elif algorithm == ClusteringAlgorithm.GMM:
            print('GMM')

        # KMeans算法
        elif algorithm == ClusteringAlgorithm.KMEANS:
            km=KMeansAlgorithm(parameters,features)
            clusters=km.go()

        # 3.将聚类列表中的索引数据对应到good_report_features的索引上去，并保存到页节点中去
        for cluster in clusters:
            # 对应
            node_values=[]
            for item in cluster:
                node_values.append(values[item])
            # 建立叶节点
            node=ReportTree(node_values)
            tree.addSon(node)





