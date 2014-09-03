from django.conf import settings
from django.conf.urls import patterns, include
from tastypie.api import Api

from SetOperations.core.resources import SetOperationsResource
api_v1 = Api(api_name=settings.API_VERSION)
api_v1.register(SetOperationsResource(settings.API_VERSION, None))

urlpatterns = patterns('',
                       (r'^api/', include(api_v1.urls)),
                       )
