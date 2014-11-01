import unittest
from api.complexsearch import Search

class TestComplexSearching(unittest.TestCase):

    def setUp(self):
        self.search = Search()

    def test_request(self):
        self.search.name(contains='Cloud').description(contains='Flying') \
                   .type(contains='Creature').power(less_than=3, greater_or_equals=0 )

        self.search.process()
        cards = self.search.search()
        cloudfin = None
        
        for card in cards:
            if(card.name == "Cloudfin Raptor"):
                cloudfin = card
        self.assertFalse(cloudfin == None)
