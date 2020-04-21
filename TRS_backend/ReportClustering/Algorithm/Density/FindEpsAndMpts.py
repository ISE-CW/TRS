import math
import copy
import numpy as np
from sklearn.cluster import DBSCAN


def loadDataSet(fileName, splitChar='\t'):
    """
    输入：文件名
    输出：数据集
    描述：从文件读入数据集
    """
    dataSet = []
    with open(fileName) as fr:
        for line in fr.readlines():
            curline = line.strip().split(splitChar)
            fltline = list(map(float, curline))
            dataSet.append(fltline)
    return dataSet


def dist(a, b):
    """
    :param a: 样本点
    :param b: 样本点
    :return: 两个样本点之间的欧式距离
    """
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def returnDk(matrix, k):
    """
    :param matrix: 距离矩阵
    :param k: 第k最近
    :return: 第k最近距离集合
    """
    Dk = []
    for i in range(len(matrix)):
        Dk.append(matrix[i][k])
    return Dk


def returnDkAverage(Dk):
    """
    :param Dk: k-最近距离集合
    :return: Dk的平均值
    """
    sum = 0
    for i in range(len(Dk)):
        sum = sum + Dk[i]
    return sum / len(Dk)


def CalculateDistMatrix(dataset):
    """
    :param dataset: 数据集
    :return: 距离矩阵
    """
    DistMatrix = [[0 for j in range(len(dataset))] for i in range(len(dataset))]
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            DistMatrix[i][j] = dist(dataset[i], dataset[j])
    return DistMatrix


def returnEpsCandidate(dataSet):
    """
    :param dataSet: 数据集
    :return: eps候选集合
    """
    DistMatrix = CalculateDistMatrix(dataSet)
    tmp_matrix = copy.deepcopy(DistMatrix)
    for i in range(len(tmp_matrix)):
        tmp_matrix[i].sort()
    EpsCandidate = []
    for k in range(1, len(dataSet)):
        Dk = returnDk(tmp_matrix, k)
        DkAverage = returnDkAverage(Dk)
        EpsCandidate.append(DkAverage)
    return EpsCandidate


def returnMinptsCandidate(DistMatrix, EpsCandidate, features):
    """
    :param DistMatrix: 距离矩阵
    :param EpsCandidate: Eps候选列表
    :return: Minpts候选列表
    """
    MinptsCandidate = []
    for k in range(len(EpsCandidate)):
        tmp_eps = EpsCandidate[k]
        tmp_count = 0
        for i in range(len(DistMatrix)):
            for j in range(len(DistMatrix[i])):
                if DistMatrix[i][j] <= tmp_eps:
                    tmp_count = tmp_count + 1
        MinptsCandidate.append(tmp_count / len(features))
    return MinptsCandidate


def returnClusterNumberList(dataset, EpsCandidate, MinptsCandidate):
    """
    :param dataset: 数据集
    :param EpsCandidate: Eps候选列表
    :param MinptsCandidate: Minpts候选列表
    :return: 聚类数量列表
    """
    np_dataset = np.array(dataset)  # 将dataset转换成numpy_array的形式
    ClusterNumberList = []
    for i in range(len(EpsCandidate)):
        clustering = DBSCAN(eps=EpsCandidate[i], min_samples=MinptsCandidate[i]).fit(np_dataset)
        num_clustering = max(clustering.labels_)
        ClusterNumberList.append(num_clustering)
    return ClusterNumberList

def findEpsandMpts(features):
    EpsCandidate = returnEpsCandidate(features)
    DistMatrix = CalculateDistMatrix(features)
    MinptsCandidate = returnMinptsCandidate(DistMatrix, EpsCandidate, features)
    ClusterNumberList = returnClusterNumberList(features, EpsCandidate, MinptsCandidate)
    continuous=1
    previous_cluster=ClusterNumberList[0]
    result_index=0
    for i in range(1,len(ClusterNumberList)):
        if ClusterNumberList[i]==previous_cluster:
            continuous=continuous+1
            if continuous>=3:
                result_index=i
                break
        else:
            previous_cluster=ClusterNumberList[i]
            continuous=1
    return EpsCandidate[result_index],MinptsCandidate[result_index]


# if __name__ == '__main__':
#     dataSet = loadDataSet('D:\TRS\TRS_backend\ReportClustering\FunctionClass\FileProduction\\788points.txt', splitChar=',')
#     EpsCandidate = returnEpsCandidate(dataSet)
#     DistMatrix = CalculateDistMatrix(dataSet)
#     MinptsCandidate = returnMinptsCandidate(DistMatrix, EpsCandidate)
#     ClusterNumberList = returnClusterNumberList(dataSet, EpsCandidate, MinptsCandidate)
#     print(EpsCandidate)
#     print(MinptsCandidate)
#     print('cluster number list is')
#     print(ClusterNumberList)