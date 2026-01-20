'''
    ocr test
'''
import logging
import warnings
import cv2
import easyocr

#logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("easyocr").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

warnings.filterwarnings("ignore",
                        message=".*pin_memory.*no accelerator is found.*")

img_path: str = "test/test_szall.jpg"
prefixes = ["KSL"]

img = cv2.imread(img_path)
h, w, _ = img.shape

crop = img[0:int(h * 2 / 5), 0:w]

reader = easyocr.Reader(['en'])
results = reader.readtext(crop)

for _, text, _ in results:
    for prefix in prefixes:
        if prefix in text.strip():
            print(text)
