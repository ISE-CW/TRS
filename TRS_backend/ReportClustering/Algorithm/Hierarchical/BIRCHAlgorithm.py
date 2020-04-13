from sklearn.cluster import Birch
X=[]
threshold=0.5
branching_factor=50
n_clusters=3
compute_labels=True
copy=True
features=[]
db2=Birch(threshold=0.5, branching_factor=50, n_clusters=3,
                 compute_labels=True, copy=True).fit(X)
