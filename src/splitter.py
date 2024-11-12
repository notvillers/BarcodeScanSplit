'''pdf splitter'''

import os
import PyPDF2
from villog import Logger

class Splitter:
    '''Split a PDF file into individual pages'''
    def __init__(self,
        input_pdf_path: str,
        output_folder: str,
        logger: Logger = None,
        do_log: bool = True
    ) -> None:
        self.input_pdf_path: str = input_pdf_path
        self.output_folder: str = output_folder
        self.pages: int = 0
        self.logger: Logger = logger if logger else Logger(
            file_path = os.path.dirname(__file__)
        )
        self.do_log: bool = do_log
        self.output_files: list[str] = []

    def __log(self, content) -> None:
        if self.do_log:
            self.logger.log(content)

    def split(self, base_name: str = None) -> list[str]:
        '''Split the PDF file into individual pages'''
        base_name: str = base_name if base_name else os.path.basename(self.input_pdf_path)
        self.__log(f"Splitting {base_name} into individual pages")
        base_name = base_name[:-4] if base_name.lower().endswith(".pdf") else base_name
        with open(self.input_pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_number, _ in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_number])
                output_pdf_path = os.path.join(self.output_folder, f"{base_name}_{page_number}.pdf")
                with open(output_pdf_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                self.__log(f"Page {page_number + 1} saved to {output_pdf_path}")
                self.output_files.append(output_pdf_path)
                self.pages += 1
        return self.output_files

class DirSplitter:
    '''Split multiple PDF files into individual pages'''
    __EXTENSION: str = ".pdf"

    def __init__(self,
        input_folder: str,
        output_folder: str,
        logger: Logger = None,
        do_log: bool = True
    ) -> None:
        self.input_folder: str = input_folder
        self.output_folder: str = output_folder
        self.__logger: Logger = logger if logger else Logger(
            file_path = os.path.dirname(__file__)
        )
        self.do_log: bool = do_log
        self.output_paths: list[dict] = []

    def __files_in_folder(self) -> list[str]:
        '''Return a list of files in a folder'''
        files_in_dir: list[str] = []
        for file in os.listdir(self.input_folder):
            if file.lower().endswith(self.__EXTENSION):
                files_in_dir.append(os.path.join(self.input_folder, file))
        self.files = files_in_dir
        return files_in_dir

    def split(self) -> None:
        '''Split the PDF files into individual pages'''
        files: list[str] = self.__files_in_folder()
        for file in files:
            try:
                output_file: list[str] = Splitter(
                    input_pdf_path = file,
                    output_folder = self.output_folder,
                    logger = self.__logger,
                    do_log = self.do_log
                ).split()
                self.output_paths.append(
                    {file: output_file}
                )
            except Exception as error:
                self.__logger.log(f"Error splitting {file}: {error}")