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
    return str(uuid4().hex)


class ObjLikeDict(dict):
    '''
        Extends the standard dictionary to work like an object by supporting
        dot notation attribute lookup.
    '''

    def __getattr__(self, name):
        '''
            Gets called when the attribute lookup is unsuccessful.
        '''
        return self.__getitem__(name)
