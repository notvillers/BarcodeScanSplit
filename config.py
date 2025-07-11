'''
    This module handles the creation of necessary directories for the BarcodeScanSplit project.
'''

import os

cwd_path: str = os.getcwd()

def make_dir(path: str) -> None:
    '''
        Create a directory if it does not exist

        :param path: :class:`str` Directory path
    '''
    if not os.path.exists(path):
        os.mkdir(path)

def make_dir_return_path(path: str) -> str:
    '''
        Create a directory if it does not exist and return the path

        :param path: :class:`str` Directory path
    '''
    dir_path: str = os.path.join(cwd_path,
                                 path)
    make_dir(dir_path)
    return dir_path

# Directories
# Log directory
LOG_DIR: str = "logs"

# Document directory
DOC_DIR: str = "docs"

# Temp directory
TEMP_DIR: str = "temp"

# Image directory
IMG_DIR: str = "images"

# Output directory
OUTPUT_DIR: str = "out"

# Backup directory
BACKUP_DIR: str = "backup"

# Variables
default_max_processes: int = os.cpu_count() or 1

SINGLE_PROCESS_COMMANDS: list[str] = ["singleproccess",
                                      "single",
                                      "s",
                                      "sp",
                                      "sync"]

MULTI_PROCESS_COMMANDS: list[str] = ["multiproccess",
                                     "multi",
                                     "m",
                                     "mp",
                                     "async"]
