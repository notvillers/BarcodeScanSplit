'''barcode scanner class'''

import os
from dataclasses import dataclass
from pyzbar.pyzbar import decode
from PIL import Image
from villog import Logger

@dataclass
class Barcode:
    '''barcode class'''
    barcode_type: str
    barcode_data: str

class Scanner:
    '''barcode scanner class'''
    def __init__(self,
                 image_path: str,
                 logger: Logger|None = None) -> None:
        '''
            Barcode scanner class

            Args:
                image_path (str): Path to the image
                logger (Logger, optional): Logger object (creates one if not provided)
        '''
        self.image_path: str = image_path
        self.logger: Logger = logger or Logger(file_path = f"{os.path.dirname(__file__)}.log")
        self.barcodes: list[Barcode] = []

    def log(self,
            content: str) -> None:
        '''
            Log content

            Args:
                content (str): Content to log
        '''
        self.logger.log(content)

    def scan_for_barcodes(self) -> list[Barcode]:
        '''scan for barcodes'''
        try:
            image = Image.open(self.image_path)
            barcodes: list = decode(image)
            if barcodes:
                for barcode in barcodes:
                    barcode_type: str = barcode.type
                    barcode_data: str = barcode.data.decode("utf-8")
                    self.log(f"Barcode found: {barcode_type} - {barcode_data}")
                    self.barcodes.append(
                        Barcode(barcode_type = barcode_type,
                                barcode_data = barcode_data))
            else:
                self.log("No barcodes found")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error scanning for barcodes: {error}")
        return self.barcodes

    def get_barcodes(self) -> list[Barcode]:
        '''return barcodes'''
        return self.barcodes
