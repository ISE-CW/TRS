from TRS_backend.ReportClustering.FunctionClass.Schedule import doClustering
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.BusinessLogic.ClusterBL import *
import json
import pandas as pd

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

def experiment():
    # kmeans
    choice1 = {
        'relevant_data': ['Problem Widget Screenshots', 'Problem Widget', 'Replay Stpes'],
        'algorithm_chosen': 'KMeans',
        'parameters': {
            'n_clusters': 48,
            'init': 'k-means++',
            'n_init': 10,
            'max_iter': 300,
            'tol': 0.0001,
            'precompute_distances': 'auto',
            'verbose': 0,
            'random_state': 'None',
            'copy_x': 'True',
            'n_jobs': 1,
            'algorithm': 'auto'
        }
    }

    # dbscan
    choice2 = {
        'relevant_data': ['Problem Widget'],
        'algorithm_chosen': 'DBSCAN',
        'parameters': {
            'eps': 0,
            'min_samples': 0,
            'metric': 'euclidean',
            'metric_params': None,
            'algorithm': 'auto',
            'leaf_size': 30,
            'p': None,
            'n_jobs': None,
            'features': [],
        }
    }

    # birch
    choice3 = {
        'relevant_data': ['Replay Steps'],
        'algorithm_chosen': 'BIRCH',
        'parameters': {
            'threshold': 0,
            'branching_factor': 0,
            'n_clusters': None,
            'compute_labels': True,
            'copy': True,
        }
    }

    # gmm
    choice4 = {
        'relevant_data': ['Replay Steps'],
        'algorithm_chosen': 'GMM',
        'parameters': {
            'n_components': 48,
            'covariance_type': 'full',
            'tol': 1e-3,
            'reg_covar': 1e-6,
            'max_iter': 100,
            'n_init': 1,
            'init_params': 'random',
            'weights_init': None,
            'means_init': None,
            'precisions_init': None,
            'random_state': None,
            'warm_start': False,
            'verbose': 0,
            'verbose_interval': 10
        }
    }

    choices = [choice1, choice2, choice3, choice4]
    input = [['Replay Steps'], ['Problem Widget'], ['Problem Widget Screenshots'],
             ['Problem Widget', 'Replay Steps'], ['Problem Widget', 'Problem Widget Screenshots'],
             ['Replay Steps', 'Problem Widget Screenshots'],
             ['Problem Widget', 'Replay Steps', 'Problem Widget Screenshots']]
    choice = choices[3]
    for j in range(0, len(input)):
        choice['relevant_data'] = input[j]
        good_features, bad_features = featureTransformation(4, Reduction.AVERAGE)
        tree = algorithmExecution(good_features, [choice])
        fileProduction(str(3) + '_' + str(j), 4, tree, [choice], Reduction.AVERAGE, good_features, bad_features,
                       '20200416222410', '')
        print('*******', 3, j, '*******')

def getReportsAccordingID():
    file=open('E:\\TRS\\TRS_backend\\ReportClustering\\files.txt','r')
    content=json.loads(file.read())
    index=[]
    bug_id=[]
    bug_category=[]
    severity=[]
    recurrent=[]
    bug_create_time=[]
    bug_page=[]
    description=[]
    image_url=[]
    app_name=[]
    device=[]
    for i in range(0,len(content)):
        index.append(i)
        report=get_report(content[i])
        bug_id.append(report['bug_id'])
        bug_category.append(report['bug_category'])
        severity.append(report['severity'])
        recurrent.append(report['recurrent'])
        bug_create_time.append(report['bug_create_time'])
        bug_page.append(report['bug_page'])
        description.append(report['description'])
        image_url.append(report['img_url'])
        app_name.append(report['app_name'])
        device.append(report['device'])

    data=pd.DataFrame()
    data.insert(0,'value',index)
    data.insert(1,'bug_id',bug_id)
    data.insert(2,'bug_category',bug_category)
    data.insert(3,'severity',severity)
    data.insert(4,'recurrent',recurrent)
    data.insert(5,'bug_create_time',bug_create_time)
    data.insert(6,'bug_page',bug_page)
    data.insert(7,'description',description)
    data.insert(8,'image_url',image_url)
    data.insert(9,'app_name',app_name)
    data.insert(10,'device',device)
    data.to_csv('E:\\TRS\\TRS_backend\\ReportClustering\\new_data.csv',encoding='utf8')


getReportsAccordingID()


# #print(open('\TRS\TRS_backend\ReportClustering\DataFile\ChoiceFile\choice_1_20200416222410.txt','r').read())

# good_features,bad_features=featureTransformation(4, Reduction.AVERAGE)
# tree=algorithmExecution(good_features,[choice4])
# fileProduction('dbscan_replay',4,tree,[choice4],Reduction.AVERAGE,good_features,bad_features,'20200416222410','')

