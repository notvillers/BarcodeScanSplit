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

    def __create_lock_file(self, file_path: str, encoding: str = "utf-8-sig") -> None:
        """
            Create a lock file for the file

            Args:
                file_path (str): Path to the file
        """
        try:
            with open(f"{file_path}.lock", "w", encoding = encoding) as lock_file:
                lock_file.write("LOCKED")
            self.__log(f"Lock file created for {file_path}")
        except Exception as error:
            self.__log(f"Error creating lock file for {file_path}: {error}")

    def __check_lock_file(self, file_path: str) -> bool:
        """
            Check if the file is locked

            Args:
                file_path (str): Path to the file
        """
        return os.path.exists(f"{file_path}.lock")

    def __check_and_create_lock_file(self, file_path: str, encoding: str = "utf-8-sig") -> bool:
        """
            Check if the file is locked and create a lock file if it is not

            Args:
                file_path (str): Path to the file
        """
        if not self.__check_lock_file(file_path):
            self.__create_lock_file(file_path, encoding)
            return False
        return True

    def __remove_lock_file(self, file_path: str) -> None:
        """
            Remove the lock file for the file

            Args:
                file_path (str): Path to the file
        """
        try:
            os.remove(f"{file_path}.lock")
            self.__log(f"Removed lock file for {file_path}")
        except Exception as error:
            self.__log(f"Error removing lock file for {file_path}: {error}")

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

    def __remove_file_and_lock_file(self, file_path: str) -> None:
        """
            Remove the file and its lock file

            Args:
                file_path (str): Path to the file
        """
        self.__remove_file(file_path)
        self.__remove_lock_file(file_path)

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
                if not self.__check_and_create_lock_file(pdf):
                    for split_pdf_file in self.__split_pdf(pdf):
                        for split_image_file in self.__convert_pdf_to_images(split_pdf_file):
                            barcodes: list[Barcode] = self.__check_barcode_on_image(split_image_file)
                            self.__remove_file(split_image_file)
                            self.__copy_file_as(
                                split_pdf_file,
                                os.path.join(
                                    self.output_dir,
                                    f"{barcodes[0].barcode_data}.pdf" if barcodes else os.path.basename(split_pdf_file)
                                )
                            )
                            self.__remove_file(split_pdf_file)
                    self.__remove_file_and_lock_file(pdf)
                else:
                    self.__log(f"Skipping {pdf} as it is locked")
            except Exception as error:
                self.__log(f"Error processing {pdf}: {error}")
