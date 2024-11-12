'''imager class '''

import os
from pdf2image import convert_from_path
from villog import Logger

class Pdf2Img:
    '''Pdf2Img class'''
    def __init__(self,
        pdf_path: str,
        output_path: str,
        logger: Logger = None
    ) -> None:
        self.pdf_path: str = pdf_path
        self.output_path: str = output_path
        self.logger: Logger = logger if logger else Logger(
            file_path = f"{os.path.dirname(__file__)}.log"
        )
        self.image_path: list[str]|str = []

    def __log(self, content) -> None:
        self.logger.log(content)

    def convert(self) -> str:
        '''convert to image'''
        images = convert_from_path(self.pdf_path)
        pdf_path_name: str = os.path.basename(self.pdf_path)
        pdf_path_name = pdf_path_name.replace(".pdf", "").replace(".PDF", "")
        for i, images in enumerate(images):
            image_path: str = os.path.join(self.output_path, f"{pdf_path_name}_{i}.png")
            images.save(image_path, "PNG")
            self.image_path.append(image_path)
            self.__log(f"Converted {self.pdf_path} to {image_path}")
        return self.image_path
