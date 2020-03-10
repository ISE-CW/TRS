import os
import urllib.request
import time
from urllib.parse import quote
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.Canny_detection import canny_detection
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.Widget_Recognition import widget_recognition

def download_img(image_url):
    timestamp = str(int(time.time()))
    curpath = os.path.dirname(os.path.realpath(__file__))
    file_path = curpath + '\\images\\' + timestamp + image_url[len(image_url)-4:]
    try:
        urllib.request.urlretrieve(quote(image_url, safe='/:?='), filename=file_path)  # 利用urllib.request.urltrieve方法下载图片
        return timestamp + os.path.splitext(image_url)[1]
    except IOError as e:
        print(1, e)
    except Exception as e:
        print(2, e)

def image_feature_extraction(image_url_list,widget_information_list):
    image_name_list = []
    for image_url in image_url_list:
        img_name = download_img(image_url)
        image_name_list.append(img_name)
        canny_detection(img_name)
    result_list = widget_recognition(image_name_list,widget_information_list)
    return result_list

