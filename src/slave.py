'''
    slave
'''

from datetime import datetime

def date_string() -> str:
    '''
        Return the current date as a string
    '''
    return datetime.now().strftime("%Y-%m-%d")
