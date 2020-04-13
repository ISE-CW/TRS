import pandas as pd

import TRS_backend.FeatureExtraction.ImageFeatureExtraction.image_feature_extraction as ImageFeatureExtraction
import TRS_backend.FeatureExtraction.TextFeatureExtraction.text_feature_extraction as TextFeatureExtraction
import TRS_backend.data as data


def get_report_feature(report_set_id):
    if data.is_feature_result_exist(report_set_id):
        return data.find_feature_result(report_set_id)
    reports = data.find_report(report_set_id)
    descriptions = []
    images = []
    for report in reports:
        descriptions.append(report['description'])
        images.append(report['img_url'])
    report_features = []
    text_feature_list = TextFeatureExtraction.text_feature_extraction(descriptions)
    widget_information_list = []
    for text_feature in text_feature_list:
        widget_information_list.append(text_feature['problem_widget'])
    image_feature_list = ImageFeatureExtraction.image_feature_extraction(images, widget_information_list)
    print('text_feature:{}'.format(text_feature_list))
    print('image_feature_list:{}'.format(image_feature_list))
    for i in range(len(reports)):
        text_feature = text_feature_list[i]
        img_feature = image_feature_list[i]
        feature = {'procedure': text_feature['procedures_list'], 'widget': text_feature['problem_widget'],
                   'problem': text_feature['problems_list'],
                   'is_widget_available': img_feature['is_widget_available'],
                   'widget_path': img_feature['valid_widget_path'], 'other_widget': img_feature['other_widget'],
                   'andrimg_path': img_feature['andrimg_path']}
        report_features.append(feature)
        data.insert_feature_result(reports[i]['rid'], text_feature['procedures_list'], text_feature['problems_list'],
                                   text_feature['problem_widget'], img_feature['is_widget_available'],
                                   img_feature['valid_widget_path'], img_feature['other_widget'],
                                   img_feature['andrimg_path'])
    return report_features


# report_features = get_report_feature('./sample.csv')
# file=open("workid_feature.txt","w")
# bug_id=0
# for feature in report_features:
#     bug_id=bug_id+1
#     file.write("bug_id: "+str(bug_id)+"\n")
#     file.write("is_widget_available: "+str(feature['is_widget_available'])+"\n")
#     file.write("andrimg_path: "+str(feature['andrimg_path'])+"\n")
#
#     procedure=feature['procedure_vector']
#     file.write("procedure_vector: "+str(len(procedure))+"\n")
#     for item in procedure:
#         file.write("[")
#         for i in range(0,len(item)):
#             file.write(str(item[i])+",")
#         file.write("]\n")
#
#     widget=feature['widget_vector']
#     file.write("widget_vector: "+str(len(widget))+"\n")
#     file.write("[")
#     for i in range(0, len(widget)):
#         file.write(str(widget[i]) + ",")
#     file.write("]\n")
#
#     problem=feature['problem_vector']
#     file.write("problem_vector: "+str(len(problem))+"\n")
#     for item in problem:
#         file.write("[")
#         for i in range(0, len(item)):
#             file.write(str(item[i]) + ",")
#         file.write("]\n")
#
#     image=feature['image_vector']
#     file.write("image_vector: " + str(len(image))+"\n")
#     for item in image:
#         file.write("[")
#         for i in range(0, len(item)):
#             file.write(str(item[i]) + ",")
#         file.write("]\n")
# file.close()

report_features = get_report_feature(2)
for feature in report_features:
    print(
        'procedure:{},widget:{},problem:{},is_widget_available:{},widget_path:{},other_widget:{},andrimg_path:{}'.format(
            feature['procedure'], feature['widget'], feature['problem'],
            feature['is_widget_available'], feature['widget_path'], feature['other_widget'], feature['andrimg_path']))
