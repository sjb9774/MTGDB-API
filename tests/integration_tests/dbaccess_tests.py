"""
Integration tests
"""

from api import dbaccess
import unittest

class TestDbCardMethods(unittest.TestCase):
    """
    """

    def setUp(self):
        # test specific card properties
        self.card_id = 50
        self.card_name = 'Black Knight'
        self.card_set_id = 'LEA'

        self.dirty_card_name = 'Turn // Burn'

    def test_random_card_no_set(self):
        c = dbaccess.get_random_card()

    def test_random_card_with_set(self):
        c = dbaccess.get_random_card('THS')
        self.assertEquals(c.card_set_id, 'THS')

    def test_specific_card(self):
        c = dbaccess.get_card(id=self.card_id)
        self.assertEquals(c.name, self.card_name)
        self.assertEquals(c.card_set_id, self.card_set_id)

    def test_specific_dirty_card(self):
        c = dbaccess.get_card(name=self.dirty_card_name)
        self.assertEquals(c.name, self.dirty_card_name)

    def test_populate_fields(self):
        c = dbaccess.get_card(id=self.card_id)
        c.name = ''
        dbaccess.populate_fields_from_db(c)
        self.assertEquals(c.name, self.card_name)


class TestDbCardSetMethods(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def test_get_card_set_no_build(self):
        cs = dbaccess.get_card_set('GTC', False)
        self.assertEquals(cs.name, 'Gatecrash')

    def test_get_card_set_with_build(self):
        cs = dbaccess.get_card_set('GTC', True)
        correct_set = True
        for card in cs.cards:
            if(card.card_set_id != 'GTC'):
                correct_set = False
                break
        self.assertTrue(correct_set)

class TestDbSimpleSearch(unittest.TestCase):
    """
    """

    def setUp(self):
        self.search_name_single = 'bidentofthassa'
        self.search_name_multi = 'staffofthe'

    def test_search_single(self):
        results = dbaccess.simple_search(self.search_name_single)
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].name, 'Bident of Thassa')

    def test_search_multi(self):
        results = dbaccess.simple_search(self.search_name_multi, limit=5)
        self.assertTrue(len(results) == 5 )
