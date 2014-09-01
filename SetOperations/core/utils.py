'''
Created on 01-Sep-2014

@author: Rahul

Description: Contains all the reusable utility functions (pure functions).
'''
from uuid import uuid4


def get_unique_identifier():
    '''
        Returns the new unique identifier - uuid.
    '''
    return str(uuid4())
