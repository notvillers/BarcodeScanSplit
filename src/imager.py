'''imager class '''

import os
from pdf2image import convert_from_path
from PIL import Image
from villog import Logger

class Pdf2Img:
    '''
        Pdf2Img class
    '''
    __slots__: list[str] = ["pdf_path",
                            "output_path",
                            "logger",
                            "image_path"]
    def __init__(self,
                 pdf_path: str,
                 output_path: str,
                 logger: Logger | None = None) -> None:
        '''
            Pdf2Img class

            :param pdf_path: :class:`str` Path to the .pdf file
            :param output_path: :class:`str` Path to the output directory
            :param logger: :class:`Optional(Union(logger, None))` Logger object, creates on if not provided. Defaults to `None`
        ''' # pylint: disable=line-too-long
        self.pdf_path: str = pdf_path
        self.output_path: str = output_path
        self.logger: Logger = logger or Logger(file_path = f"{os.path.dirname(__file__)}.log")
        self.image_path: list[str] | str = []


    def log(self,
            content: str) -> None:
        '''
            Log content

            :param content: :class:`str` Content to log
        '''
        self.logger.log(content)


    def convert(self) -> str:
        '''
            Convert to image
        '''
        images: list[Image.Image] = convert_from_path(self.pdf_path)
        pdf_path_name: str = os.path.basename(self.pdf_path).replace(".pdf", "").replace(".PDF", "")
        for i, image in enumerate(images):
            image_path: str = os.path.join(self.output_path,
                                           f"{pdf_path_name}_{i}.png")
            image.save(image_path, "PNG")
            self.image_path.append(image_path)
            self.log(f"Converted {self.pdf_path} to {image_path}")
        return self.image_path
