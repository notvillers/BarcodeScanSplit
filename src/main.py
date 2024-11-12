'''main module'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import log_path, doc_path, temp_path, img_path, output_path, backup_path

def run() -> None:
    '''Main function'''
    PdfManager(
        pdf_dir = doc_path,
        temp_dir = temp_path,
        image_dir = img_path,
        output_dir = output_path,
        backup_dir = backup_path,
        logger = Logger(
            file_path = os.path.join(log_path, f"{date_string()}.log")
        )
    ).process()
