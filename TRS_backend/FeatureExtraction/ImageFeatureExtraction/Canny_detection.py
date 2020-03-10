# noinspection PyInterpreter
import cv2
import numpy as np
import os
import sys

# Reference: https://blog.csdn.net/liqiancao/article/details/55670749
# Reference: https://blog.csdn.net/HuangZhang_123/article/details/80746847
# https://blog.csdn.net/poem_qianmo/article/details/23710721
# https://blog.csdn.net/qq_40962368/article/details/80444144

def canny_detection(filename):
    # path = sys.argv[1]
    # web_path = sys.argv[2]
    # dir_path = web_path + "python/"
    curpath = os.path.dirname(os.path.realpath(__file__))
    path = curpath + "\\images\\"+filename
    # dir_path="E:/study for university/实验室工作/参考项目/iCTBRG/back-end/src/main/webapp/python/"
    myimg_name = filename
    img = open(path, 'rb').read()
    i_name = path[0:len(path) - 4]
    # 在这里输入完整图片的绝对地址
    i_image = i_name + '.jpg'
    i_text = i_name + '.txt'
    image = cv2.imread(path)
    sp = image.shape
    # height of image
    max_y = sp[0]
    # width of image
    max_x = sp[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("p1.png", gray)

    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.convertScaleAbs(cv2.subtract(gradX, gradY))
    # cv2.imwrite("p2.png", gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    # cv2.imwrite("p3.png", thresh)

    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))
    # cv2.imwrite("p4.png", closed)
    # perform a series of erosion and dilation
    closed = cv2.dilate(cv2.erode(closed, None, iterations=4), None, iterations=4)
    # cv2.imwrite("p5.png", closed)

    # (__, contour, _) = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (_,contour, _) = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = 1

    os.mkdir(curpath + '\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\' + myimg_name.split('.')[0]) #创建用于存放控件截图的文件夹

    for c in sorted(contour, key=cv2.contourArea, reverse=True):
        # 这边的c是边框的坐标，考虑从这边入手截取控件坐标出来
        # compute the rotated bounding box of the largest contour
        box = np.int0(cv2.boxPoints(cv2.minAreaRect(c)))
        # cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = max(0, min(Xs) - 10)
        x2 = min(max_x, max(Xs) + 10)
        y1 = max(0, min(Ys) - 10)
        y2 = min(max_y, max(Ys) + 10)
        height = y2 - y1
        width = x2 - x1
        red = (0, 0, 255)
        # 测试图片的名称保存在test.txt里，但是实际上一次只有一张图片需要测试
        f = open(
            curpath + '\\data\\VOCdevkit2007\\VOC2007\\ImageSets\\Main\\test.txt',
            'a')
        co = count
        f.write(str(co) + '\n')
        # 位置信息存储 顺序为x1 y1 x2 y2
        f1 = open(curpath + '\\data\\VOCdevkit2007\\VOC2007\\coordinate\\' +
                  myimg_name.split('.')[0] + '.txt', 'a')
        location = str(count) + ':' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(
            y2) + '\n'
        f1.write(location)
        # cv2.rectangle(image, (x1, y1), (x2, y2), red, 2)
        # cv2.imwrite(i_image,image)
        # 这里需要修改为训练图片所在的文件夹
        image2 = cv2.imread(path)
        crop = image2[y1:y2, x1:x2]
        # 前面放训练图片所在位置
        # 向JPEGImages_CannyTest文件夹中写入截图
        # cv2.imwrite(
        #     dir_path+'Faster-RCNN-TensorFlow-Python3/data/VOCdevkit2007/VOC2007/JPEGImages/'
        #     + str(count) + '.jpg', crop)
        cv2.imwrite(curpath + '\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\' + myimg_name.split('.')[0] + '\\' + str(count) + ".jpg", crop)
        print(curpath + '\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\'
              + myimg_name.split('.')[0] + '\\' + str(count) + '.jpg')
        count = count + 1