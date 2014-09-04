'''
Created on 01-Sep-2014

@author: rahul

Description: Holds the in memory data store implementation and infrastructure.
'''
from utils import get_unique_identifier
from SetOperations.core.utils import ObjLikeDict
from SetOperations.core.exceptions import DoesNotExist


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
        return ObjLikeDict(doc[_id])

    @classmethod
    def find(cls, doc_id):
        '''
            Finds and returns the document based on the id.
        '''
        req_obj = cls._data_store.get(doc_id, None)
        if req_obj is None:
            raise DoesNotExist()
        return ObjLikeDict(req_obj)

    @classmethod
    def find_all(cls):
        '''
            Returns all the set documents in the system.
        '''
        return [ObjLikeDict(doc) for doc in cls._data_store.values()]

    @classmethod
    def remove(cls, doc_id):
        '''
            Removes the document with doc_id from the datastore.
        '''
        obj_deleted = cls._data_store.pop(doc_id, None)
        if obj_deleted is None:
            raise DoesNotExist()
        return ObjLikeDict(obj_deleted)

    # TODO: Make these operations generic with no assumptions for this app.
    @classmethod
    def add_members(cls, doc_id, members):
        '''
            Add members in the given document. This is getting specific to set
            operations..
        '''
        obj = cls.find(doc_id)
        obj.members.add_all(members)
        return obj

    # TODO: Make these operations generic with no assumptions for this app.
    @classmethod
    def remove_members(cls, doc_id, members):
        '''
            Add members in the given document. This is getting specific to set
            operations..
        '''
        obj = cls.find(doc_id)
        obj.members.remove_all(members)
        return obj

    @classmethod
    def _pre_process(cls, doc):
        '''
        '''
        _id = get_unique_identifier()
        doc[cls._id_attribute] = _id
        return (_id, {_id: doc})
