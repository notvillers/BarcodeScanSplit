'''barcode scanner class'''

import os
from dataclasses import dataclass
from pyzbar.pyzbar import decode as pyz_decode, Decoded
from PIL import Image
from PIL.ImageOps import grayscale
from PIL.ImageFile import ImageFile
from PIL.ImageEnhance import Contrast
from PIL.ImageFilter import SHARPEN
from villog import Logger

@dataclass(slots = True)
class Barcode:
    ''' 
        Barcode class
    '''
    barcode_type: str
    barcode_data: str


class Scanner:
    '''
        Barcode scanner class
    '''
    ENHANCE_MIN: int = 0
    ENHANCE_MAX: int = 3

    CONTRAST_RATIO: float = 2.0
    INCREASE_RATIO: float = 2.0

    __slots__: list[str] = ["image_path",
                            "image_file",
                            "image",
                            "logger",
                            "barcodes",
                            "enhance_count"]

    def __init__(self,
                 image_path: str,
                 logger: Logger | None = None) -> None:
        '''
            Barcode scanner class

            :param image_path: :class:`str` Path to the image
            :param logger: :class:`Optional(Union(Logger, None))` Logger object, creates one if not provided. Defaults to `None`
        ''' # pylint: disable=line-too-long
        self.image_path: str = image_path
        self.image_file: ImageFile = Image.open(self.image_path)
        self.image = self.image_file.copy()
        self.logger: Logger = logger or Logger(file_path = f"{os.path.dirname(__file__)}.log")
        self.barcodes: list[Barcode] = []
        self.enhance_count: int = self.ENHANCE_MIN

    def log(self,
            content: str) -> None:
        '''
            Log content

            :param content: :class:`str` Content to log
        '''
        self.logger.log(content)


    def __inc_enhance_cnt(self) -> None:
        '''
            Increments enhance count
        '''
        self.enhance_count += 1


    def __grayscale_image(self) -> None:
        '''
            Grayscales image
        '''
        self.log(content = f"Grayscaling '{self.image_path}'")
        self.image = grayscale(self.image)


    def __sharpen_image(self) -> None:
        '''
            Sharpens image
        '''
        self.log(content = f"Sharpening '{self.image_path}'")
        self.image = self.image.filter(SHARPEN)


    def __contrast_image(self,
                         contrast_ratio: float = CONTRAST_RATIO) -> None:
        '''
            Increases image contrast

            :param contrast_ratio: :class:`float` defaults to `CONTRAST_RATIO`
        '''
        self.log(content = f"Contrasting '{self.image_path}'")
        enhancer: Contrast = Contrast(self.image)
        self.image = enhancer.enhance(contrast_ratio)


    def __increase_image(self,
                         increase_ratio: float = INCREASE_RATIO) -> None:
        '''
            Increase image size

            :param increase_ratio: :class:`float` defaults to `INCREASE_RATIO`
        '''
        self.log(content = f"Increasing '{self.image_path}'")
        ratio_int: int = int(round(increase_ratio, 0))
        width, height = self.image.size
        self.image = self.image.resize((width * ratio_int,
                                        height * ratio_int))

    def __enhance_image(self) -> None:
        '''
            Enhances image
        '''
        match self.enhance_count:
            case 0:
                self.__grayscale_image()
                self.__inc_enhance_cnt()
                return None
            case 1:
                self.__increase_image()
                self.__inc_enhance_cnt()
                return None
            case 2:
                self.__contrast_image()
                self.__inc_enhance_cnt()
                return None
            case 3:
                self.__sharpen_image()
                self.__inc_enhance_cnt()
                return None
            case _:
                return None
        return None

    def decode_pyz(self) -> list[Decoded]:
        '''
            Decodes barcodes from `Image` and tries to enhance if fails
        '''
        barcodes: list[Decoded] = []
        while self.enhance_count <= self.ENHANCE_MAX and not barcodes:
            barcodes = pyz_decode(self.image)
            if barcodes:
                break
            self.__enhance_image()
        return barcodes


    def scan_for_barcodes(self) -> list[Barcode]:
        '''
            Scan for barcodes
        '''
        try:
            barcodes: list[Decoded] = self.decode_pyz()
            if barcodes:
                for barcode in barcodes:
                    barcode_type: str = barcode.type
                    barcode_data: str = barcode.data.decode("utf-8")
                    self.log(f"'{self.image_path}' Barcode found: {barcode_type} - {barcode_data}")
                    self.barcodes.append(Barcode(barcode_type = barcode_type,
                                                 barcode_data = barcode_data))
            else:
                self.log("No barcodes found")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error scanning for barcodes: {error}")
        return self.barcodes

    def get_barcodes(self) -> list[Barcode]:
        '''
            Return barcodes
        '''
        return self.barcodes
