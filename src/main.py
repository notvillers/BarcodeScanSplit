'''Running the splitter by argument'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import log_path, doc_path, temp_path, img_path, output_path, backup_path

def is_none(
    main_value: any,
    default_value: any
) -> any:
    '''
        If the main value is None, return the default value

        Parameters:
            main_value (any): Main value
            default_value (any): Default value
    '''
    return main_value if main_value else default_value

def run(
    pdf_dir: str|None = None,
    temp_dir: str|None = None,
    image_dir: str|None = None,
    output_dir: str|None = None,
    backup_dir: str|None = None,
    log_dir: str|None = None
) -> None:
    '''
        Main function for the splitter
    
        Parameters:
            pdf_dir (str|None): PDF directory
            temp_dir (str|None): Temporary directory
            image_dir (str|None): Image directory
            output_dir (str|None): Output directory
            backup_dir (str|None): Backup directory
            log_dir (str|None): Log directory
    '''
    PdfManager(
        pdf_dir = is_none(pdf_dir, doc_path),
        temp_dir = is_none(temp_dir, temp_path),
        image_dir = is_none(image_dir, img_path),
        output_dir = is_none(output_dir, output_path),
        backup_dir = is_none(backup_dir, backup_path),
        logger = Logger(
            file_path = os.path.join(
                is_none(log_dir, log_path),
                f"{date_string()}.log"
            )
        )
    ).process()
