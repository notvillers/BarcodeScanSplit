'''Running the splitter by argument'''

import os
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import (LOG_DIR, DOC_DIR, TEMP_DIR, IMG_DIR, OUTPUT_DIR, BACKUP_DIR,
                    default_max_processes,
                    SINGLE_PROCESS_COMMANDS, MULTI_PROCESS_COMMANDS,
                    make_dir_return_path)

def run(pdf_dir: str|None = None,
        temp_dir: str|None = None,
        image_dir: str|None = None,
        output_dir: str|None = None,
        backup_dir: str|None = None,
        log_dir: str|None = None,
        mode: str = "single",
        max_processes: int = default_max_processes) -> None:
    '''
        Main function for the splitter
    
        Args:
            pdf_dir (str|None): PDF directory
            temp_dir (str|None): Temporary directory
            image_dir (str|None): Image directory
            output_dir (str|None): Output directory
            backup_dir (str|None): Backup directory
            log_dir (str|None): Log directory
            mode (str): Mode of operation (single|multi)
            max_processes (int): Maximum number of processes to run 
    '''
    pdf_manager: PdfManager = PdfManager(pdf_dir = make_dir_return_path(pdf_dir or DOC_DIR),
                                         temp_dir = make_dir_return_path(temp_dir or TEMP_DIR),
                                         image_dir = make_dir_return_path(image_dir or IMG_DIR),
                                         output_dir = make_dir_return_path(output_dir or OUTPUT_DIR), # pylint: disable=line-too-long
                                         backup_dir = make_dir_return_path(backup_dir or BACKUP_DIR), # pylint: disable=line-too-long
                                         logger = Logger(file_path = os.path.join(make_dir_return_path(log_dir or LOG_DIR), # pylint: disable=line-too-long
                                                                                  f"{date_string()}.log"))) # pylint: disable=line-too-long
    mode = str(mode).lower()
    if mode.lower() in MULTI_PROCESS_COMMANDS:
        pdf_manager.log("Running in multi-process mode")
        if not isinstance(max_processes, int) or max_processes <= 1:
            pdf_manager.log(f"Invalid value for 'max_processes': {max_processes}, using default value: {default_max_processes} (no. of CPU threads)") # pylint: disable=line-too-long
            max_processes = default_max_processes
        pdf_manager.multi_process_all(max_processes = max_processes or default_max_processes)
    else:
        if mode.lower() not in SINGLE_PROCESS_COMMANDS and mode.lower() in MULTI_PROCESS_COMMANDS:
            pdf_manager.log(f"Unknown mode: '{mode}', anyway...")
        if max_processes:
            pdf_manager.log(f"Max processes is not used in single-process mode, ignoring value: {max_processes}") # pylint: disable=line-too-long
        pdf_manager.log("Running in single-process mode")
        pdf_manager.process_all()
