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
LOG_DIR: str = "logs"
''' Directory for the log files '''

SOURCE_DIR: str = "source"
''' Directory to the source files '''

TEMP_DIR: str = "temp"
''' Directory for the temp files '''

IMG_DIR: str = "images"
''' Directory for the created `temp` images '''

DESTINATION_DIR: str = "destination"
''' Directory for the output files '''

BACKUP_DIR: str = "backup"
''' Directory to backup files '''

default_max_processes: int = os.cpu_count() or 1
''' Allowed default max processes to run in `multiprocess`/`multi` mode '''

SINGLE_PROCESS_COMMANDS: list[str] = ["singleproccess",
                                      "single",
                                      "s",
                                      "sp",
                                      "sync"]
''' Synonym(s) for `singleprocess` command '''

MULTI_PROCESS_COMMANDS: list[str] = ["multiproccess",
                                     "multi",
                                     "m",
                                     "mp",
                                     "async"]
''' Synonym(s) for `multiprocess` command '''
