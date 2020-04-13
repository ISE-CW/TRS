from sklearn.cluster import DBSCAN
X=[]
eps=0.5
min_samples=5
metric='euclidean'
metric_params=None
algorithm='auto'
leaf_size=30
p=None
n_jobs=None
features=[]
db = DBSCAN(eps=0.3, min_samples=10).fit(X)

