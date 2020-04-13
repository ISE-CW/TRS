from TRS_backend.ReportClustering.Dao import ReportDao
from TRS_backend.ReportClustering.Dao import FeatureDao

# 通过数据库将特征信息提取出来返回
def getFeaturesContent(workid):
    #1 先通过工作号将该次操作所有的原始报告拿出来
    reports=ReportDao.getOrigianlReports(workid)

    #2 针对每个原始报告，获取其提取的特征数据
    good_features=[]
    bad_features=[]
    for i in range(0,len(reports)):
        feature=FeatureDao.getReportFeature(reports[i].getReportID())
        if feature['is_widget_available']:
            good_features.append(feature)
        else:
            bad_features.append(feature)

    #3 返回获取的特征数据
    return good_features,bad_features

# 将提取出来的特征信息通过保存的模型进行内容到向量的转化
def getFeaturesVector(features):
    data=[]
    return data