import cv2
import os


def get_sift_feature(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptor = sift.detectAndCompute(gray, None)
    return descriptor


def image_feature_to_vector(result_list):
    descriptor_list = []
    for result in result_list:
        other_widget_vector = []
        problem_widget_vector = None
        is_widget_available = result['is_widget_available']
        problem_widget_path = result['problem_widget']
        other_widget_path = result['other_widget']
        if is_widget_available:
            problem_widget_vector = get_sift_feature(problem_widget_path)
            for other_widget in other_widget_path:
                other_widget_vector.append(get_sift_feature(other_widget))
        res = {'is_widget_available': is_widget_available, 'problem_widget_vector': problem_widget_vector,
               'other_widget_vector': other_widget_vector}
        descriptor_list.append(res)
    print('-----image feature to vector success-----')
    return descriptor_list