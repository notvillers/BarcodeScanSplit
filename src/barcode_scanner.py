'''barcode scanner class'''

import os
from pyzbar.pyzbar import decode
from PIL import Image
from villog import Logger

class Barcode:
    '''barcode class'''
    def __init__(self,
        barcode_type: str,
        barcode_data: str
    ) -> None:
        self.barcode_type: str = barcode_type
        self.barcode_data: str = barcode_data

class Scanner:
    '''barcode scanner class'''
    def __init__(self,
        image_path: str,
        logger: Logger = None
    ) -> None:
        self.image_path: str = image_path
        self.logger: Logger = logger if logger else Logger(
            file_path = f"{os.path.dirname(__file__)}.log"
        )
        self.barcodes: list[Barcode] = []

    def __log(self, content) -> None:
        self.logger.log(content)

    def scan_for_barcodes(self) -> list[Barcode]:
        '''scan for barcodes'''
        try:
            image = Image.open(self.image_path)
            barcodes = decode(image)
            if barcodes:
                for barcode in barcodes:
                    self.__log(f"Barcode found: {barcode.type} - {barcode.data.decode('utf-8')}")
                    self.barcodes.append(
                        Barcode(
                            barcode_type = barcode.type,
                            barcode_data = barcode.data.decode("utf-8"),
                        )
                    )
            else:
                self.__log("No barcodes found")
        except Exception as error:
            self.__log(f"Error scanning for barcodes: {error}")
        return self.barcodes

    def get_barcodes(self) -> list[Barcode]:
        '''return barcodes'''
        return self.barcodes
