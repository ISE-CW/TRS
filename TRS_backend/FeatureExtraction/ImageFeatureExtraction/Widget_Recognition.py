#!/usr/bin/env python
# coding=utf-8

# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen, based on code from Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.lib.utils.nms_wrapper import nms
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.lib.utils.test import im_detect
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.lib.nets.vgg16 import vgg16
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.lib.utils.timer import Timer
import gensim
import jieba
import math
from TRS_backend.FeatureExtraction.ImageFeatureExtraction.OCR_Baidu import get_baidu_ocr_res
import shutil
import sys

COLOR = ['red', 'white', 'blue', 'black', 'gray', 'orange', 'green', 'pink', 'cyan', 'blue', 'black', 'gray', 'orange',
         'green', 'pink', 'cyan']
FACE = ['red', 'white', 'blue', 'black', 'gray', 'orange', 'green', 'pink', 'cyan', 'blue', 'black', 'gray', 'orange',
        'green', 'pink', 'cyan']

CLASSES = ('__background__',  # always index 0
           'TextView', 'CheckBox', 'ImgButton', 'Button', 'EditText', 'ImgView', 'CheckedTextView', 'ProgressBar',
           'RadioButton', 'RatingBar', 'SeekBar', 'Switch', 'ProgressBarHorizontal')

NETS = {'vgg16': ('vgg16_faster_rcnn_iter_40000.ckpt',), 'res101': ('res101_faster_rcnn_iter_110000.ckpt',)}
DATASETS = {'pascal_voc': ('voc_2007_trainval',)}
MAX_SCORE = [0.0]
CLASS_NAME = ""
CHECK = 0
INDS = {'TextView': 0, 'CheckBox': 1, 'ImgButton': 2, 'Button': 3, 'EditText': 4, 'ImgView': 5, 'CheckedTextView': 6,
        'ProgressBar': 7,
        'RadioButton': 8, 'RatingBar': 9, 'SeekBar': 10, 'Switch': 11}
RES = np.zeros((12, 12))


def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    global CHECK
    global CLASS_NAME
    global INDS
    global RES
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    bbox = dets[inds[0], :4]
    score = dets[inds[0], -1]
    if len(inds) > 1:
        score = -1
        for i in inds:
            temp = dets[i, -1]
            if (temp > score):
                score = temp
                bbox = dets[i, :4]
    if score <= MAX_SCORE[0]:
        return
    else:
        CHECK = 1
        MAX_SCORE[0] = score
        CLASS_NAME = class_name
        # im = im[:, :, (2, 1, 0)]
        # fig, ax = plt.subplots()
        # ax.imshow(im, aspect='equal')
        # ax.add_patch(
        #     plt.Rectangle((bbox[0], bbox[1]),
        #                   bbox[2] - bbox[0],
        #                   bbox[3] - bbox[1], fill=False,
        #                   edgecolor='red', linewidth=3.5)
        # )
        # ax.text(bbox[0], bbox[1] - 2,
        #         '{:s} {:.3f}'.format(class_name, score),
        #         bbox=dict(facecolor='blue', alpha=0.5),
        #         fontsize=10, color='white')
        # ax.set_title(('{} detections with '
        #               'p({} | box) >= {:.1f}').format(class_name, class_name,
        #                                               thresh),
        #              fontsize=10)
        # plt.axis('off')
        # plt.tight_layout()
        # plt.draw()


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""
    # Load the demo image
    global CLASS_NAME
    global CHECK
    CHECK = 0
    # 读取的截图所在的位置
    # im_file = Cnn_path + "data/VOCdevkit2007/VOC2007/JPEGImages/" + image_name
    curpath = os.path.dirname(os.path.realpath(__file__))
    im_file = curpath + "\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\" + image_name
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print('Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]))

    # Visualize detections for each class
    # score 阈值，最后画出候选框时需要，>thresh才会被画出
    CONF_THRESH = 0.5
    # 非极大值抑制的阈值，剔除重复候选框
    NMS_THRESH = 0.3
    # 利用enumerate函数，获得CLASSES中 类别的下标cls_ind和类别名cls
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1  # because we skipped background
        # 取出bbox ,score
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        # 将bbox,score 一起存入dets
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        # 进行非极大值抑制，得到抑制后的 dets
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        # 画框
        vis_detections(im, cls, dets, thresh=CONF_THRESH)
    if CHECK == 0:
        CLASS_NAME = "None"
        # im = im[:, :, (2, 1, 0)]
        # fig, ax = plt.subplots()
        # ax.imshow(im, aspect='equal')
        # ax.set_title("None",fontsize=10)
        # plt.axis('off')
        # plt.tight_layout()
        # plt.draw()
    # RES[INDS.__getitem__(image_name.split("_")[0])][INDS.__getitem__(CLASS_NAME)]+=1
    # plt.savefig("./output/"+CLASS_NAME+"_" + image_name)
    # plt.savefig("./output/" + image_name)
    MAX_SCORE[0] = 0.0


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16 res101]',
                        choices=NETS.keys(), default='vgg16')
    parser.add_argument('--dataset', dest='dataset', help='Trained dataset [pascal_voc pascal_voc_0712]',
                        choices=DATASETS.keys(), default='pascal_voc')

    args = parser.parse_args()

    return args


