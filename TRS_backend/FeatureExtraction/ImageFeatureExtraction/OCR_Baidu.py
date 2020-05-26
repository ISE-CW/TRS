import sys

from aip import AipOcr

def get_baidu_ocr_res(path):
    img = open(path, 'rb').read()
    options = {'language-type': "CNH_ENG"}

    client = AipOcr('17039863', '81GdpEUTYZn6KzAUt3c7FgA7', 'TybpGKBqQHAoU9ESFFp30P9vOStv4fue')
    res = client.basicAccurate(img, options)
    if 'words_result' in res:
        txt = [r['words'] for r in res['words_result']]
    else:
        res = client.basicGeneral(img, options)
        if 'words_result' in res:
            txt = [r['words'] for r in res['words_result']]
        else:
            txt = []
    return txt
#
# for i in range(257*50):
#     print(get_baidu_ocr_res("E:\\TRS\\TRS_backend\\FeatureExtraction\\ImageFeatureExtraction\\data\\VOCdevkit2007\\VOC2007\\JPEGImages\\1590271922\\3.jpg"))