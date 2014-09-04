from django.conf import settings
from django.conf.urls import patterns, include
from tastypie.api import Api

from SetOperations.core.resources import SetOperationsResource
from SetOperations.core.datastore import InMemDataStore

api_v1 = Api(api_name=settings.API_VERSION)
api_v1.register(SetOperationsResource(InMemDataStore, settings.API_VERSION))

urlpatterns = patterns('',
                       (r'^api/', include(api_v1.urls)),
                       )
