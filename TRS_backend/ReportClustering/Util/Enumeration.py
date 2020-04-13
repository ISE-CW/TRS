from enum import Enum

class InputData(Enum):
    PROCEDURE_VECTOR=1
    WIDGET_VECTOR=2
    PROBLEM_VECTOR=3
    IMAGE_VECTOR=4

class ClusteringAlgorithm(Enum):
    KMEANS=1
    GMM=2
    BIRCH=3
    DBSCAN=4

class FileFormat(Enum):
    MARKDOWN=1
    PDF=2
    WORD=3

