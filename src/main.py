'''Running the splitter by argument'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import (
    log_path, doc_path, temp_path, img_path, output_path, backup_path, default_max_processes,
    SINGLE_PROCESS_COMMANDS, MULTI_PROCESS_COMMANDS
)

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
    log_dir: str|None = None,
    mode: str = "single",
    max_processes: int = 4
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
            mode (str): Mode of operation (single|multi)
            max_processes (int): Maximum number of processes to run 
    '''
    pdf_manager: PdfManager = PdfManager(
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
    )
    if mode.lower() in MULTI_PROCESS_COMMANDS:
        pdf_manager.log("Running in multi-process mode")
        if not isinstance(max_processes, int) or max_processes < 1:
            pdf_manager.log(f"Invalid value for 'max_processes': {max_processes}, using default value: {default_max_processes}") # pylint: disable=line-too-long
            max_processes = default_max_processes
        pdf_manager.multi_process_all(
            max_processes = is_none(max_processes, default_max_processes)
        )
    else:
        if mode.lower() not in SINGLE_PROCESS_COMMANDS:
            pdf_manager.log(f"Unknown mode: '{mode}', anyway...")
        if max_processes:
            pdf_manager.log(f"Max processes is not used in single-process mode, ignoring value: {max_processes}") # pylint: disable=line-too-long
        pdf_manager.log("Running in single-process mode")
        pdf_manager.process_all()
