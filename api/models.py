"""
This module contains models used to represent Magic: The Gathering resources. This module is
intended to be used internally and its methods should not be called and objects not instantiated
outside of the API.
"""

from config import REG_IMAGE_URL, HI_RES_IMAGE_URL
from util import _pythonic_property_name

class MtgDbObject(object):
    """
    Base object for the models in the API.
    """

    def __init__(self, attr_dict):
        """
        Expects a dictionary of a specific format. Do not attempt to pass an arbitrary dictionary,
        or other methods will not work as expected.
        """
        for attribute in attr_dict:
            setattr(self, _pythonic_property_name(attribute), attr_dict[attribute])

        self.json_data = attr_dict


class Card(MtgDbObject):
    """
    Represents a single Magic: The Gathering card
    """

    def __init__(self, card_attr_dict=None, id=None, name=None):
        """
        Expects a dictionary of a specific format. Do not attempt to pass an arbitrary dictionary,
        or other methods will not work as expected.
        """
        if id:
            self.id = id
        elif name:
            self.name = name
        else:
            super(Card, self).__init__(card_attr_dict)
            self._toss_bad_attributes()


    def _toss_bad_attributes(self):
        if not "creature" in self.type.lower():
            if hasattr(self, 'power'):
                del self.power
            if hasattr(self, 'toughness'):
                del self.toughness
            self.json_data.pop('power', 0)
            self.json_data.pop('toughness', 0)

    def get_image(self, hiRes=False):
        """
        Returns a url to an image of the card.

        :param hiRes: Indicates whether the images is high-resolution or not
        :returns: url .jpeg image
        """

        image_url = REG_IMAGE_URL
        ext = 'jpeg'

        if( hiRes ):
            image_url = HI_RES_IMAGE_URL
            ext = 'jpg'

        return "{0}/{1}.{2}".format(image_url, self.id, ext)

    def get_legality(self, format=None):
        """
        Returns whether the card is legal in a specified format. If no format
        is passed it returns a dictionary with strings of format-names
        mapped to string elements of legality values.

        :param format: String specifying a format.
        :returns: String specifying 'Legal', 'Restricted', 'Banned', etc.
        """
        if not format:
            return self.formats

        for legality_format_dict in self.formats:
            if(legality_format_dict['name'].lower() == format.lower()):
                return legality_format_dict['legality']
        return u'Legal'  # assume unspecified is legal

    def is_legal(self, format):
        """
        A convenience method for determining if a card is legal in a certain format. Any legality
        other than fully Legal (ie Restricted, Banned) will evaluate to False
        :returns: Whether the card is fully legal in a given format
        """
        return self.get_legality(format) == 'Legal'

    def __str__(self):
        return self.name

    def __repr__(self):
        showable_items = [ "name", "mana_cost", "card_set_id", "type", "description", "power", "toughness" ]
        showable_items_in_card = []

        for item in showable_items:
            if hasattr(self, item):
                showable_items_in_card.append(item)

        s = ""
        for item in showable_items_in_card:
            s += item + ":\t" + str(getattr(self, item)) + "\n"

        return s


class CardSet(MtgDbObject):
    """
    Represents a card set from Magic: The Gathering. If the card objects have been built
    they will be contained in card_set.cards, otherwise the ids of the cards in the set
    are found in card_set.card_ids
    """

    def __init__(self, card_set_attr_dict):
        """
        Expects a dictionary of a specific format. Do not attempt to pass an arbitrary dictionary,
        or other methods will not work as expected.
        """
        super(CardSet, self).__init__(card_set_attr_dict)
        self.cards = []

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.card_ids)

class CardList():
    """
    Represents an arbitrary list of Magic: The Gathering cards and provides a number
    of convenience functions for dealing with them.
    """

    def __init__(self, cards):
        """
        Expects a list containing only lists and Card objects. Any nested lists will be
        recursively traversed so the CardList will hold all cards.

        :param cards: A list of Card objects.
        """
        self.cards = []
        self.append(cards)

    def append(self, cards):
        """
        Recursively appends a list of Card objects to the CardList.

        :param cards: A list of Card objects.
        """
        if( type(cards) == list ):
            for card in cards:
                self.append(card)
        else:
            self.cards.append(cards)

    def remove_reprints(self, prefer_sets=None):
        """
        Removes all versions of each card except one from the CardList. There is no
        guarantee which version will be kept.
        """
        new_cards = []

        if prefer_sets:
            added = []
            for card in self.cards:
                # reprints all have the same name, self[card.name] returns all cards by
                # that name so we only check one of any given name
                if card.name in added:
                    continue
                else:
                    added.append(card.name)

                cards_of_this_name = self[card.name]

                cards_from_prefer_sets = []
                for c in cards_of_this_name:
                    if c.card_set_id in prefer_sets:
                        cards_from_prefer_sets.append(c)

                if len(cards_from_prefer_sets) == 0:
                    new_cards.append(cards_of_this_name[0])
                else:
                    for card in cards_from_prefer_sets:
                        new_cards.append(card)

        else:
            added = {}
            for card in self.cards:
                if card.name in added:
                    continue
                else:
                    new_cards.append(card)
                    added[card.name] = len(new_cards) - 1

        self.cards = new_cards

    def copy(self):
        copy_cards = []
        for card in self.cards:
            copy_cards.append(Card(card.json_data))

        return CardList(copy_cards)

    def __getitem__(self, i):
        if type(i) == int:
            return self.cards[i]

        c = None
        for card in self.cards:
            if card.name == i:
                if c:
                    c.append(card)
                else:
                    c = [card]
        return c

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        s = ""
        for x in range(len(self) - 1):
            s += str(self[x]) + "\n"
        s += str(self[-1])
        return s
