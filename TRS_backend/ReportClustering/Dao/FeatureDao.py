from TRS_backend import data as DATA
from TRS_backend.ReportClustering.Bean.ReportFeature import *
# 根据报告集ID获取该报告集所有的特征数据
def getFeatureResults(setid):
    features=DATA.find_feature_result(setid)
    result=[]
    for feature in features:
        temp=ReportFeature(feature)
        result.append(temp)
    return result



# 根据单份测试报告id获取单个报告的特征数据内容
def getReportFeature(reportid):
    return