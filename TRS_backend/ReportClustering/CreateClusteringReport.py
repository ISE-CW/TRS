from TRS_backend.ReportClustering.FunctionClass.Schedule import doClustering
from TRS_backend.ReportClustering.Util.Enumeration import *
# work_id表示该次聚类操作的id号
# choices包括了用户选择的所有聚类相关内容 是一个多层级的数组 每个数组项choice包含了如下内容
# *choice['relevant_data']是一个枚举类数组，里面包括了这次聚类需要的输入数据，可能是procedure_vector或procedure_vector和widget_vector的结合
# *choice['algorithm_chosen']是一个枚举项，表示该轮聚类采用什么算法
# *choice['parameters']是一个字典，根据不同的算法，进行相应的参数设置
def getClusteringReport(workid,choices):
    result=doClustering(workid,choices)
    file=open('\TRS\TRS_backend\ReportClustering\DataFile\ClusteringFile\\'+workid+'_clustering_report.md','w')
    file.write(result)
    file.close()

choice1={
    'relevant_data':[InputData.PROCEDURE_VECTOR,InputData.WIDGET_VECTOR],
    'algorithm_chosen':ClusteringAlgorithm.KMEANS,
    'parameters':{
        'n_clusters':2,
        'init':'k-means++',
        'n_init': 10,
        'max_iter' : 300,
        'tol' : 0.0001,
        'precompute_distances' : 'auto',
        'verbose' : 0,
        'random_state' : None,
        'copy_x' : True,
        'n_jobs' : 1,
        'algorithm': 'auto'
    }
}
choice2={
    'relevant_data':[InputData.PROBLEM_VECTOR,InputData.IMAGE_VECTOR],
    'algorithm_chosen':ClusteringAlgorithm.KMEANS,
    'parameters':{
        'n_clusters':0,
        'init':'k-means++',
        'n_init' : 10,
        'max_iter' : 300,
        'tol' : 0.0001,
        'precompute_distances' : 'auto',
        'verbose' : 0,
        'random_state' : None,
        'copy_x' : True,
        'n_jobs' : 1,
        'algorithm': 'auto'
    }
}
choices=[choice1,choice2]
getClusteringReport('workid',choices)