'''
    Pdf manager module
'''

import os
from pathlib import Path
from multiprocessing import Process, freeze_support
from villog import Logger
from src.pdf_splitter import PdfSplitter
from src.imager import Pdf2Img
from src.barcode_scanner import Scanner, Barcode
from src.ocr_reader import ImgData, OcrReader

class PdfManagerException(Exception):
    '''
        Pdf manager exception class
    '''
    def __init__(self,
                 message: str | None = None):
        '''
            Pdf manager exception class

            :param message: :class:`Optional(Union(str, None))` Message to the exception. Defaults to `None`
        ''' # pylint: disable=line-too-long
        super().__init__(message or "Unknow PDF Manager exception")


class PdfManager:
    '''
        Pdf manager class
    '''
    EXTENSION: str = ".pdf"

    __slots__ = ["pdf_dir",
                 "temp_dir",
                 "image_dir",
                 "output_dir",
                 "backup_dir",
                 "ocr_prefixes",
                 "ratio",
                 "logger"]
    def __init__(self,
                 pdf_dir: str,
                 temp_dir: str,
                 image_dir: str,
                 output_dir: str,
                 backup_dir: str | None = None,
                 ocr_prefixes: list[str] | None = None,
                 ratio: float | None = None,
                 logger: Logger | None = None) -> None:
        '''
            PDF manager class

            :param pdf_dir: :class:`Optional(Union(str, None))` PDF directory. Defaults to `None`
            :param temp_dir: :class:`Optional(Union(str, None))` Temporary directory. Defaults to `None`
            :param image_dir: :class:`Optional(Union(str, None))` Image directory. Defaults to `None`
            :param output_dir: :class:`Optional(Union(str, None))` Output directory. Defaults to `None`
            :param backup_dir: :class:`Optional(Union(str, None))` Backup directory. Defaults to `None`
            :param ocr_prefixes: class:`Optional(Union(list[str], None))` Defaults to `None`
            :param ratio: :class:`Optional(Union(float, None))` Defaults to `None`
            :param logger: :class:`Optional(Union(Logger, None))` Logger class, creates one if not provided. Defaults to `None`
        ''' # pylint: disable=line-too-long
        self.pdf_dir: str = self.__check_path(pdf_dir)
        self.temp_dir: str = self.__check_path(temp_dir)
        self.image_dir: str = self.__check_path(image_dir)
        self.output_dir: str = self.__check_path(output_dir)
        self.backup_dir: str | None = self.__check_path(backup_dir) if backup_dir else None
        self.ocr_prefixes: list[str] | None = ocr_prefixes
        self.ratio: list[float] | None = ratio
        self.logger: Logger = logger or Logger(file_path = f"{os.path.dirname(__file__)}.log")


    def log(self,
            content: str) -> None:
        '''
            Logs content

            :param content: :class:`str` Content to log.
        '''
        self.logger.log(content)


    def __check_path(self,
                     dir_path: str) -> str:
        '''
            Check if the path exists, if not raise an exception

            :param dir_path: :class:`str` Path to check
        '''
        if not os.path.exists(dir_path):
            raise PdfManagerException(f"Path does not exist: {dir_path}")
        return dir_path


    def __files_in_dir(self) -> list[str]:
        '''
            Get the list of PDF files in {pdf_dir} with the extension of {EXTENSION}
        '''
        files_in_dir: list[str] = []
        for file in os.listdir(self.pdf_dir):
            if file.lower().endswith(self.EXTENSION):
                files_in_dir.append(os.path.join(self.pdf_dir,
                                                 file))
        return files_in_dir


    def __create_lock_file(self,
                           file_path: str,
                           encoding: str = "utf-8-sig") -> None:
        '''
            Create a lock file for the file

            :param file_path: :class:`str` .lock file to create
            :param encoding: :class:`Optional(str)` Encoding of the file. Defaults to `"utf-8-sig`
        '''
        try:
            with open(f"{file_path}.lock",
                      "w",
                      encoding = encoding) as lock_file:
                lock_file.write("LOCKED")
            self.log(f"Lock file created for {file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error creating lock file for {file_path}: {error}")


    def __check_lock_file(self,
                          file_path: str) -> bool:
        '''
            Check if the file is locked

            :param file_path: :class:`str` File path
        '''
        return os.path.exists(f"{file_path}.lock")


    def __check_and_create_lock_file(self,
                                     file_path: str,
                                     encoding: str = "utf-8-sig") -> bool:
        '''
            Check if the file is locked and create a lock file if it is not

            :param file_path: :class:`str` File path
            :param encoding: :class:`Optional(str)` Encoding of the file. Defaults to `"utf-8-sig"`
        '''
        if not self.__check_lock_file(file_path):
            self.__create_lock_file(file_path,
                                    encoding)
            return False
        return True


    def __remove_lock_file(self,
                           file_path: str) -> None:
        '''
            Remove the lock file for the file

            :param file_path: :class:`str` File path
        '''
        try:
            os.remove(f"{file_path}.lock")
            self.log(f"Removed lock file for {file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error removing lock file for {file_path}: {error}")


    def __split_pdf(self,
                    pdf_path: str) -> list[str]:
        '''
            Split the PDF file into individual pages

            :param pdf_path: :class:`str` File path
        '''
        splitter: PdfSplitter = PdfSplitter(pdf_path = pdf_path,
                                            output_dir = self.temp_dir,
                                            logger = self.logger)
        splitter.split()
        return splitter.output_files


    def __convert_pdf_to_images(self,
                                pdf_path: str) -> list[str]:
        '''
            Convert the PDF file to images

            :param pdf_path: :class:`str` File path
        '''
        pdf2img: Pdf2Img = Pdf2Img(pdf_path = pdf_path,
                                   output_path = self.image_dir,
                                   logger = self.logger)
        pdf2img.convert()
        return pdf2img.image_path


    def __check_barcode_on_image(self,
                                 image_path: str) -> list[Barcode]:
        '''
            Check for barcodes on the image

            :param image_path: :class:`str` File path
        '''
        scanner: Scanner = Scanner(image_path = image_path,
                                   logger = self.logger)
        scanner.scan_for_barcodes()
        return scanner.barcodes


    def __get_enum_for_ocr(self,
                           base_name: str) -> str:
        '''
            Gets enum for ocr read pdf

            :param base_name: :class:`str`
        '''
        output_path: str = os.path.join(self.output_dir,
                                        f"{base_name}.pdf")
        path: Path = Path(output_path)
        i: int = 1
        path = path.with_stem(f"{path.stem}_{i}")
        while os.path.exists(str(path)):
            i += 1
            path.stem[-1] = str(i)
            path = path.with_stem(f"{path.stem[:-1]}_{i}")
        return path.stem


    def __get_prefixed_text_from_image(self,
                                       image_path: str) -> list[Barcode]:
        '''
            Gets first `self.ocr_prefixed` text from image, if found

            :param image_data: :class:`str`
        '''
        ocr_reader: OcrReader = OcrReader(image_data = ImgData(path = image_path,
                                                               ratio = self.ratio),
                                          prefixes = self.ocr_prefixes,
                                          logger = self.logger)
        barcodes: list[Barcode] = [Barcode(barcode_type = "ocr_reader",
                                           barcode_data = self.__get_enum_for_ocr(text)) for text in ocr_reader.get_texts()] # pylint: disable=line-too-long
        return barcodes



    def __copy_file_as(self,
                       file_path: str,
                       new_file_path: str) -> None:
        '''
            Copy a file to a new location

            :param file_path: :class:`str` File path
            :param new_file_path: :class:`str` New file path
        '''
        try:
            with open(file_path,
                      "rb") as file:
                with open(new_file_path,
                          "wb") as new_file:
                    new_file.write(file.read())
            self.log(f"Copied {file_path} to {new_file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error copying {file_path} to {new_file_path}: {error}")


    def __remove_file(self,
                      file_path: str) -> None:
        '''
            Remove a file

            :param file_path: :class:`str` File path
        '''
        try:
            os.remove(file_path)
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error removing {file_path}: {error}")


    def __remove_file_and_lock_file(self,
                                    file_path: str) -> None:
        '''
            Remove the file and its lock file

            :param file_path: :class:`str` File path
        '''
        self.__remove_file(file_path)
        self.__remove_lock_file(file_path)


    def __backup_file(self,
                      file_path: str,
                      backup_dir: str | None = None) -> bool:
        '''
            Backup a file to the backup directory

            :param file_path: :class:`str` File path
            :param backup_dir: :class:`Optional(Union(str, None))` Backupd directory. Defaults to `None` and uses `self.backup_dir`
        ''' # pylint: disable=line-too-long
        backup_dir = backup_dir or self.backup_dir
        if backup_dir:
            if os.path.exists(backup_dir):
                self.__copy_file_as(file_path = file_path,
                                    new_file_path = os.path.join(backup_dir,
                                                                 os.path.basename(file_path)))
                self.log(f"Backed up {file_path} to {backup_dir}")
                return True
        return False


    def process_file(self,
                       pdf_file: str,
                       i: int | None = None,
                       length: int | None = None) -> None:
        '''
            Process a single PDF file

            :param pdf_file: :class:`str` File path
            :param i: :class:`Optional(Union(int, None))` Enumerate. Defaults to `None`
            :param length: :class:`Optional(Union(int, None))` Length for enumerate. Default to `None`
        ''' # pylint: disable=line-too-long
        pcs: str = f"{str(i + 1)}/{str(length)}." if i and length else ""
        try:
            self.log(f"{pcs} Processing {pdf_file}")
            if not self.__check_and_create_lock_file(pdf_file):
                self.__backup_file(pdf_file)
                split_files: list[str] = self.__split_pdf(pdf_file)
                for cnt, split_pdf_file in enumerate(split_files):
                    self.log(f"{cnt + 1}/{len(split_files)}.: {pdf_file} -> {split_pdf_file}")
                    for split_image_file in self.__convert_pdf_to_images(split_pdf_file):
                        barcodes: list[Barcode] = self.__check_barcode_on_image(split_image_file)
                        if not barcodes and self.ratio is not None and self.ocr_prefixes:
                            self.log(f"Trying to OCR read '{split_image_file}'")
                            barcodes = self.__get_prefixed_text_from_image(split_image_file)
                        self.__remove_file(split_image_file)
                        self.__copy_file_as(split_pdf_file,
                                            os.path.join(self.output_dir,
                                                        f"{barcodes[0].barcode_data}.pdf" if barcodes else os.path.basename(split_pdf_file))) # pylint: disable=line-too-long
                        self.__remove_file(split_pdf_file)
                self.__remove_file_and_lock_file(pdf_file)
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error processing {pdf_file}: {error}")


    def process_all(self) -> None:
        '''
            Process the PDF files in the directory
        '''
        self.log(f"Processing '{self.pdf_dir}'")
        files: list[str] = self.__files_in_dir()
        if not files:
            self.log("No files found")
            return
        self.log(f"Processing {len(files)} file{'' if len(files) < 2 else 's'} using single process") # pylint: disable=line-too-long
        for i, pdf in enumerate(files):
            self.process_file(pdf_file = pdf,
                                i = i,
                                length = len(files))


    def __remove_dead_processes(self,
                                processes: list[Process]) -> list[Process]:
        '''
            Remove dead processes from the list

            :param processes: :class:`list[Process]` Remove dead processes.
        '''
        for process in processes:
            if not process.is_alive():
                processes.remove(process) #pylint: disable = modified-iterating-list
        return processes


    def __wait_if_process_on_limit(self,
                                   processes: list[Process],
                                   max_processes: int) -> None:
        '''
            Wait if the number of processes is greater than max_processes

            :param processes: :class:`list[Process]` List of processes to wait for
            :param max_processes: :class:`int` Maximum number of processes.
        '''
        wait: bool = True
        while len(processes) >= max_processes:
            if wait:
                self.log("Waiting for processes to finish")
                wait = False
            processes = self.__remove_dead_processes(processes)
        return processes


    def multi_process_all(self,
                          max_processes: int = 2) -> None:
        '''
            Process the PDF files in the directory using multiprocessing

            :param max_processes: :class:`Optional(int)` Max processes to run. Defaults to `4`
        '''
        self.log(f"Processing '{self.pdf_dir}'")
        files: list[str] = self.__files_in_dir()
        if not files:
            self.log("No files found in")
            return
        if not isinstance(max_processes, int):
            if isinstance(max_processes, float):
                self.log("'max_processes' is float, rounding it")
                max_processes = int(round(max_processes, 0))
            else:
                raise PdfManagerException("'max_processes' should be an integer")
        if max_processes < 1:
            raise PdfManagerException("'max_processes' minimum value is 1")
        # looping pdf files
        self.log(f"Processing {len(files)} file{'' if len(files) < 2 else 's'} using {max_processes} processes") # pylint: disable=line-too-long
        # starting the multiprocessing
        freeze_support()
        processes: list[Process] = []
        for i, pdf in enumerate(files):
            # creating a process for each pdf file
            process: Process = Process(target = self.process_file,
                                       args = (pdf, i, len(files)))
            # adding the process to the list
            processes.append(process)
            # starting the process
            process.start()
            # wait if the number of processes is greater than max_processes
            self.__wait_if_process_on_limit(processes = processes,
                                            max_processes = max_processes)
        for process in processes:
            process.join()
        self.log("All processes finished")
