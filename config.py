'''This module handles the creation of necessary directories for the BarcodeScanSplit project.'''

import os

def make_dir(dir_path: str):
    '''Create a directory if it does not exist'''
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

path: str = os.path.dirname(__file__)

# Directories

# Log directory
LOG_DIR: str = "logs"
log_path: str = os.path.join(path, LOG_DIR)
make_dir(log_path)

# Document directory
DOC_DIR: str = "docs"
doc_path: str = os.path.join(path, DOC_DIR)
make_dir(doc_path)

# Temp directory
TEMP_DIR: str = "temp"
temp_path: str = os.path.join(path, TEMP_DIR)
make_dir(temp_path)

# Image directory
IMG_DIR: str = "images"
img_path: str = os.path.join(path, IMG_DIR)
make_dir(img_path)

# Output directory
OUTPUT_DIR: str = "out"
output_path: str = os.path.join(path, OUTPUT_DIR)
make_dir(output_path)

# Backup directory
BACKUP_DIR: str = "backup"
backup_path: str = os.path.join(path, BACKUP_DIR)
make_dir(backup_path)
