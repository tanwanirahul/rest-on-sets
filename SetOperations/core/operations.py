'''
Created on 01-Sep-2014

@author: Rahul

Description: Defines all the supported set operations and implementations.
'''


def union(l_set, r_set):
    '''
        Returns the set of values which is union of both the input sets.
    '''
    pass


def intersect(l_set, r_set):
    '''
        Returns the set of values which is intersection of both the input sets.
    '''
    pass


def difference(l_set, r_set):
    '''
        Returns the set difference between l_set and r_set (l_Set - r_set).
        This will return all the members in l_set, but not in r_set.
    '''
    pass


def symm_difference(l_set, r_set):
    '''
        Returns the symmetric set difference between l_set and r_set.
        This will return all the members which are either in l_set or r_set,
        but not in both.
    '''
    pass


def perform_operation(operation_func, *args):
    '''
        Wrapper for performing any operation.
    '''
    return operation_func(*args)
