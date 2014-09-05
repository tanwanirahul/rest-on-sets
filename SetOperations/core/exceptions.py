'''
Created on 01-Sep-2014

@author: Rahul

Description: Home for all the custom implemented exceptions.
'''


class DoesNotExist(Exception):
    '''
        Raised when we try to access a resource that does not exist
    '''

    def __init__(self, *args, **kwargs):
        '''
            Initialize.
        '''
        Exception.__init__(self, *args, **kwargs)


class NotAnHSet(Exception):
    '''
        Raised when we try to perform a set operation on Data Structure
        which is not a set (HSet).
    '''

    def __init__(self, *args, **kwargs):
        '''
            Initialize.
        '''
        Exception.__init__(self, *args, **kwargs)
