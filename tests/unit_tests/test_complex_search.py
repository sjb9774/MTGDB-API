from api.complexsearch import Search
import unittest

class TestComplexSearch(unittest.TestCase):

    def setUp(self):
        self.search = Search()

    def test_query_holds(self):
        self.search.name(contains='David')
        self.assertEquals(self.search.query_dict['name']['contains'][0], 'David')
