from sklearn.cluster import Birch
from sklearn import metrics


class BIRCHAlgorithm:
    threshold = 0
    branching_factor = 0
    n_clusters = None
    compute_labels = True
    copy = True
    features = []

    def __init__(self, parameters, features):
        self.features = features
        self.threshold = parameters['threshold']
        self.branching_factor = parameters['branching_factor']
        self.n_clusters = parameters['n_clusters']
        self.compute_labels = parameters['compute_labels']
        self.copy = parameters['copy']
        self.features = features

    def go(self):
        thresholds = [0.1, 0.2, 0.3, 0, 4, 0.5, 0.6, 0.7, 0.8, 0.9]
        branching_factors = [100, 50, 20, 10]
        labels=[]
        if self.threshold == 0 and self.branching_factor == 0:
            clusters = []
            CH = []
            for t in thresholds:
                for b in branching_factors:
                    result = self.executeBirch(t, b)
                    clusters.append(result['clusters'])
                    CH.append(result['CH'])
            labels=clusters[CH.index(max(CH))]
        elif self.threshold == 0:
            clusters = []
            CH = []
            for t in thresholds:
                result = self.executeBirch(t, self.branching_factor)
                clusters.append(result['clusters'])
                CH.append(result['CH'])
            labels=clusters[CH.index(max(CH))]
        elif self.branching_factor == 0:
            clusters = []
            CH = []
            for b in branching_factors:
                result = self.executeBirch(self.threshold, b)
                clusters.append(result['clusters'])
                CH.append(result['CH'])
            labels=clusters[CH.index(max(CH))]
        else:
            labels=self.executeBirch(self.threshold, self.branching_factor)['clusters']

        cluster_num=max(labels)+1
        result=[]
        for i in range(0,cluster_num):
            result.append([])
        for i in range(0,len(labels)):
            result[labels[i]].append(i)

        return result

    def executeBirch(self, threshold, branching_factor):
        bc = Birch(threshold=threshold, branching_factor=branching_factor, n_clusters=self.n_clusters,
                   compute_labels=self.compute_labels, copy=self.copy).fit(self.features)
        labels = bc.labels_
        result = {}
        try:
            result = {
                'clusters': bc.labels_,
                'CH': metrics.calinski_harabaz_score(self.features, labels)
            }
        except:
            result = {
                'clusters': bc.labels_,
                'CH': float(1)
            }
        return result
