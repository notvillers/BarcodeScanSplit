'''
    OCR reader class
'''

import os
import logging
import warnings
from dataclasses import dataclass
import cv2
import easyocr
from villog import Logger

logging.getLogger("easyocr").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

warnings.filterwarnings("ignore",
                        message = ".*pin_memory.*no accelerator is found.*")

@dataclass(slots = True)
class ImgData:
    '''
        Image data class
    '''
    path: str
    ratio: float = 1.0


class OcrReader:
    '''
        OCR reader class
    '''
    REPLACES: list[str] = ["O", "0",
                            "l", "1"]
    def __init__(self, # pylint: disable=dangerous-default-value
                 image_data: ImgData,
                 prefixes: list[str],
                 languages: list[str] = ["hu", "en"],
                 logger: Logger | None = None) -> None:
        '''
            OCR reader class

            :param img_data: :class:`ImgData`
            :param prefixes: :class:`list[str]`
            :param languages: :class:`Optional(list[str])` defaults to `["hu", "en"]`
            :param logger: :class:`Optional(Union(Logger, None))` Defaults to `None`
        ''' # pylint: disable=line-too-long
        self.image_data: ImgData = image_data
        self.prefixes: list[str] = prefixes
        self.languages: list[str] = languages
        self.logger: Logger = logger or Logger(file_path = f"{os.path.dirname(__file__)}.log")
        self.image = cv2.imread(self.image_data.path) # pylint: disable=no-member
        self.__crop_to_ratio()


    def __log(self,
              content: any) -> None:
        '''
            Log content

            :param content: :class:`any`
        '''
        self.logger.log(content = content)


    def __crop_to_ratio(self) -> None:
        '''
            Crops image to given ratio
        '''
        if not 0 < self.image_data.ratio <= 1:
            self.__log(f"Ratio is not valid '{str(self.image_data.ratio)}', changing to 1")
            self.image_data.ratio = 1.0

        height, width = self.image.shape[:2]
        self.image = self.image[:int(height * self.image_data), :width]


    def __read_file_text(self) -> list[str]:
        '''
            Reads text on given file on the given ratio
        '''
        reader: easyocr.Reader = easyocr.Reader(self.languages,
                                                gpu = True)
        results = reader.readtext(self.image)

        return [text for _, text, _ in results]


    def __get_file_prefix_text(self) -> list[str]:
        '''
            Reads text on file and returns if it is prefix
        '''
        prefix_text: list[str] = []
        for text in self.__read_file_text():
            for prefix in self.prefixes:
                if prefix in text:
                    prefix_text.append(text)
        return prefix_text


    def __convert_prefixed_text(self) -> list[str]:
        '''
            Convert missmatched characters like 'O' to '0'
        '''
        texts: list[str] = []
        for text in self.__get_file_prefix_text():
            temp_text: str = text
            for replace in self.REPLACES:
                if replace[0] in temp_text:
                    temp_text.replace(replace[0],
                                      replace[1])
            texts.append(temp_text)
        return texts


    def get_texts(self) -> str:
        '''
            Gets first no text
        '''
        return self.__convert_prefixed_text()
