'''
Created on 01-Sep-2014

@author: Rahul

Description: Contains all the reusable utility functions (pure functions).
'''
from uuid import uuid4
from SetOperations.core.exceptions import DoesNotExist, NotAnHSet
from tastypie.exceptions import NotFound
from SetOperations.core.hset import HSet


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


def handle_does_not_exist(func):
    '''
        A decorator to wrap and handle Does Not Exist exception
    '''
    def wrapper(*args, **kwars):
        '''
            Wrapps the function call - func()
        '''
        try:
            return func(*args, **kwars)
        except DoesNotExist:
            raise NotFound("The requested resource does not exist")
    return wrapper


def type_check(func):
    '''
        A decorator to wrap and perform type check of HSet.
    '''
    def wrapper(*args, **kwars):
        '''
            Wrapps the function call - func()
        '''
        failed_types = [arg for arg in args if type(arg) not in (HSet,)]
        if failed_types:
            raise NotAnHSet("The arguments passed are not of a HSet type.")
        return func(*args, **kwars)
    return wrapper
