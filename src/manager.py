'''Pdf manager class'''

import os
from villog import Logger
from src.splitter import Splitter
from src.imager import Pdf2Img
from src.barcode_scanner import Scanner, Barcode

class PdfManagerException(Exception):
    '''Pdf manager exception class'''
    def __init__(self, message):
        super().__init__(message)

class PdfManager:
    '''Pdf manager class'''
    __EXTENSION: str = ".pdf"

    def __init__(self,
        pdf_dir: str,
        temp_dir: str,
        image_dir: str,
        output_dir: str,
        backup_dir: str = None,
        logger: Logger = None
    ) -> None:
        """
            PDF manager class

            Args:
                pdf_dir (str): Directory containing PDF files
                temp_dir (str): Temporary directory to store split PDF files
                image_dir (str): Directory to store images
                output_dir (str): Directory to store output files
                backup_dir (str, optional): Directory to store backup files
                logger (Logger, optional): Logger object (creates one if not provided)
        """
        self.pdf_dir: str = pdf_dir
        self.temp_dir: str = temp_dir
        self.image_dir: str = image_dir
        self.output_dir: str = output_dir
        self.backup_dir: str = backup_dir
        self.logger: Logger = logger if logger else Logger(
            file_path = f"{os.path.dirname(__file__)}.log"
        )

    def __log(self, content) -> None:
        """
            Logs content

            Args:
                content (str): Content to log
        """
        self.logger.log(content)

    def __files_in_dir(self) -> list[str]:
        """
            Get the list of PDF files in {pdf_dir} with the extension of {__EXTENSION}
        """
        files_in_dir: list[str] = []
        for file in os.listdir(self.pdf_dir):
            if file.lower().endswith(self.__EXTENSION):
                files_in_dir.append(os.path.join(self.pdf_dir, file))
        return files_in_dir

    def __split_pdf(self, pdf_path: str) -> list[str]:
        """
            Split the PDF file into individual pages

            Args:
                pdf_path (str): Path to the PDF file
        """
        splitter: Splitter = Splitter(
            pdf_path = pdf_path,
            output_dir = self.temp_dir,
            logger = self.logger
        )
        splitter.split()
        return splitter.output_files

    def __convert_pdf_to_images(self, pdf_path: str) -> list[str]:
        """
            Convert the PDF file to images

            Args:
                pdf_path (str): Path to the PDF file
        """
        pdf2img: Pdf2Img = Pdf2Img(
            pdf_path = pdf_path,
            output_path = self.image_dir,
            logger = self.logger
        )
        pdf2img.convert()
        return pdf2img.image_path

    def __check_barcode_on_image(self, image_path: str) -> list[Barcode]:
        """
            Check for barcodes on the image

            Args:
                image_path (str): Path to the image file
        """
        scanner: Scanner = Scanner(
            image_path = image_path,
            logger = self.logger
        )
        scanner.scan_for_barcodes()
        return scanner.barcodes

    def __copy_file_as(self, file_path: str, new_file_path: str, silent: bool = False) -> None:
        """
            Copy a file to a new location

            Args:
                file_path (str): Path to the file to copy
                new_file_path (str): Path to the new file
        """
        try:
            with open(file_path, "rb") as file:
                with open(new_file_path, "wb") as new_file:
                    new_file.write(file.read())
            if not silent:
                self.__log(f"Copied {file_path} to {new_file_path}")
        except Exception as error:
            self.__log(f"Error copying {file_path} to {new_file_path}: {error}")

    def __remove_file(self, file_path: str) -> None:
        """
            Remove a file

            Args:
                file_path (str): Path to the file to remove
        """
        try:
            os.remove(file_path)
        except Exception as error:
            self.__log(f"Error removing {file_path}: {error}")

    def __backup_files(self) -> None:
        """
            Backup files to backup directory
        """
        if self.backup_dir:
            if os.path.exists(self.backup_dir):
                self.__log(f"Backing up files to {self.backup_dir}")
                for file in self.__files_in_dir():
                    self.__copy_file_as(file, os.path.join(self.backup_dir, os.path.basename(file)), silent = True)
            else:
                raise PdfManagerException(f"Backup directory {self.backup_dir} does not exist")

    def process(self) -> None:
        """
            Process the PDF files in the directory
        """
        files = self.__files_in_dir()
        self.__backup_files()
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
                            new_file_path: str = os.path.join(self.output_dir, f"{new_file_name}.pdf")
                            self.__copy_file_as(split_pdf_file, new_file_path)
                        else:
                            new_file_path: str = os.path.join(self.output_dir, os.path.basename(split_pdf_file))
                            self.__copy_file_as(split_pdf_file, new_file_path)
                        self.__remove_file(split_pdf_file)
                self.__remove_file(pdf)
            except Exception as error:
                self.__log(f"Error processing {pdf}: {error}")
