'''
Created on 01-Sep-2014

@author: Rahul

Description: Holds the resource definitions and REST interface details.
'''
from django.conf.urls import url
from django.http.response import HttpResponse
from tastypie.bundle import Bundle
from tastypie.fields import CharField, ListField
from tastypie.http import HttpAccepted
from tastypie.resources import Resource
from tastypie.utils.mime import determine_format
from tastypie.utils.urls import trailing_slash

from SetOperations.core.hset import HSet
from SetOperations.core.operations import union, intersect, difference,\
    symm_difference
from SetOperations.core.utils import handle_does_not_exist


class SetOperationsResource(Resource):
    '''
        A standard REST based Resource that provides the basic infrastructure
        for creating REST APIs.
    '''
    title = CharField(attribute="title", null=False)
    id = CharField(attribute="_id", null=False)
    members = ListField(default=[])

    class Meta:
        resource_name = "sets"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "delete"]
        union_allowed_methods = ["get"]
        intersection_allowed_methods = ["get"]
        difference_allowed_methods = ["get"]
        sdifference_allowed_methods = ["get"]
        cardinality_allowed_methods = ["get"]
        members_allowed_methods = ["post", "delete"]
        detail_uri_name = "_id"

    def __init__(self, dao, api_name):
        '''
            Initialize.
        '''
        Resource.__init__(self, api_name=api_name)
        self.dao = dao

    def prepend_urls(self):
        '''
            Add our custom endpoints specific to set operations.
        '''
        return [
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>union)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_union"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>intersection)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_intersection"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>difference)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_difference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>sdifference)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_sdifference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<%s>[0-9a-f]{32})/(?P<operation>cardinality)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_sdifference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<%s>[0-9a-f]{32})/(?P<operation>members)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_members"),  # @IgnorePep8
        ]

    def dispatch_set_operation(self, request, **kwargs):
        '''
            Dispatches API calls for all custom set operations.
        '''
        return self.dispatch(kwargs["operation"], request, **kwargs)

    @handle_does_not_exist
    def get_union(self, request, l_set_id, r_set_id, **kwargs):
        '''
            Handles the GET call for set union operation.
        '''
        union_set = union(self.dao.find(l_set_id).members, self.dao.find(r_set_id).members)  # @IgnorePep8
        return self.create_response(request, {"members": union_set.members})

    @handle_does_not_exist
    def get_intersection(self, request, l_set_id, r_set_id, **kwargs):
        '''
            Handles the GET call for set intersection operation.
        '''
        res_set = intersect(self.dao.find(l_set_id).members, self.dao.find(r_set_id).members)  # @IgnorePep8
        return self.create_response(request, {"members": res_set.members})

    @handle_does_not_exist
    def get_difference(self, request, l_set_id, r_set_id, **kwargs):
        '''
            Handles the GET call for set difference operation.
        '''
        res_set = difference(self.dao.find(l_set_id).members, self.dao.find(r_set_id).members)  # @IgnorePep8
        return self.create_response(request, {"members": res_set.members})

    @handle_does_not_exist
    def get_sdifference(self, request, l_set_id, r_set_id, **kwargs):
        '''
            Handles the GET call for set symmetric difference operation.
        '''
        res_set = symm_difference(self.dao.find(l_set_id).members, self.dao.find(r_set_id).members)  # @IgnorePep8
        return self.create_response(request, {"members": res_set.members})

    @handle_does_not_exist
    def get_cardinality(self, request, **kwargs):
        '''
            Handles the GET call for set cardinality operation.
        '''
        cardinality = self.dao.find(kwargs[self._meta.detail_uri_name]).members.cardinality  # @IgnorePep8
        return self.create_response(request, {"cardinality": cardinality})

    @handle_does_not_exist
    def post_members(self, request, **kwargs):
        '''
            Handles the POST call for adding members into the set.
        '''
        deserialized = self.deserialize_data(request)

        obj = self.dao.add_members(kwargs[self._meta.detail_uri_name], deserialized.get("members", []))  # @IgnorePep8
        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        return self.create_response(request, data=bundle, response_class=HttpAccepted)  # @IgnorePep8

    @handle_does_not_exist
    def delete_members(self, request, **kwargs):
        '''
            Handles the DELETE call for removing members from the set.
        '''
        deserialized = self.deserialize_data(request)

        obj = self.dao.remove_members(kwargs[self._meta.detail_uri_name], deserialized.get("members", []))  # @IgnorePep8
        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        return self.create_response(request, data=bundle, response_class=HttpAccepted)  # @IgnorePep8

    def obj_get_list(self, bundle, **kwargs):
        '''
            Handles the GET call on Sets list API /Sets.
        '''
        return self.dao.find_all()

    @handle_does_not_exist
    def obj_get(self, bundle, **kwargs):
        '''
            Handles GET call on /sets/id details API to get the specific set.
        '''
        bundle.obj = self.dao.find(kwargs[self._meta.detail_uri_name])
        return bundle.obj

    def obj_create(self, bundle, **kwargs):
        '''
            Handles the POST call on /sets to create a new set.
        '''
        bundle.obj = self.dao.save(bundle.data)
        bundle = self.full_hydrate(bundle)
        return bundle

    @handle_does_not_exist
    def obj_delete(self, bundle, **kwargs):
        '''
            Deletes the specific set object.
        '''
        self.dao.remove(kwargs[self._meta.detail_uri_name])

    def hydrate_members(self, bundle):
        '''
            A Tastypie lifecycle method for maintaining list of objects as set.
        '''
        bundle.data['members'] = HSet(bundle.data['members'])
        return bundle

    def dehydrate_members(self, bundle):
        '''
            A Tastypie lifecycle method for maintaining list of objects as set.
        '''
        return bundle.obj.members.members

    def _prepare_response(self, request, data, response_class=HttpResponse):
        '''
            Wraps the data into bundle (Tastypie's packaging format).
        '''
        bundle = self.build_bundle(data=data, request=request)
        return self.create_response(request, bundle, response_class)

    def determine_format(self, request):
        '''
            Overriding this to by pass text/html format when accessing ``API
            directly through browser.
        '''
        req_format = determine_format(request, self._meta.serializer,
                                      default_format=self._meta.default_format)
        if req_format == "text/html":
            req_format = self._meta.default_format

        return req_format

    def deserialize_data(self, request):
        '''
            Deserialize the data from the POST request to valid python object.
        '''
        return Resource.deserialize(self, request, request.body,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))  # @IgnorePep8

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.
        """
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj.obj, self._meta.detail_uri_name)  # @IgnorePep8
        else:
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj, self._meta.detail_uri_name)  # @IgnorePep8

        return kwargs
