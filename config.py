'''This module handles the creation of necessary directories for the BarcodeScanSplit project.'''

import os

path: str = os.getcwd()

def make_dir(
    dir_path: str
) -> None:
    '''
        Create a directory if it does not exist

        Parameters:
            dir_path (str): Directory path
    '''
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def make_dir_return_path(
    dir_path: str
) -> str:
    '''
        Create a directory if it does not exist and return the path
    
        Parameters:
            dir_path (str): Directory path
    '''
    dir_path: str = os.path.join(path, dir_path)
    make_dir(dir_path)
    return dir_path

# Directories

# Log directory
LOG_DIR: str = "logs"
log_path: str = make_dir_return_path(LOG_DIR)

# Document directory
DOC_DIR: str = "docs"
doc_path: str = make_dir_return_path(DOC_DIR)

# Temp directory
TEMP_DIR: str = "temp"
temp_path: str = make_dir_return_path(TEMP_DIR)

# Image directory
IMG_DIR: str = "images"
img_path: str = make_dir_return_path(IMG_DIR)

# Output directory
OUTPUT_DIR: str = "out"
output_path: str = make_dir_return_path(OUTPUT_DIR)

# Backup directory
BACKUP_DIR: str = "backup"
backup_path: str = make_dir_return_path(BACKUP_DIR)

# Variables
default_max_processes: int = os.cpu_count() or 1

SINGLE_PROCESS_COMMANDS: list[str] = [
    "singleproccess",
    "single",
    "s",
    "sp",
    "sync"
]

MULTI_PROCESS_COMMANDS: list[str] = [
    "multiproccess",
    "multi",
    "m",
    "mp",
    "async"
]