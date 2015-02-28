from api.complexsearch import Search
import unittest

class TestComplexSearch(unittest.TestCase):

    def setUp(self):
        self.search = Search()

    def test_query_holds(self):
        self.search.name(contains='David')
        self.assertEquals(self.search.search_criteria.filter_dict['name']['contains'][0], 'David')

    def test_removal_of_duplicate_search_terms(self):
        s = Search()
        s.name(contains='Thassa').convertedmanacost(less_than=5).type(contains='Enchantment')
        q = s.process().search_criteria.query
        s.name(contains='Thassa').type(contains='Enchantment').process()

        self.assertEquals(s.search_criteria.query, q)
