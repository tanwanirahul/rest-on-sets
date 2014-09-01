'''
Created on 01-Sep-2014

@author: Rahul

Description: Our implementation of hash based Set implementation.
'''


class HSet(object):
    '''
        Encapsulates our hash based Set implementation.
        Uses hash table (dict) for maintaining uniqueness and faster lookups.
    '''

    def __init__(self, *args):
        '''
            Initialize / Implement the hash table from the passed initial
            sequence of values.
        '''
        self._hset_table = {}

    @property
    def members(self):
        '''
            Returns all members in the set.
        '''
        return self.get_all()

    @property
    def cardinality(self):
        '''
            Returns the cardinality for the set.
        '''
        return self.size()

    def size(self):
        '''
            Returns the number of elements in the set.
        '''
        return len(self._hset_table)

    def get_all(self):
        '''
            Returns all the members in the set.
        '''
        return self._hset_table.values()

    def add(self, element):
        '''
            Adds new element in the set.
        '''
        pass

    def add_all(self, elements):
        '''
            Given the sequence of elements, add them all into the set.
        '''
        pass

    def remove(self, element):
        '''
            Removes element from the set.
        '''
        pass

    def remove_all(self, elements):
        '''
            Removes all the elements from the set.
        '''
        pass

    def is_member(self, element):
        '''
            Returns if the elements is part of the set.
        '''
        pass

    def strip(self, elements):
        '''
            Preserves only the given in the set.
        '''
        pass
