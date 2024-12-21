'''pdf splitter'''

import os
from pypdf import PdfReader, PdfWriter
from villog import Logger

class PdfSplitter:
    '''Split a PDF file into individual pages'''
    def __init__(self,
        pdf_path: str,
        output_dir: str,
        logger: Logger = None
    ) -> None:
        '''
            Splitter class

            Parameters:
                pdf_path (str): Path to the PDF file
                output_dir (str): Path to the output directory
                logger (Logger, optional): Logger object (creates one if not provided
        '''
        self.pdf_path: str = pdf_path
        self.output_dir: str = output_dir
        self.logger: Logger = logger if logger else Logger(
            file_path = os.path.dirname(__file__)
        )
        self.output_files: list[str] = []

    def __log(self,
        content: str
    ) -> None:
        '''
            Log content

            Parameters:
                content (str): Content to log
        '''
        self.logger.log(content)

    def split(self):
        '''Split the PDF file into individual pages'''
        self.__log(f"Splitting {self.pdf_path}")
        base_name: str = os.path.basename(self.pdf_path)
        try:
            with open(self.pdf_path, "rb") as pdf_file:
                reader = PdfReader(pdf_file)
                for page_number, _ in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_number])
                    name_without_ext: str = base_name.replace(".pdf", "").replace(".PDF", "")
                    output_pdf_path = os.path.join(
                        self.output_dir, 
                        f"{name_without_ext}_{page_number}.pdf"
                    )
                    with open(output_pdf_path, "wb") as output_pdf:
                        writer.write(output_pdf)
                    self.__log(f"Page {page_number + 1} saved to {output_pdf_path}")
                    self.output_files.append(output_pdf_path)
        except Exception as error: #pylint: disable=broad-exception-caught
            self.__log(f"Error splitting {base_name}: {error}")
