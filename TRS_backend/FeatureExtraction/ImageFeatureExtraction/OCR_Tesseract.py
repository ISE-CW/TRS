import PIL.Image
import pytesseract
import sys

imgPath = sys.argv[1]
lang = sys.argv[2]
res = pytesseract.image_to_string(PIL.Image.open(imgPath), lang)

NONE_SPACE_LANG = ['chi_sim', 'chi_tra', 'jpn']
if lang in NONE_SPACE_LANG:
    print(res.replace(' ', ''))
else:
    print(res)
