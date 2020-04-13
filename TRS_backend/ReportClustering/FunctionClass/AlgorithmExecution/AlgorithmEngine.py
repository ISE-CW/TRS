from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.Algorithm.Density.DBSCANAlgorithm import *
from TRS_backend.ReportClustering.Algorithm.Partition.KMeansAlgorithm import *
from TRS_backend.ReportClustering.Algorithm.Hierarchical.BIRCHAlgorithm import *
from TRS_backend.ReportClustering.Algorithm.Model.GMMAlgorithm import *
from TRS_backend.ReportClustering.Bean.ReportTree import *

# 用来针对某个数据集用特定算法进行特定的聚类操作
# data为以下数据的集合：将某份报告中的内容全部转化为一维向量，然后根据用户选择的数据拼接用一个向量来表示一份报告
# indexes为该聚类需要用到的报告索引
# algorithm为该次聚类选择的算法
# parameters为该次聚类需要的参数
def doAlgorithm(tree,algorithm, parameters,good_report_features):
    # 1.如果不是叶节点，即表示该节点已经做过聚类，遍历下面的子节点进行聚类操作
    if not tree.isLeave():
        sons = tree.sons
        for son in sons:
            doAlgorithm(son, algorithm, parameters, good_report_features)
    else:
        # 1.先将需要的（也就是该叶节点中values所包括的）good_report_features提取出来
        features = []
        values = tree.values
        for i in values:
            features.append(good_report_features[i])

        # 2.根据算法要求进行聚类操作，返回聚类的列表（聚类列表是features列表的索引号数据）
        clusters = []
        if algorithm == ClusteringAlgorithm.BIRCH:
            print('BIRCH')
        elif algorithm == ClusteringAlgorithm.DBSCAN:
            print('DBSCAN')
        elif algorithm == ClusteringAlgorithm.GMM:
            print('GMM')

        # KMeans算法
        elif algorithm == ClusteringAlgorithm.KMEANS:
            km = KMeansAlgorithm(parameters, features)
            clusters = km.go()

        # 3.将聚类列表中的索引数据对应到good_report_features的索引上去，并保存到页节点中去
        for cluster in clusters:
            # 对应
            node_values = []
            for item in cluster:
                node_values.append(values[item])
            # 建立叶节点
            node = ReportTree(node_values)
            tree.addSon(node)
    return tree