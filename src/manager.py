'''Pdf manager class'''

import os
from villog import Logger
from src.splitter import Splitter
from src.imager import Pdf2Img
from src.barcode_scanner import Scanner, Barcode

class PdfManager:
    '''Pdf manager class'''
    __EXTENSION: str = ".pdf"

    def __init__(self,
        pdf_dir: str,
        output_dir: str,
        image_dir: str,
        copy_dir: str,
        logger: Logger = None
    ) -> None:
        self.pdf_dir: str = pdf_dir
        self.output_dir: str = output_dir
        self.image_dir: str = image_dir
        self.copy_dir: str = copy_dir
        self.logger: Logger = logger if logger else Logger(
            file_path = f"{os.path.dirname(__file__)}.log"
        )

    def __log(self, content) -> None:
        self.logger.log(content)

    def __files_in_dir(self) -> list[str]:
        '''Return a list of files in a directory'''
        files_in_dir: list[str] = []
        for file in os.listdir(self.pdf_dir):
            if file.lower().endswith(self.__EXTENSION):
                files_in_dir.append(os.path.join(self.pdf_dir, file))
        return files_in_dir

    def __split_pdf(self, pdf_path: str) -> list[str]:
        '''Split the PDF file into individual pages'''
        splitter: Splitter = Splitter(
            pdf_path = pdf_path,
            output_dir = self.output_dir,
            logger = self.logger
        )
        splitter.split()
        return splitter.output_files

    def __convert_pdf_to_images(self, pdf_path: str) -> list[str]:
        '''Convert the PDF file to images'''
        pdf2img: Pdf2Img = Pdf2Img(
            pdf_path = pdf_path,
            output_path = self.image_dir,
            logger = self.logger
        )
        pdf2img.convert()
        return pdf2img.image_path

    def __check_barcode_on_image(self, image_path: str) -> list[Barcode]:
        '''Check for barcodes on the image'''
        scanner: Scanner = Scanner(
            image_path = image_path,
            logger = self.logger
        )
        scanner.scan_for_barcodes()
        return scanner.barcodes

    def __copy_file_as(self, file_path: str, new_file_path: str) -> None:
        '''Copy a file to a new location'''
        try:
            with open(file_path, "rb") as file:
                with open(new_file_path, "wb") as new_file:
                    new_file.write(file.read())
            self.__log(f"Copied {file_path} to {new_file_path}")
        except Exception as error:
            self.__log(f"Error copying {file_path} to {new_file_path}: {error}")

    def __remove_file(self, file_path: str) -> None:
        '''Remove a file'''
        try:
            os.remove(file_path)
        except Exception as error:
            self.__log(f"Error removing {file_path}: {error}")

    def process(self) -> None:
        '''Process the PDF files'''
        files = self.__files_in_dir()
        for i, pdf in enumerate(files):
            try:
                self.__log(f"{str(i + 1)}/{str(len(files))}. Processing {pdf}")
                split_pdf_files: list[str] = self.__split_pdf(pdf)
                for split_pdf_file in split_pdf_files:
                    split_image_files: list[str] = self.__convert_pdf_to_images(split_pdf_file)
                    for split_image_file in split_image_files:
                        barcodes: list[Barcode] = self.__check_barcode_on_image(split_image_file)
                        self.__remove_file(split_image_file)
                        if barcodes:
                            new_file_name: str = barcodes[0].barcode_data
                            new_file_path: str = os.path.join(self.copy_dir, f"{new_file_name}.pdf")
                            self.__copy_file_as(split_pdf_file, new_file_path)
                        else:
                            self.__copy_file_as(split_pdf_file, os.path.join(self.copy_dir, os.path.basename(split_pdf_file)))
                        self.__remove_file(split_pdf_file)
                self.__remove_file(pdf)
            except Exception as error:
                self.__log(f"Error processing {pdf}: {error}")