def sentence_similarity(model, s1, s2):
    size = model.layer1_size

    def sentence_vector(s):
        words = []
        try:
            words = [x for x in jieba.cut(s, cut_all=True) if x != '']
        except:
            return np.zeros(size)
        v = np.zeros(size)
        length = len(words)
        for word in words:
            try:
                v += model[word]
            except:
                length -= 1
        if length != 0:
            v /= length
        return v

    def cos_dist(a, b):
        if len(a) != len(b):
            return None
        part_up = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for a1, b1 in zip(a, b):
            part_up += a1 * b1
            a_sq += a1 ** 2
            b_sq += b1 ** 2
        part_down = math.sqrt(a_sq * b_sq)
        if part_down == 0.0:
            return None
        else:
            return part_up / part_down

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    dis = cos_dist(v1, v2)
    return dis


def widget_recognition(img_name_list, widget_information_list):
    curpath = os.path.dirname(os.path.realpath(__file__))

    args = parse_args()

    # model path
    demonet = args.demo_net
    dataset = args.dataset
    tfmodel = os.path.join(curpath + '\\output', demonet, DATASETS[dataset][0], 'default', NETS[demonet][0])
    if not os.path.isfile(tfmodel + '.meta'):
        print(tfmodel)
        raise IOError(('{:s} not found.\nDid you download the proper networks from '
                       'our server and place them properly?').format(tfmodel + '.meta'))

    # set config
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth = True

    # init session
    sess = tf.Session(config=tfconfig)
    # load network
    if demonet == 'vgg16':
        net = vgg16(batch_size=1)
    # elif demonet == 'res101':
    # net = resnetv1(batch_size=1, num_layers=101)
    else:
        raise NotImplementedError

    n_classes = len(CLASSES)
    # create the structure of the net having a certain shape (which depends on the number of classes) 
    net.create_architecture(sess, "TEST", n_classes,
                            tag='default', anchor_scales=[8, 16, 32])
    saver = tf.train.Saver()
    saver.restore(sess, tfmodel)
    print('Loaded network {:s}'.format(tfmodel))

    father_dir = os.path.dirname(curpath)
    word2vec_model = gensim.models.Word2Vec.load(
        father_dir + '\\word2vec_model\\bugdata_format_model_100')  # 调用先前的word2vec模型

    filepath = curpath + "\\data\\VOCdevkit2007\\VOC2007\\coordinate\\"

    result_list = []

    for index in range(len(img_name_list)):
        img_name = img_name_list[index]
        widget_information = widget_information_list[index]
        andrimg_path = curpath + "\\res\\" + img_name.split('.')[0] + "_res.png"
        image_path = curpath + "\\images\\" + img_name
        count = 1
        file = open(filepath + img_name.split('.')[0] + '.txt')
        lines = file.readlines()
        im = cv2.imread(image_path)
        im = im[:, :, (2, 1, 0)]
        fig, ax = plt.subplots(figsize=(11, 20))
        is_widget_available = False
        vaild_widget_path = ''
        other_widget = []
        for line in lines:
            filename = line.strip('\n').split(":")[0]
            bbox = line.strip('\n').split(":")[1].split(" ")
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Demo for {}'.format(filename + ".jpg"))
            demo(sess, net, img_name.split('.')[0] + '\\' + filename + ".jpg")
            number = filename
            widget_file_path = curpath + "\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\" + img_name.split('.')[
                0] + '\\' + filename + ".jpg"
            print('file_path : {}'.format(widget_file_path))
            ocr_res = get_baidu_ocr_res(widget_file_path)
            print('ocr result: {}'.format(' '.join(ocr_res)))
            if CLASS_NAME != "None":
                if is_widget_available:
                    ax.imshow(im, aspect='equal')
                    ax.add_patch(
                        plt.Rectangle((float(bbox[0]), float(bbox[1])),
                                      float(bbox[2]) - float(bbox[0]),
                                      float(bbox[3]) - float(bbox[1]), fill=False,
                                      edgecolor='blue', linewidth=2)
                    )
                    ax.text(float(bbox[0]), float(bbox[1]) - 2,
                            '{:s}'.format(str(number) + ':' + "None"),
                            bbox=dict(facecolor='blue', alpha=0.5),
                            fontsize=8, color='white')
                    other_widget.append(widget_file_path)
                else:
                    match_res = False
                    for ocr_txt in ocr_res:
                        similarity = sentence_similarity(word2vec_model, ocr_txt, widget_information)
                        if (similarity and similarity >= 0.98) or (
                                CLASS_NAME == 'EditText' and (
                                widget_information == '搜索栏' or widget_information == '输入框')):
                            match_res = True
                            break
                    if match_res:
                        ax.imshow(im, aspect='equal')
                        ax.add_patch(
                            plt.Rectangle((float(bbox[0]), float(bbox[1])),
                                          float(bbox[2]) - float(bbox[0]),
                                          float(bbox[3]) - float(bbox[1]), fill=False,
                                          edgecolor='red', linewidth=2)
                        )
                        ax.text(float(bbox[0]), float(bbox[1]) - 2,
                                '{:s}'.format(CLASS_NAME),
                                bbox=dict(facecolor='red', alpha=0.5),
                                fontsize=8, color='white')
                        is_widget_available = True
                        vaild_widget_path = widget_file_path
                    else:
                        ax.imshow(im, aspect='equal')
                        ax.add_patch(
                            plt.Rectangle((float(bbox[0]), float(bbox[1])),
                                          float(bbox[2]) - float(bbox[0]),
                                          float(bbox[3]) - float(bbox[1]), fill=False,
                                          edgecolor='blue', linewidth=2)
                        )
                        ax.text(float(bbox[0]), float(bbox[1]) - 2,
                                '{:s}'.format(str(number) + ':' + "None"),
                                bbox=dict(facecolor='blue', alpha=0.5),
                                fontsize=8, color='white')
                        other_widget.append(widget_file_path)
        if is_widget_available:
            plt.axis('off')
            plt.draw()
            print(andrimg_path)
            plt.savefig(andrimg_path)
        else:
            if img_name[len(img_name) - 3:] == 'JPG' or img_name[len(img_name) - 3:] == 'jpg':
                andrimg_path = curpath + "\\res\\" + img_name.split('.')[0] + "_res" + img_name[len(img_name - 4):]
            try:
                shutil.copy(image_path, andrimg_path)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
        file.close()
        os.remove(filepath + img_name.split('.')[0] + '.txt')
        path = curpath + '\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\' + img_name.split('.')[0]
        for i in os.listdir(path):
            path_file = curpath + '\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\' + img_name.split('.')[0] + '\\' + i
            if os.path.isfile(path_file):
                if path_file != vaild_widget_path and (path_file not in other_widget):
                    os.remove(path_file)
        open(curpath + '\\data\\VOCdevkit2007\\VOC2007\\ImageSets\\Main\\test.txt', 'w').close()
        image_result = {'is_widget_available': is_widget_available, 'valid_widget_path': vaild_widget_path,
                        'other_widget': other_widget, 'andrimg_path': andrimg_path}
        result_list.append(image_result)

    return result_list
