# -*- coding: utf-8 -*-
import json
from api.models import Card

import unittest

class TestCardMethods(unittest.TestCase):

    def setUp(self):
        card_data = '''{"id":366443,"relatedCardId":0,"setNumber":230,"name":"Gruul Keyrune","searchName":"gruulkeyrune","description":"{Tap}: Add {Red} or {Green} to your mana pool.\n{Red}{Green}: Gruul Keyrune becomes a 3/2 red and green Beast artifact creature with trample until end of turn.","flavor":" As perilous and unpredictable as the wilds themselves.","colors":["None"],"manaCost":"3","convertedManaCost":3,"cardSetName":"Gatecrash","type":"Artifact","subType":null,"power":0,"toughness":0,"loyalty":0,"rarity":"Uncommon","artist":"Daniel Ljunggren","cardSetId":"GTC","token":false,"promo":false,"rulings":[{"releasedAt":"2013-04-15","rule":"Until the ability that turns the Keyrune into a creature resolves, the Keyrune is colorless."},{"releasedAt":"2013-04-15","rule":"Activating the ability that turns the Keyrune into a creature while it's already a creature will override any effects that set its power and/or toughness to another number, but effects that modify power and/or toughness without directly setting them will still apply."}],"formats":[{"name":"Standard","legality":"Legal"},{"name":"Modern","legality":"Legal"},{"name":"Extended","legality":"Legal"},{"name":"Return to Ravnica Block","legality":"Legal"},{"name":"Legacy","legality":"Legal"},{"name":"Vintage","legality":"Legal"},{"name":"Freeform","legality":"Legal"},{"name":"Prismatic","legality":"Legal"},{"name":"Tribal Wars Legacy","legality":"Legal"},{"name":"Tribal Wars Standard","legality":"Legal"},{"name":"Classic","legality":"Legal"},{"name":"Singleton 100","legality":"Legal"},{"name":"Commander","legality":"Legal"}],"releasedAt":"2013-02-01"}'''
        cleaned_card_data= card_data.replace('\n','\\n').replace('\r', '\\r')

        self.test_card = Card(json.loads(cleaned_card_data))

    def test_get_legality(self):
        self.assertEquals(self.test_card.get_legality('Standard'),
                          'Legal')

    def test_is_legal(self):
        self.assertTrue(self.test_card.is_legal('Modern'))

    def test_reg_image_url(self):
        self.assertEquals(self.test_card.get_image(False),
                          'http://api.mtgdb.info/content/card_images/366443.jpeg')

    def test_hi_res_image_url(self):
        self.assertEquals(self.test_card.get_image(True),
                         'http://api.mtgdb.info/content/hi_res_card_images/366443.jpg')

    def test_attributes(self):
        self.assertEquals(self.test_card.related_card_id, 0)
        self.assertEquals(self.test_card.set_number, 230)
        self.assertEquals(self.test_card.search_name, 'gruulkeyrune')
