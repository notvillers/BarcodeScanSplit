'''
    Running the splitter by argument
'''

import os
from dataclasses import dataclass
from villog import Logger
from src.slave import date_string
from src.manager import PdfManager
from config import (LOG_DIR, DOC_DIR, TEMP_DIR, IMG_DIR, OUTPUT_DIR, BACKUP_DIR,
                    default_max_processes,
                    SINGLE_PROCESS_COMMANDS, MULTI_PROCESS_COMMANDS,
                    make_dir_return_path)

@dataclass(slots = False)
class PathConfig:
    '''
        `PathConfig` class
    '''
    source: str | None = None
    destination: str | None = None
    temp: str | None = None
    image: str | None = None
    backup: str | None = None
    log: str | None = None


def run(path_config: PathConfig | None = None,
        mode: str = "single",
        max_processes: int = default_max_processes,
        ocr_prefixes: str | None = None,
        ratio: float | None = None) -> None:
    '''
        Main function for the splitter
    
        :param path_config: :class:`Optional(Union(PathConfig, None))` Defaults to `None`
        :param mode: :class:`Optional(str)` Mode of operation. Defaults to `"single"`. Options: `"single"`, `"multi"`
        :param max_processes: :class:`Optional(int)` Maximum number of processes to run. Defaults to `default_max_processes`
        :param ocr_prefixes: :class:`Optional(Union(str, None))` defaults to `None`
        :param ratio: :class:`Optional(Union(float, None))` defaults to `None`
    ''' # pylint: disable=line-too-long
    path_config = path_config or PathConfig()
    ocr_prefix_list: list[str] | None = None if not ocr_prefixes or not isinstance(ocr_prefixes, str) else ocr_prefixes.strip().replace(" ", "").split(",")
    pdf_manager: PdfManager = PdfManager(pdf_dir = make_dir_return_path(path_config.source or DOC_DIR),
                                         temp_dir = make_dir_return_path(path_config.temp or TEMP_DIR),
                                         image_dir = make_dir_return_path(path_config.image or IMG_DIR),
                                         output_dir = make_dir_return_path(path_config.destination or OUTPUT_DIR), # pylint: disable=line-too-long
                                         backup_dir = make_dir_return_path(path_config.backup or BACKUP_DIR), # pylint: disable=line-too-long
                                         ocr_prefixes = ocr_prefix_list,
                                         ratio = ratio,
                                         logger = Logger(file_path = os.path.join(make_dir_return_path(path_config.log or LOG_DIR), # pylint: disable=line-too-long
                                                                                  f"{date_string()}.log"))) # pylint: disable=line-too-long
    mode = str(mode).lower()
    if mode in MULTI_PROCESS_COMMANDS:
        pdf_manager.log("Running in multi-process mode")
        if not isinstance(max_processes, int) or max_processes <= 1:
            if max_processes is None:
                pdf_manager.log(f"'max_processes' not given, using default value: {default_max_processes}")
            else:
                pdf_manager.log(f"Invalid value for 'max_processes': {max_processes}, using default value: {default_max_processes} (no. of CPU threads)") # pylint: disable=line-too-long
            max_processes: int = default_max_processes
        pdf_manager.multi_process_all(max_processes = max_processes or default_max_processes)
    else:
        if mode.lower() not in SINGLE_PROCESS_COMMANDS and mode.lower() in MULTI_PROCESS_COMMANDS:
            pdf_manager.log(f"Unknown mode: '{mode}', anyway...")
        if max_processes:
            pdf_manager.log(f"Max processes is not used in single-process mode, ignoring value: {max_processes}") # pylint: disable=line-too-long
        pdf_manager.log("Running in single-process mode")
        pdf_manager.process_all()
    pdf_manager.log("PDF splitter finished")
