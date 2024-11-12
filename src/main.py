'''main module'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import log_path, doc_path, temp_path, img_path, copy_path

def run() -> None:
    '''Main function'''
    logger: Logger = Logger(
        file_path = os.path.join(log_path, f"{date_string()}.log")
    )
    PdfManager(
        pdf_dir = doc_path,
        output_dir = temp_path,
        image_dir = img_path,
        copy_dir = copy_path,
        logger = logger
    ).process()
