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

    def __init__(self, args):
        '''
            Initialize / Implement the hash table from the passed initial
            sequence of values.
        '''
        self._hset_table = {}
        self.add_all(args)

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
        self._hset_table.update({self._get_hash(element): element})
        return element

    def add_all(self, elements):
        '''
            Given the sequence of elements, add them all into the set.
        '''
        return [self.add(element) for element in elements]

    def remove(self, element):
        '''
            Removes element from the set.
        '''
        return self._hset_table.pop(self._get_hash(element), {})

    def remove_all(self, elements):
        '''
            Removes all the elements from the set.
        '''
        return [self.remove(element) for element in elements]

    def contains(self, element):
        '''
            Returns if the elements is part of the set.
        '''
        return self._get_hash(element) in self._hset_table

    def _get_hash(self, element):
        '''
            Returns the hash for the given element.
        '''
        return element.__hash__()

    def __iter__(self):
        '''
            A simple generator based iterator. Trying to be lazy here.
        '''
        for element in self.get_all():
            yield element

    def __contains__(self, element):
        '''
            A magic method that gets called for in operator.
            Provides easy to use and intuitive symantics for checking
            membership. for ex: if element in hset
        '''
        return self.contains(element)
