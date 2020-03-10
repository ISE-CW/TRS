import pandas as pd

import TRS_backend.FeatureExtraction.ImageFeatureExtraction.image_feature_extraction as ImageFeatureExtraction
import TRS_backend.FeatureExtraction.TextFeatureExtraction.text_feature_extraction as TextFeatureExtraction
import TRS_backend.FeatureExtraction.FeatureVectorization.image_feature_vectorization as ImageFeatureVectorization
import TRS_backend.FeatureExtraction.FeatureVectorization.text_feature_vectorization as TextFeatureVectoriztion


def get_report_feature(reports_path):
    reports = pd.read_csv(reports_path)
    descriptions = reports['description']
    images = reports['img_url']
    report_features = []
    text_feature_list = TextFeatureExtraction.text_feature_extraction(descriptions)
    widget_information_list = []
    for text_feature in text_feature_list:
        widget_information_list.append(text_feature['problem_widget'])
    image_feature_list = ImageFeatureExtraction.image_feature_extraction(images, widget_information_list)
    text_vector_list = TextFeatureVectoriztion.text_feature_to_vector(text_feature_list)
    widget_path_list = []
    for image_feature in image_feature_list:
        widget_path_list.append(image_feature['valid_widget_path'])
    image_vector_list = ImageFeatureVectorization.image_feature_to_vector(widget_path_list)
    for i in range(len(descriptions)):
        text_vector = text_vector_list[i]
        image_feature = image_feature_list[i]
        feature = {'procedure_vector': text_vector['procedure_vector'], 'widget_vector': text_vector['widget_vector'],
                   'problem_vector': text_vector['problem_vector'],
                   'is_widget_available': image_feature['is_widget_available'],
                   'image_vector': image_vector_list[i], 'andrimg_path': image_feature['andrimg_path']}
        report_features.append(feature)
    return report_features


report_features = get_report_feature('./sample.csv')
for feature in report_features:
    print(
        'procedure_vector:{},widget_vector:{},problem_vector:{},is_widget_available:{},image_vector:{},andrimg_path:{}'.format(
            feature['procedure_vector'], feature['widget_vector'], feature['problem_vector'],
            feature['is_widget_available'], feature['image_vector'], feature['andrimg_path']))
