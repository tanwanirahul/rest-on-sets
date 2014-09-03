'''
Created on 01-Sep-2014

@author: Rahul

Description: Holds the resource definitions and REST interface details.
'''
from tastypie.resources import Resource
from tastypie.fields import CharField, ListField
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from django.http.response import HttpResponse
from tastypie.utils.mime import determine_format


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

    def __init__(self, dao, api_name):
        '''
            Initialize.
        '''
        Resource.__init__(self, api_name=api_name)
        self._meta.dao = dao

    def prepend_urls(self):
        '''
            Add our custom endpoints specific to set operations.
        '''
        return [
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>union)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_union"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>intersection)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_intersection"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>difference)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_difference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>sdifference)/(?P<r_set_id>[0-9a-f]{32})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_sdifference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>cardinality)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_sdifference"),  # @IgnorePep8
            url(r"^(?P<resource_name>%s)/(?P<l_set_id>[0-9a-f]{32})/(?P<operation>members)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_set_operation'), name="api_dispatch_members"),  # @IgnorePep8
        ]

    def dispatch_set_operation(self, request, **kwargs):
        '''
            Dispatches API calls for all custom set operations.
        '''
        return self.dispatch(kwargs["operation"], request, **kwargs)

    def get_union(self, request, **kwargs):
        '''
            Handles the GET call for set union operation.
        '''
        return self.create_response(request, {"members": []})

    def get_intersection(self, request, **kwargs):
        '''
            Handles the GET call for set intersection operation.
        '''
        return self.create_response(request, {"members": []})

    def get_difference(self, request, **kwargs):
        '''
            Handles the GET call for set difference operation.
        '''
        return self.create_response(request, {"members": []})

    def get_sdifference(self, request, **kwargs):
        '''
            Handles the GET call for set symmetric difference operation.
        '''
        return self.create_response(request, {"members": []})

    def get_cardinality(self, request, **kwargs):
        '''
            Handles the GET call for set cardinality operation.
        '''
        return self.create_response(request, {"cardinality": 0})

    def post_members(self, request, **kwargs):
        '''
            Handles the POST call for adding members into the set.
        '''
        pass

    def delete_members(self, request, **kwargs):
        '''
            Handles the DELETE call for removing members from the set.
        '''
        pass

    def obj_get_list(self, bundle, **kwargs):
        '''
            Handles the GET call on Sets list API /Sets.
        '''
        pass

    def obj_get(self, bundle, **kwargs):
        '''
            Handles GET call on /sets/id details API to get the specific set.
        '''
        pass

    def obj_create(self, bundle, **kwargs):
        '''
            Handles the POST call on /sets to create a new set.
        '''
        pass

    def obj_delete(self, bundle, **kwargs):
        '''
            Deletes the specific set object.
        '''
        pass

    def _prepare_response(self, request, data, response_class=HttpResponse):
        '''
            Wraps the data into bundle (Tastypie's packaging format).
        '''
        bundle = self.build_bundle(data=data, request=request)
        return self.create_response(request, bundle, response_class)

    def determine_format(self, request):
        '''
            Overriding this to by pass text/html format when accessing API
            directly through browser.
        '''
        req_format = determine_format(request, self._meta.serializer,
                                      default_format=self._meta.default_format)
        if req_format == "text/html":
            req_format = self._meta.default_format

        return req_format
