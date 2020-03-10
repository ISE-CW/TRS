import cv2
import os


def image_feature_to_vector(widget_path_list):
    descriptor_list = []
    for widget_path in widget_path_list:
        if widget_path == '':
            descriptor_list.append(None)
        else:
            img = cv2.imread(widget_path)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            sift = cv2.xfeatures2d.SIFT_create()
            keypoints, descriptor = sift.detectAndCompute(gray, None)
            descriptor_list.append(descriptor)
    print('-----image feature to vector success-----')
    return descriptor_list
