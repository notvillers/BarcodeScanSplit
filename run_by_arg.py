'''Running the splitter by argument'''

import os
import argparse
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import log_path, doc_path, temp_path, img_path, output_path, backup_path

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog = "PDF Splitter",
    description = "Split PDF files into individual pages, by reading the barcode on each page"
)

arg_list: list[list[any]] = [
    ["-s", "--source", str, "Directory containing PDF files"],
    ["-d", "--destination", str, "Directory to store output files"],
    ["-b", "--backup", str, "Directory to store backup files"],
    ["-l", "--log", str, "Directory to store log files"],
    ["-t", "--temp", str, "Temporary directory to store split PDF files"],
    ["-i", "--image", str, "Temporary directory to store the images"]
]

for arg in arg_list:
    parser.add_argument(arg[0], arg[1], type = arg[2], help = arg[3])

args = parser.parse_args()

def is_none(main_value: any, default_value: any) -> any:
    '''
        If the main value is None, return the default value

        Parameters:
            main_value (any): Main value
            default_value (any): Default value
    '''
    return main_value if main_value is None else default_value

def run() -> None:
    '''Main function'''
    PdfManager(
        pdf_dir = is_none(args.source, doc_path),
        temp_dir = is_none(args.temp, temp_path),
        image_dir = is_none(args.image, img_path),
        output_dir = is_none(args.destination, output_path),
        backup_dir = is_none(args.backup, backup_path),
        logger = Logger(
            file_path = os.path.join(
                is_none(args.log, log_path),
                f"{date_string()}.log"
            )
        )
    ).process()


if __name__ == '__main__':
    run()
