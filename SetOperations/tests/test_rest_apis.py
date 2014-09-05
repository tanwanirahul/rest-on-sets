'''
Created on 04-Sep-2014

@author: rahul
'''
from tastypie.test import ResourceTestCase
from django.conf import settings
from SetOperations.core.datastore import InMemDataStore
from SetOperations.core.hset import HSet
from SetOperations.core.utils import get_unique_identifier
from tastypie.exceptions import NotFound


class BaseTestCase(ResourceTestCase):
    '''
        All the common functionality needed for creating our API test cases.
    '''
    def setUp(self):
        ResourceTestCase.setUp(self)
        self.client = self.api_client

    def get_full_uri(self, resource_name):
        '''
            Given the resource name, return the full uri.
        '''
        api_root = settings.API_ROOT
        api_version = settings.API_VERSION

        return "/{0}/{1}/{2}/".format(api_root, api_version, resource_name)

    def get(self, uri, format, **options):
        '''
            Makes a get call and returns the response.
        '''
        return self.client.get(uri, format)

    def get_json(self, uri, apply_assetions):
        '''
            Json specific GET implementation.
        '''
        response = self.get(uri, format="json")

        if apply_assetions:
            # Asset API returns 200 OK.
            self.assertHttpOK(response)
            self.assertValidJSONResponse(response)

        return response


class SetOperationsResourceTest(BaseTestCase):
    '''
        Tests set operations REST APIs.
    '''
    def setUp(self):
        BaseTestCase.setUp(self)
        self.resource_name = "sets"
        self.shapes, self.pocker = self._create_initial_sets()

    def tearDown(self):
        '''
            Destroy the initial sets.
        '''
        InMemDataStore.remove(self.shapes["_id"])
        InMemDataStore.remove(self.pocker["_id"])

    def test_get_list_of_sets(self):
        '''
            Tests the listing API /api/v1/sets returns the list of sets
            in the system.
        '''
        uri = self.get_full_uri(self.resource_name)
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self.assertEqual(2, response["meta"]["total_count"])

    def test_get_a_specific_set(self):
        '''
            Tests the details API /api/v1/sets/{id}
        '''
        uri = self.get_full_uri(self.resource_name) + self.pocker["_id"]
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self.assertEqual("pocker", response["title"])
        self.assertEqual(4, len(response["members"]))
        self._assert_list_equal(self.pocker.members.members, response["members"])  # @IgnorePep8

    def test_get_on_invalid_id_should_return_404(self):
        '''
            Tests the details API /api/v1/sets/{id}
        '''
        uri = self.get_full_uri(self.resource_name) + get_unique_identifier()
        with self.assertRaises(NotFound):
            self.get_json(uri, apply_assetions=False)

    def test_get_cardinality(self):
        '''
            Tests the get operation on cardinality.
            GET /api/v1/sets/{id}/cardinality
        '''
        uri = self.get_full_uri(self.resource_name) + self.pocker["_id"] + "/" + "cardinality"  # @IgnorePep8
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self.assertEqual(4, response["cardinality"])

    def test_shapes_union_pocker(self):
        '''
            Tests the API for union operation.
            GET /api/v1/sets/{shapes}/union/{pocker}.
        '''
        uri = self.get_full_uri(self.resource_name) + self.shapes["_id"] + "/" + "union/" + self.pocker["_id"]  # @IgnorePep8
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self._assert_list_equal(["circle", "diamond", "heart", "rectangle", "spade", "square", "turn"], response["members"])  # @IgnorePep8

    def test_shapes_intersect_pocker(self):
        '''
            Tests the API for intersect operation.
            GET /api/v1/sets/{shapes}/intersection/{pocker}.
        '''
        uri = self.get_full_uri(self.resource_name) + self.shapes["_id"] + "/" + "intersection/" + self.pocker["_id"]  # @IgnorePep8
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self._assert_list_equal(["diamond", "heart"], response["members"])  # @IgnorePep8

    def test_shapes_difference_pocker(self):
        '''
            Tests the API for difference operation.
            GET /api/v1/sets/{shapes}/union/{pocker}.
        '''
        uri = self.get_full_uri(self.resource_name) + self.shapes["_id"] + "/" + "difference/" + self.pocker["_id"]  # @IgnorePep8
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self._assert_list_equal(["circle", "rectangle", "square"], response["members"])  # @IgnorePep8

    def test_shapes_sdifference_pocker(self):
        '''
            Tests the API for union operation.
            GET /api/v1/sets/{shapes}/union/{pocker}.
        '''
        uri = self.get_full_uri(self.resource_name) + self.shapes["_id"] + "/" + "sdifference/" + self.pocker["_id"]  # @IgnorePep8
        response = self.get_json(uri, apply_assetions=True)
        response = self.deserialize(response)
        self._assert_list_equal(["circle", "rectangle", "spade", "square", "turn"], response["members"])  # @IgnorePep8

    def _create_initial_sets(self):
        '''
            Used as the fixtures for creating initial test data.
        '''
        shapes = InMemDataStore.save({"title": "shapes",
                                      "members": HSet(["circle", "square", "rectangle", "heart", "diamond"])})  # @IgnorePep8

        pocker = InMemDataStore.save({"title": "pocker",
                                      "members": HSet(["heart", "diamond", "spade", "turn"])})  # @IgnorePep8
        return shapes, pocker

    def _assert_list_equal(self, expected, actual):
        '''
            Compares if both the list have same elements without taking into
            account the ordering of the elements.
        '''
        self.assertListEqual(sorted(expected), sorted(actual))
