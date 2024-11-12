'''barcode scanner class'''

from pyzbar.pyzbar import decode
from PIL import Image

class Scanner:
    '''barcode scanner class'''
    def __init__(self,
        image_path: str
    ) -> None:
        self.image_path: str = image_path

    def scan_for_barcodes(self):
        '''scan for barcodes'''
        image = Image.open(self.image_path)
        barcodes = decode(image)
        barcode_arr: list[str] = []
        if barcodes:
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                barcode_arr.append([barcode_type, barcode_data])
        return barcode_arr