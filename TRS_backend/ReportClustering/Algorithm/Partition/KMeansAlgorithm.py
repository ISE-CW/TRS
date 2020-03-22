from sklearn.cluster import KMeans
import math

class KMeansAlgorithm:
    n_clusters=1
    init='k-means++'
    n_init=10
    max_iter=300
    tol=0.0001
    precompute_distances='auto'
    verbose=0
    random_state=None
    copy_x=True
    n_jobs=1
    algorithm='auto'
    features=[]
    def __init__(self,parameters,features):
        self.n_clusters=parameters['n_clusters']
        self.init=parameters['init']
        self.max_iter=parameters['max_iter']
        self.tol=parameters['tol']
        self.precompute_distances=parameters['precompute_distances']
        self.verbose=parameters['verbose']
        self.random_state=parameters['random_state']
        self.copy_x=parameters['copy_x']
        self.n_jobs=parameters['n_jobs']
        self.algorithm=parameters['algorithm']
        self.features=features

    def go(self):
        if self.n_clusters<=0:
            # 1.根据不同的K值获得SSE和聚类数组
            SSE=[]
            clusters=[]
            for i in range(1,len(self.features)+1):
                result=self.executeKMeans(i)
                SSE.append(result['SSE']) #不同k值的SSE数组
                clusters.append(result['clusters']) #不同k值的聚类结果数组
                # 如果没有把分类分到最细的程度下SSE已经为0，则为最佳状态
                if i<len(self.features) and SSE[i-1]==0:
                    return result['clusters']

            # 2.找出曲率变化最快的点
            theta=[]
            for i in range(1,len(SSE)-1):
                k1=(SSE[i]-SSE[i-1])*1.0
                k2=(SSE[i+1]-SSE[i])*1.0
                angle1=math.atan(k1)
                angle2=math.atan(k2)
                theta.append(180-angle2+angle1)
            quickest_point_index=theta.index(min(theta))
            return clusters[quickest_point_index+1]

        else:
            result=self.executeKMeans(self.n_clusters)
            return result['clusters']

    # 用一个k值执行一次KMeans算法
    def executeKMeans(self,clusters_num):
        # 1.根据参数训练模型
        km=KMeans(n_clusters=clusters_num, init=self.init, n_init=self.n_init, max_iter=self.max_iter,
                        tol=self.tol, precompute_distances=self.precompute_distances, verbose=self.verbose,
                        random_state=self.random_state, copy_x=self.copy_x, n_jobs=self.n_jobs,
                        algorithm=self.algorithm)
        km.fit(self.features)

        # 2.获取分类标签
        labels=km.labels_

        # 3.创建聚类数组，并将结果feature的索引写入其中
        clusters=[]
        for i in range(0,clusters_num):
            clusters.append([])

        for i in range(0,len(labels)):
            clusters[labels[i]].append(i)

        # 4.计算SSE值
        SSE=km.inertia_

        return {'clusters':clusters,'SSE':SSE}


