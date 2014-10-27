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

    def test_random_card_no_set(self):
        c = dbaccess.get_random_card()

    def test_random_card_with_set(self):
        c = dbaccess.get_random_card('THS')
        self.assertEquals(c.card_set_id, 'THS')

    def test_specific_card(self):
        c = dbaccess.get_card(id=self.card_id)
        self.assertEquals(c.name, self.card_name)
        self.assertEquals(c.card_set_id, self.card_set_id)

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