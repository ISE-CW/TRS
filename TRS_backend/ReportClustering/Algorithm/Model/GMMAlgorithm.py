from sklearn.mixture import GaussianMixture
from TRS_backend.ReportClustering.Algorithm.Partition.KMeansAlgorithm import *
class GMMAlgorithm:
    n_components = 0
    covariance_type = 'full'
    tol = 1e-3
    reg_covar = 1e-6
    max_iter = 100
    n_init =1
    init_params = 'kmeans'
    weights_init = None
    means_init = None
    precisions_init = None
    random_state = None
    warm_start = False
    verbose = 0
    verbose_interval = 10
    features=[]
    def __init__(self,parameters,features):
        self.n_components=parameters['n_components']
        self.covariance_type=parameters['covariance_type']
        self.tol=parameters['tol']
        self.reg_covar=parameters['reg_covar']
        self.max_iter=parameters['max_iter']
        self.n_init=parameters['n_init']
        self.init_params=parameters['init_params']
        self.weights_init=parameters['weights_init']
        self.means_init=parameters['means_init']
        self.precisions_init=parameters['precisions_init']
        self.random_state=parameters['random_state']
        self.warm_start=parameters['warm_start']
        self.verbose=parameters['verbose']
        self.verbose_interval=parameters['verbose_interval']
        self.features=features

    def go(self):
        if self.n_components<=0:
            self.findNComponents()
        gmm = GaussianMixture(n_components=self.n_components,covariance_type=self.covariance_type,
                              tol=self.tol,reg_covar=self.reg_covar,max_iter=self.max_iter,n_init=self.n_init,
                              init_params=self.init_params,weights_init=self.weights_init,means_init=self.means_init,
                              precisions_init=self.precisions_init,random_state=self.random_state,
                              warm_start=self.warm_start,verbose=self.verbose,
                              verbose_interval=self.verbose_interval).fit(self.features)
        labels = gmm.predict(self.features)
        cluster_num=max(labels)+1
        result=[]
        for i in range(0,cluster_num):
            result.append([])
        for i in range(0,len(labels)):
            result[labels[i]].append(i)
        return result

    def findNComponents(self):
        # 先通过kmeans算法确定一下n_components的数量
        km = KMeansAlgorithm(
            {
                'n_clusters': 0,
                'init': 'k-means++',
                'n_init': 10,
                'max_iter': 300,
                'tol': 0.0001,
                'precompute_distances': 'auto',
                'verbose': 0,
                'random_state': None,
                'copy_x': True,
                'n_jobs': 1,
                'algorithm': 'auto'
            },
            self.features
        )
        clusters=km.go()
        self.n_components = len(clusters)

