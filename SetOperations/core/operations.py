'''
Created on 01-Sep-2014

@author: Rahul

Description: Defines all the supported set operations and implementations.
'''
from SetOperations.core.hset import HSet


def _remove(super_set, sub_set):
    '''
        Removes all the elements of sub_set from super set.
    '''
    super_set.remove_all(sub_set)
    return super_set


def union(l_set, r_set):
    '''
        Returns the set of values which is union of both the input sets.
    '''
    result_set = HSet(l_set)
    result_set.add_all(r_set)
    return result_set


def intersect(l_set, r_set):
    '''
        Returns the set of values which is intersection of both the input sets.
    '''
    # Take the smaller set and find what all elements does exist in other set.
    s_set, o_set = (l_set, r_set) if l_set.cardinality < r_set.cardinality else (r_set, l_set)  # @IgnorePep8
    return HSet([element for element in s_set if element in o_set])


def difference(l_set, r_set):
    '''
        Returns the set difference between l_set and r_set (l_Set - r_set).
        This will return all the members in l_set, but not in r_set.
    '''
    return _remove(l_set, intersect(l_set, r_set))


def symm_difference(l_set, r_set):
    '''
        Returns the symmetric set difference between l_set and r_set.
        This will return all the members which are either in l_set or r_set,
        but not in both.
    '''
    return _remove(union(l_set, r_set), intersect(l_set, r_set))


def is_member(hset, element):
    '''
        Checks and returns if the element is the member of the given set.
    '''
    return hset.contains(element)


def perform_operation(operation_func, *args):
    '''
        Wrapper for performing any operation.
    '''
    return operation_func(*args)
