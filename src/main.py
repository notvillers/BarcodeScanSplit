'''main module'''

import os
from villog import Logger
from src.slave import date_string
from src.splitter import DirSplitter
from src.imager import PdfToImg
from src.barcode_scanner import Scanner
from config import log_path, doc_path, temp_path, img_path

def run() -> None:
    '''Main function'''
    logger: Logger = Logger(
        file_path = os.path.join(log_path, f"{date_string()}.log")
    )
    files_splitter: DirSplitter = DirSplitter(
        input_folder = doc_path,
        output_folder = temp_path,
        logger = logger
    )
    files_splitter.split()
    for paths in files_splitter.output_paths:
        for key, value in paths.items():
            for val in value:
                pdf_to_img: PdfToImg = PdfToImg(
                    pdf_path = val,
                    output_path = img_path
                )
                conv_img_paths: str = pdf_to_img.convert()
                for conv_img_path in conv_img_paths:
                    scanner: Scanner = Scanner(
                        image_path = conv_img_path
                    )
                    barcodes = scanner.scan_for_barcodes()
                    for barcode in barcodes:
                        logger.log(f"Barcode type: {barcode[0]}")
                        logger.log(f"Barcode data: {barcode[1]}")