from TRS_backend.ReportClustering.Dao import ReportDao
from TRS_backend.ReportClustering.Dao import FeatureDao
from TRS_backend.FeatureExtraction.FeatureVectorization import text_feature_vectorization as TextFeatureVectorization
from TRS_backend.FeatureExtraction.FeatureVectorization import image_feature_vectorization as ImageFeatureVectorization
from TRS_backend.ReportClustering.Bean.ReportVector import *

# 通过数据库将特征信息提取出来返回
def getFeaturesContent(setid):

    #1 先通过工作号将该次操作所有的原始报告拿出来
    reports=FeatureDao.getFeatureResults(setid)

    #2 针对每个原始报告，获取其提取的特征数据
    good_features=[]
    bad_features=[]
    for i in range(0,len(reports)):
        if reports[i].is_widget_available:
            good_features.append(reports[i])
        else:
            bad_features.append(reports[i])

    #3 返回获取的特征数据
    return good_features,bad_features

# 将提取出来的特征信息通过保存的模型进行内容到向量的转化
def getFeaturesVector(features):
    text_feature_list = []
    image_feature_list = []
    for feature in features:
        text_feature = {'procedures_list': feature.procedure, 'problem_widget': feature.widget,
                        'problems_list': feature.problem}
        img_feature = {'is_widget_available': feature.is_widget_available, 'problem_widget': feature.widget_path,
                       'other_widget': feature.other_widget}
        text_feature_list.append(text_feature)
        image_feature_list.append(img_feature)
    text_vector_list=TextFeatureVectorization.text_feature_to_vector(text_feature_list)
    image_vector_list=ImageFeatureVectorization.image_feature_to_vector(image_feature_list)
    data=[]
    for i in range(0,len(features)):
        feature=ReportVector(features[i],text_vector_list[i],image_vector_list[i])
        data.append(feature)
    return data