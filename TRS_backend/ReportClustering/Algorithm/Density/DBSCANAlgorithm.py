from sklearn.cluster import DBSCAN
from TRS_backend.ReportClustering.Algorithm.Density.FindEpsAndMpts import findEpsandMpts
class DBSCANAlgorithm:
    eps = 0.5
    min_samples = 5
    metric = 'euclidean'
    metric_params = None
    algorithm = 'auto'
    leaf_size = 30
    p = None
    n_jobs = None
    features = []
    def __init__(self,parameters,features):
        self.eps=parameters['eps']
        self.min_samples=parameters['min_samples']
        self.metric=parameters['metric']
        self.metric_params=parameters['metric_params']
        self.algorithm=parameters['algorithm']
        self.leaf_size=parameters['leaf_size']
        self.p=parameters['p']
        self.n_jobs=parameters['n_jobs']
        self.features=features

    def go(self):
        if len(self.features)<=1:
            return [[0]]

        if self.eps==0 and self.min_samples==0:
            self.eps,self.min_samples=findEpsandMpts(self.features)

        db = DBSCAN(eps=self.eps,min_samples=self.min_samples,metric=self.metric,metric_params=self.metric_params,
                    algorithm=self.algorithm,leaf_size=self.leaf_size,p=self.p,n_jobs=self.n_jobs).fit(self.features)

        labels=db.labels_
        core=db.core_sample_indices_
        result=[]
        for i in range(0,len(core)):
            result.append([])
        for i in range(0,len(labels)):
            if labels[i]==-1:
                result.append([i])
            else:
                result[labels[i]].append(i)

        return result







