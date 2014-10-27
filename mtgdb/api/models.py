"""
This module contains models used to represent Magic: The Gathering resources. This module is
intended to be used internally and its methods should not be called and objects not instantiated
outside of the API.
"""

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
            setattr(self, pylike_property_name(attribute), attr_dict[attribute])


class Card(MtgDbObject):
    """
    Represents a single Magic: The Gathering card
    """

    REG_IMAGE_URL = 'http://api.mtgdb.info/content/card_images/'
    HI_RES_IMAGE_URL = 'http://api.mtgdb.info/content/hi_res_card_images/'

    def __init__(self, card_attr_dict):
        """
        Expects a dictionary of a specific format. Do not attempt to pass an arbitrary dictionary,
        or other methods will not work as expected.
        """
        super(Card, self).__init__(card_attr_dict)

    def get_image(self, hiRes=False):
        """
        Returns a url to an image of the card.

        :param hiRes: Indicates whether the images is high-resolution or not
        :returns: url .jpeg image
        """

        image_url = REG_IMAGE_URL

        if( hiRes ):
            image_url = HI_RES_IMAGE_URL

        return "{0}{1}.jpeg".format(image_url, self.id)

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
        return get_legality(format) == 'Legal'


class CardSet(MtgDbObject):
    """
    Represents a set of Card objects
    """

    def __init__(self, card_set_attr_dict):
        """
        Expects a dictionary of a specific format. Do not attempt to pass an arbitrary dictionary,
        or other methods will not work as expected.
        """
        super(CardSet, self).__init__(card_set_attr_dict)

def pylike_property_name(s):
    """
    """
    new_name = ''
    for char in s:
        if(char.upper() == char):  # character is uppercase
            new_name += '_{0}'.format(char.lower())
        else:
            new_name += char
    return new_name
