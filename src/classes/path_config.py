'''
    Config class
'''
import os
from dataclasses import dataclass, fields
from config import SOURCE_DIR, DESTINATION_DIR, TEMP_DIR, IMG_DIR, LOG_DIR

@dataclass(slots = False)
class PathConfig:
    '''
        `PathConfig` class
    '''
    source: str = SOURCE_DIR
    destination: str = DESTINATION_DIR
    temp: str = TEMP_DIR
    image: str = IMG_DIR
    backup: str | None = None
    log: str = LOG_DIR

    def __post_init__(self) -> None:
        '''
            Check path fields 
        '''
        for field in fields(self):
            f_path: str = getattr(self,
                                  field.name)
            if isinstance(f_path,
                          str):
                if not os.path.exists(f_path):
                    os.makedirs(f_path,
                                exist_ok = True)
