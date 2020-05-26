from TRS_backend.ReportClustering.Util.Enumeration import *
def changeEnumToChinese(enum):
    if enum==InputData.PROCEDURE_VECTOR:
        return 'Replay Steps'
    elif enum==InputData.PROBLEM_VECTOR:
        return 'Bug Type'
    elif enum==InputData.WIDGET_VECTOR:
        return 'Problem Widget'
    elif enum==InputData.PROBLEM_WIDGET_VECTOR:
        return 'Problem Widget Screenshots'
    elif enum==InputData.OTHER_WIDGET_VECTOR:
        return 'Other Widget Screenshots'
    elif enum==ClusteringAlgorithm.KMEANS:
        return 'KMeans'
    elif enum==ClusteringAlgorithm.GMM:
        return 'GMM'
    elif enum==ClusteringAlgorithm.BIRCH:
        return 'BIRCH'
    elif enum==ClusteringAlgorithm.DBSCAN:
        return 'DBSCAN'
    elif enum==FileFormat.WORD:
        return 'doc'
    elif enum==FileFormat.PDF:
        return 'pdf'
    elif enum==FileFormat.MARKDOWN:
        return 'markdown'
    elif enum==Reduction.AVERAGE:
        return 'Average Method'
    elif enum==Reduction.DIMENSIONAL:
        return 'PCA Method'
    elif enum==State.FINISH:
        return 'State.FINISH'
    elif enum==State.RUNNING:
        return 'State.RUNNING'

def changeChineseToEnum(chinese):
    if chinese=='Replay Steps':
        return InputData.PROCEDURE_VECTOR
    elif chinese=='Bug Type':
        return InputData.PROBLEM_VECTOR
    elif chinese=='Problem Widget':
        return InputData.WIDGET_VECTOR
    elif chinese=='Problem Widget Screenshots':
        return InputData.PROBLEM_WIDGET_VECTOR
    elif chinese=='Other Widget Screenshots':
        return InputData.OTHER_WIDGET_VECTOR
    elif chinese=='KMeans':
        return ClusteringAlgorithm.KMEANS
    elif chinese=='GMM':
        return ClusteringAlgorithm.GMM
    elif chinese=='BIRCH':
        return ClusteringAlgorithm.BIRCH
    elif chinese=='DBSCAN':
        return ClusteringAlgorithm.DBSCAN
    elif chinese=='doc':
        return FileFormat.WORD
    elif chinese=='pdf':
        return FileFormat.PDF
    elif chinese=='markdown':
        return FileFormat.MARKDOWN
    elif chinese=='Average Method':
        return Reduction.AVERAGE
    elif chinese=='PCA Method':
        return Reduction.DIMENSIONAL
    elif chinese=='State.FINISH':
        return State.FINISH
    elif chinese=='State.RUNNING':
        return State.RUNNING
