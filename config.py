'''config file'''

import os

def make_dir(dir_path: str):
    '''Create a directory if it does not exist'''
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

path: str = os.path.dirname(__file__)

LOG_DIR: str = "logs"
log_path: str = os.path.join(path, LOG_DIR)
make_dir(log_path)

DOC_DIR: str = "docs"
doc_path: str = os.path.join(path, DOC_DIR)
make_dir(doc_path)

TEMP_DIR: str = "temp"
temp_path: str = os.path.join(path, TEMP_DIR)
make_dir(temp_path)

IMG_DIR: str = "images"
img_path: str = os.path.join(path, IMG_DIR)
make_dir(img_path)

COPY_DIR: str = "out"
copy_path: str = os.path.join(path, COPY_DIR)
make_dir(copy_path)
