"""
These are technically integration tests, they are included with the unit tests right now
for quick development purposes
"""

from api import dbaccess
import unittest

class TestDbAccessMethods(unittest.TestCase):
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
