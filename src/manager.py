'''Pdf manager class'''

import os
from multiprocessing import Process, freeze_support
from villog import Logger
from src.pdf_splitter import PdfSplitter
from src.imager import Pdf2Img
from src.barcode_scanner import Scanner, Barcode

class PdfManagerException(Exception):
    '''Pdf manager exception class'''
    def __init__(self, message):
        super().__init__(message)

class PdfManager:
    '''Pdf manager class'''
    EXTENSION: str = ".pdf"

    __slots__ = [
        "pdf_dir",
        "temp_dir",
        "image_dir",
        "output_dir",
        "backup_dir",
        "logger"
    ]
    def __init__(self,
        pdf_dir: str,
        temp_dir: str,
        image_dir: str,
        output_dir: str,
        backup_dir: str = None,
        logger: Logger = None
    ) -> None:
        '''
            PDF manager class

            Args:
                pdf_dir (str): Directory containing PDF files
                temp_dir (str): Temporary directory to store split PDF files
                image_dir (str): Directory to store images
                output_dir (str): Directory to store output files
                backup_dir (str, optional): Directory to store backup files
                logger (Logger, optional): Logger object (creates one if not provided)
        '''
        self.pdf_dir: str = self.check_path(pdf_dir)
        self.temp_dir: str = self.check_path(temp_dir)
        self.image_dir: str = self.check_path(image_dir)
        self.output_dir: str = self.check_path(output_dir)
        self.backup_dir: str = self.check_path(backup_dir)
        self.logger: Logger = logger if logger else Logger(
            file_path = f"{os.path.dirname(__file__)}.log"
        )

    def log(self, content) -> None:
        '''
            Logs content

            Args:
                content (str): Content to log
        '''
        self.logger.log(content)

    def check_path(self,
        dir_path: str
    ) -> str:
        '''
            Check if the path exists, if not raise an exception

            Args:
                path (str): Path to check
        '''
        if not os.path.exists(dir_path):
            raise PdfManagerException(f"Path does not exist: {dir_path}")
        return dir_path

    def files_in_dir(self) -> list[str]:
        """
            Get the list of PDF files in {pdf_dir} with the extension of {EXTENSION}
        """
        files_in_dir: list[str] = []
        for file in os.listdir(self.pdf_dir):
            if file.lower().endswith(self.EXTENSION):
                files_in_dir.append(os.path.join(self.pdf_dir, file))
        return files_in_dir

    def create_lock_file(self,
        file_path: str,
        encoding: str = "utf-8-sig"
    ) -> None:
        """
            Create a lock file for the file

            Args:
                file_path (str): Path to the file
        """
        try:
            with open(f"{file_path}.lock", "w", encoding = encoding) as lock_file:
                lock_file.write("LOCKED")
            self.log(f"Lock file created for {file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error creating lock file for {file_path}: {error}")

    def check_lock_file(self, file_path: str) -> bool:
        """
            Check if the file is locked

            Args:
                file_path (str): Path to the file
        """
        return os.path.exists(f"{file_path}.lock")

    def check_and_create_lock_file(self,
        file_path: str,
        encoding: str = "utf-8-sig"
    ) -> bool:
        """
            Check if the file is locked and create a lock file if it is not

            Args:
                file_path (str): Path to the file
        """
        if not self.check_lock_file(file_path):
            self.create_lock_file(file_path, encoding)
            return False
        return True

    def remove_lock_file(self,
        file_path: str
    ) -> None:
        """
            Remove the lock file for the file

            Args:
                file_path (str): Path to the file
        """
        try:
            os.remove(f"{file_path}.lock")
            self.log(f"Removed lock file for {file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error removing lock file for {file_path}: {error}")

    def split_pdf(self,
        pdf_path: str
    ) -> list[str]:
        """
            Split the PDF file into individual pages

            Args:
                pdf_path (str): Path to the PDF file
        """
        splitter: PdfSplitter = PdfSplitter(
            pdf_path = pdf_path,
            output_dir = self.temp_dir,
            logger = self.logger
        )
        splitter.split()
        return splitter.output_files

    def convert_pdf_to_images(self,
        pdf_path: str
    ) -> list[str]:
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

    def check_barcode_on_image(self,
        image_path: str
    ) -> list[Barcode]:
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

    def copy_file_as(self,
        file_path: str,
        new_file_path: str,
        silent: bool = False
    ) -> None:
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
                self.log(f"Copied {file_path} to {new_file_path}")
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error copying {file_path} to {new_file_path}: {error}")

    def remove_file(self,
        file_path: str
    ) -> None:
        """
            Remove a file

            Args:
                file_path (str): Path to the file to remove
        """
        try:
            os.remove(file_path)
        except Exception as error: #pylint: disable=broad-exception-caught
            self.log(f"Error removing {file_path}: {error}")

    def remove_file_and_lock_file(self,
        file_path: str
    ) -> None:
        """
            Remove the file and its lock file

            Args:
                file_path (str): Path to the file
        """
        self.remove_file(file_path)
        self.remove_lock_file(file_path)

    def backup_file(self,
        file_path: str,
        backup_dir: str|None = None
    ) -> bool:
        '''
            Backup a file to the backup directory

            Args:
                file_path (str): Path to the file to backup
                backup_dir (str, optional): Directory to backup the file to
        '''
        backup_dir = backup_dir if backup_dir else self.backup_dir
        if os.path.exists(backup_dir):
            self.copy_file_as(
                file_path = file_path,
                new_file_path = os.path.join(backup_dir, os.path.basename(file_path)),
                silent = True
            )
            self.log(f"Backed up {file_path} to {backup_dir}")
            return True
        return False

    def process_file(self,
        pdf_file: str,
        i: int|None = None,
        length: int|None = None
    ) -> None:
        '''
            Process a single PDF file

            Args:
                pdf (str): Path to the PDF file
        '''
        pcs: str = f"{str(i + 1)}/{str(length)}." if i and length else ""
        try:
            self.log(f"{pcs} Processing {pdf_file}")
            if not self.check_and_create_lock_file(pdf_file):
                self.backup_file(pdf_file)
                for spit_pdf_file in self.split_pdf(pdf_file):
                    for split_image_file in self.convert_pdf_to_images(spit_pdf_file):
                        barcodes: list[Barcode] = self.check_barcode_on_image(split_image_file)
                        self.remove_file(split_image_file)
                        self.copy_file_as(
                            spit_pdf_file,
                            os.path.join(
                                self.output_dir,
                                f"{barcodes[0].barcode_data}.pdf" if barcodes else os.path.basename(spit_pdf_file) # pylint: disable = line-too-long
                            )
                        )
                        self.remove_file(spit_pdf_file)
                self.remove_file_and_lock_file(pdf_file)
        except Exception as error: #pylint: disable = broad-exception-caught
            self.log(f"Error processing {pdf_file}: {error}")

    def multi_process_file(self,
        pdf_file: str,
        i: int|None = None,
        length: int|None = None
    ) -> None:
        '''
            Process a single PDF file using multiprocessing

            Args:
                pdf (str): Path to the PDF file
        '''
        Process(target=self.process_file, args=(pdf_file, i, length)).start()

    def process_all(self) -> None:
        """
            Process the PDF files in the directory
        """
        files: list[str] = self.files_in_dir()
        for i, pdf in enumerate(files):
            self.process_file(
                pdf_file = pdf,
                i = i,
                length = len(files)
            )

    def wait_if_process_on_limit(self,
        processes: list[Process],
        max_processes: int
    ) -> None:
        '''
            Wait if the number of processes is greater than max_processes

            Parameters:
                processes (list[Process]): List of processes
                max_processes (int): Maximum number of processes
        '''
        wait: bool = True
        while len(processes) >= max_processes:
            if wait:
                self.log("Waiting for processes to finish")
                wait = False
            processes = self.remove_dead_processes_from_list(processes)
        return processes

    def remove_dead_processes_from_list(self,
        processes: list[Process]
    ) -> list[Process]:
        '''
            Remove dead processes from the list

            Parameters:
                processes (list[Process]): List of processes
        '''
        for process in processes:
            if not process.is_alive():
                processes.remove(process) #pylint: disable = modified-iterating-list
        return processes

    def multi_process_all(self,
        max_processes: int = 4
    ) -> None:
        '''
            Process the PDF files in the directory using multiprocessing
        '''
        files: list[str] = self.files_in_dir()
        processes: list[Process] = []
        if not isinstance(max_processes, int):
            raise PdfManagerException("max_processes should be an integer")
        if max_processes < 1:
            raise PdfManagerException("max_processes minimum value is 1, else it will make an infinite loop") # pylint: disable=line-too-long
        # looping pdf files
        self.log(f"Processing {len(files)} files using {max_processes} processes")
        # starting the multiprocessing
        freeze_support()
        for i, pdf in enumerate(files):
            # creating a process for each pdf file
            process: Process = Process(
                target = self.process_file,
                args = (pdf, i, len(files))
            )
            # adding the process to the list
            processes.append(process)
            # starting the process
            process.start()
            # wait if the number of processes is greater than max_processes
            self.wait_if_process_on_limit(
                processes = processes,
                max_processes = max_processes
            )
        for process in processes:
            process.join()
        self.log("All processes finished")
