'''Running the splitter by argument'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import (
    LOG_DIR, DOC_DIR, TEMP_DIR, IMG_DIR, OUTPUT_DIR, BACKUP_DIR, 
    default_max_processes,
    SINGLE_PROCESS_COMMANDS, MULTI_PROCESS_COMMANDS,
    make_dir_return_path
)

def is_none(
    main_value: any,
    default_value: any
) -> any:
    '''
        If the main value is None, return the default value (and create the directory if needed)

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
        pdf_dir = make_dir_return_path(is_none(pdf_dir, DOC_DIR)),
        temp_dir = make_dir_return_path(is_none(temp_dir, TEMP_DIR)),
        image_dir = make_dir_return_path(is_none(image_dir, IMG_DIR)),
        output_dir = make_dir_return_path(is_none(output_dir, OUTPUT_DIR)),
        backup_dir = make_dir_return_path(is_none(backup_dir, BACKUP_DIR)),
        logger = Logger(
            file_path = os.path.join(
                make_dir_return_path(is_none(log_dir, LOG_DIR)),
                f"{date_string()}.log"
            )
        )
    )
    mode = str(mode).lower()
    if mode in MULTI_PROCESS_COMMANDS:
        pdf_manager.log("Running in multi-process mode")
        if not isinstance(max_processes, int) or max_processes < 1:
            pdf_manager.log(f"Invalid value for 'max_processes': {max_processes}, using default value: {default_max_processes} (no. of CPU threads)") # pylint: disable=line-too-long
            max_processes = default_max_processes
        pdf_manager.multi_process_all(
            max_processes = is_none(max_processes, default_max_processes)
        )
    else:
        if mode not in SINGLE_PROCESS_COMMANDS:
            pdf_manager.log(f"Unknown mode: '{mode}', anyway...")
        if max_processes:
            pdf_manager.log(f"Max processes is not used in single-process mode, ignoring value: {max_processes}") # pylint: disable=line-too-long
        pdf_manager.log("Running in single-process mode")
        pdf_manager.process_all()
