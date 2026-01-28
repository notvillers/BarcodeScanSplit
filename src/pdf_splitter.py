'''
    Pdf splitter module
'''

import os
from pypdf import PdfReader, PdfWriter
from villog import Logger

class PdfSplitter:
    '''
        Split a PDF file into individual pages
    '''
    __slots__: list[str] = ["pdf_path",
                            "output_dir",
                            "logger",
                            "output_files"]
    def __init__(self,
                 pdf_path: str,
                 output_dir: str,
                 logger: Logger | None = None) -> None:
        '''
            Splitter class

            :param pdf_path: :class:`str` File path
            :param output_path: :class:`str` Output path
            :param logger: :class:`Optional(Union(Logger, None))` Logger class, creates one if not provided. Defaults to `None`
        ''' # pylint: disable=line-too-long
        self.pdf_path: str = pdf_path
        self.output_dir: str = output_dir
        self.logger: Logger = logger or Logger(file_path = os.path.join(os.path.dirname(__file__),
                                                                        "log.log"))
        self.output_files: list[str] = []


    def log(self,
            content: str) -> None:
        '''
            Log content

            :param content: :class:`str` Content to log
        '''
        self.logger.log(content)


    def split(self):
        '''
            Split the PDF file into individual pages
        '''
        self.log(f"Splitting {self.pdf_path}")
        base_name: str = os.path.basename(self.pdf_path)
        try:
            with open(file = self.pdf_path,
                      mode = "rb") as pdf_file:
                reader: PdfReader = PdfReader(pdf_file)
                self.log(f"{self.pdf_path} is {str(len(reader.pages))} page{'s' if len(reader.pages) > 1 else ''}") # pylint: disable=line-too-long
                for page_number, _ in enumerate(reader.pages):
                    writer: PdfWriter = PdfWriter()
                    writer.add_page(reader.pages[page_number])
                    name_without_ext: str = base_name.replace(".pdf", "").replace(".PDF", "")
                    output_pdf_path: str = os.path.join(self.output_dir,
                                                        f"{name_without_ext}_{page_number}.pdf")
                    with open(file = output_pdf_path,
                              mode = "wb") as output_pdf:
                        writer.write(output_pdf)
                    self.log(f"Page {page_number + 1} saved to {output_pdf_path}")
                    self.output_files.append(output_pdf_path)
        except Exception as error: # pylint: disable=broad-exception-caught
            self.log(f"Error splitting {base_name}: {error}")
