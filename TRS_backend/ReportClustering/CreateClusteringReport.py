from TRS_backend.ReportClustering.FunctionClass.Schedule import doClustering
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.BusinessLogic.ClusterBL import *
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

# kmeans
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

# dbscan
choice2={
    'relevant_data':[InputData.PROBLEM_VECTOR,InputData.PROBLEM_WIDGET_VECTOR,InputData.OTHER_WIDGET_VECTOR],
    'algorithm_chosen':ClusteringAlgorithm.DBSCAN,
    'parameters':{
        'eps' : 0,
        'min_samples' : 0,
        'metric' : 'euclidean',
        'metric_params' : None,
        'algorithm' : 'auto',
        'leaf_size' : 30,
        'p' : None,
        'n_jobs' : None,
        'features' : [],
    }
}

# birch
choice3={
    'relevant_data':[InputData.PROBLEM_VECTOR,InputData.PROBLEM_WIDGET_VECTOR,InputData.OTHER_WIDGET_VECTOR],
    'algorithm_chosen':ClusteringAlgorithm.BIRCH,
    'parameters':{
        'threshold' : 0,
        'branching_factor' : 0,
        'n_clusters' : None,
        'compute_labels' : True,
        'copy' : True,
    }
}

# gmm
choice4={
    'relevant_data':[InputData.PROCEDURE_VECTOR,InputData.WIDGET_VECTOR],
    'algorithm_chosen':ClusteringAlgorithm.GMM,
    'parameters':{
        'n_components' : 0,
        'covariance_type' : 'full',
        'tol' : 1e-3,
        'reg_covar' : 1e-6,
        'max_iter' : 100,
        'n_init' :1,
        'init_params' : 'random',
        'weights_init' : None,
        'means_init' : None,
        'precisions_init' : None,
        'random_state' : None,
        'warm_start' : False,
        'verbose' : 0,
        'verbose_interval' : 10
    }
}

choices=[choice4,choice3]
good_features,bad_features=featureTransformation(1, Reduction.AVERAGE)
tree=algorithmExecution(good_features,choices)
fileProduction(1,tree,choices,Reduction.AVERAGE,good_features,bad_features,'20200416222410')
