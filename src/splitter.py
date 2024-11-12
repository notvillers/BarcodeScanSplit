'''pdf splitter'''

import os
import PyPDF2
from villog import Logger

class Splitter:
    '''Split a PDF file into individual pages'''
    def __init__(self,
        pdf_path: str,
        output_dir: str,
        logger: Logger = None
    ) -> None:
        self.pdf_path: str = pdf_path
        self.output_dir: str = output_dir
        self.logger: Logger = logger if logger else Logger(
            file_path = os.path.dirname(__file__)
        )
        self.output_files: list[str] = []

    def __log(self, content) -> None:
        self.logger.log(content)

    def split(self):
        '''Split the PDF file into individual pages'''
        self.__log(f"Splitting {self.pdf_path}")
        base_name: str = os.path.basename(self.pdf_path)
        try:
            with open(self.pdf_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page_number, _ in enumerate(reader.pages):
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(reader.pages[page_number])
                    output_pdf_path = os.path.join(self.output_dir, f"{base_name}_{page_number}.pdf")
                    with open(output_pdf_path, "wb") as output_pdf:
                        writer.write(output_pdf)
                    self.__log(f"Page {page_number + 1} saved to {output_pdf_path}")
                    self.output_files.append(output_pdf_path)
        except Exception as error:
            self.__log(f"Error splitting {base_name}: {error}")