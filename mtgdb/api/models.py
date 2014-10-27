"""
This module contains models used to represent Magic: The Gathering resources. This module is
intended to be used internally and its methods should not be called and objects not instantiated
outside of the API.
"""

from config import REG_IMAGE_URL, HI_RES_IMAGE_URL

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
            setattr(self, _pylike_property_name(attribute), attr_dict[attribute])

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


def _pylike_property_name(s):
    """
    This function is used to translate a camel-case property name to an all lowercase
    python-style name separated by underscores instead.

    :param s: A camelCase string
    :returns: A lowercase underscore separated string
              (ie exampleAttrName -> example_attr_name)
    """
    new_name = ''
    for char in s:
        if not char.isdigit() and char.upper() == char:  # character is uppercase
            new_name += '_{0}'.format(char.lower())
        else:
            new_name += char
    return new_name
