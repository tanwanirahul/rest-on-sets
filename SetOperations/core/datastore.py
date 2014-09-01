'''
Created on 01-Sep-2014

@author: rahul

Description: Holds the in memory data store implementation and infrastructure.
'''
from utils import get_unique_identifier


class InMemDataStore(object):
    '''
        Very minimal data store to hold set documents.
        Everything is in memory with no option (currently) for persistence.
    '''
    _data_store = {}
    _id_attribute = "_id"

    @classmethod
    def save(cls, doc):
        '''
            Saves the given data, adding the new _id field.
        '''
        _id, doc = cls._pre_process(doc)
        cls._data_store.update(doc)
        return _id

    @classmethod
    def find(cls, doc_id):
        '''
            Finds and returns the document based on the id.
        '''
        return cls._data_store.get(doc_id)

    @classmethod
    def find_all(cls):
        '''
            Returns all the set documents in the system.
        '''
        return cls._data_store.values()

    @classmethod
    def _pre_process(cls, doc):
        '''
        '''
        _id = get_unique_identifier()
        doc[cls._id_attribute] = _id
        return (_id, {_id: doc})
