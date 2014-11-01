"""
This is the main module for accessing the MTGDB.info database. In most cases,
all calls to find a card or set of cards should go through this module.
"""

from models import Card, CardSet
from config import MTG_DB_URL, CARDS_PATH, SETS_PATH, RANDOM_CARD_PATH, \
                   SIMPLE_SEARCH_PATH
from util import _process_simple_request
import requests

def get_card(id=None, name=None, fields=None):
    """
    Retrieves a card from the database using a name or card id. If both name
    and id are provided, only the id will be used. If neither id nor name are
    provided this function will return a random card.

    :param name: Optional. Specifies the name of the card to retrieve.
    :param id: Optional. Specifies the id of the card to retrieve.
    :param fields: Optional. Specifies what fields to populate for the returned
                   card object (defaults to all).
    :returns: A Card object.
    """
    card_url = "{0}/{1}/{2}"

    if fields:
        fields = 'fields={0}'.format(','.join(fields))

    results = None

    if id:
        results = _process_simple_request(card_url.format(MTG_DB_URL,
                                          CARDS_PATH,
                                          id),
                                          error_msg="No card found by that id.",
                                          payload=fields)
    elif name:
        results = _process_simple_request(card_url.format(MTG_DB_URL,
                                          CARDS_PATH,
                                          clean_card_name(name)),
                                          error_msg="No card found by that name.",
                                          payload=fields)[0]
    else:
        return get_random_card(fields=fields)

    return Card(results)

def get_random_card(set=None, fields=None):
    """
    Retrieves a random card from the MTGDB.info database and returns it.

    :param set: Optional. Specifies a set from which to retrieve a random card.
    :param fields: Optional. Specifies what fields to populate for the returned
                   card object (defaults to all).
    :returns: A Card object.
    """
    results = None

    if fields:
        fields = {'fields': fields}

    if(set):
        req_url = '{0}/{1}/{2}/{3}/{4}'.format(MTG_DB_URL,
                                        SETS_PATH,
                                        set,
                                        CARDS_PATH,
                                        RANDOM_CARD_PATH)
        results = _process_simple_request(req_url,
                                          error_msg='There was a problem finding a random\
                                                    card.Please ensure card set {0} \
                                                    exists'.format(set),
                                          payload=fields)

    else:
        req_url = '{0}/{1}/{2}'.format(MTG_DB_URL, CARDS_PATH, RANDOM_CARD_PATH)
        results = _process_simple_request(req_url,
                                          error_msg='There was a problem finding a random \
                                                     card',
                                          payload=fields)

    return Card(results)

def get_card_set(set_id, create_cards=False):
    """
    Retrieves a CardSet object from the database, holds information about the card set
    as well as a reference to all cards contained in the set by id in card_set.card_ids.
    If create_cards is passed as True, the returned CardSet will also contain a list of
    all the Card objects in card_set.cards.

    :param set_id: The string id of the set to be retrieved (ie 'THS', 'RTR', 'BNG')
    :param create_cards: Boolean flag to determine whether or not to build a Card object
                         for each card in the set and store in card_set.cards
    :returns: A CardSet object.
    """
    req_url = '{0}/{1}/{2}'.format(MTG_DB_URL, SETS_PATH, set_id)
    card_set = CardSet(_process_simple_request(req_url))

    if create_cards:
        build_cards_in_card_set(card_set)

    return card_set

def simple_search(card_name, start=0, limit=0):
    """
    Will return a list of Cards retrieved from the database using a rough match of
    card_name as the only criteria.

    :param card_name: Cards with this string in their name will be returned.
    :param start: Optional. Only return Cards starting with the start-th found Card.
    :param limit: Optional. Return no more than this many cards. Returns all if 0.
    :returns: A list of Card objects.
    """
    req_url = '{0}/{1}'.format(MTG_DB_URL, SIMPLE_SEARCH_PATH)
    cleaned_name = clean_card_name(card_name).replace(' ', '')
    payload = {'start':start, 'limit':limit}
    req_url += '/{0}'.format(cleaned_name)
    results = _process_simple_request(req_url,
                                      error_msg='There was a problem with the search.',
                                      payload=payload)
    card_results = []
    for card_json in results:
        card_results.append(Card(card_json))
    return card_results


def clean_card_name(s):
    """
    Removes characters from a card name that can't be used in a request to
    the MTGDB.info database.

    :param s: The string to be cleaned.
    :returns: A safe string that can be used in a request.
    """
    return s.replace(':', '').replace('/', '')

def populate_fields_from_db(card):
    """
    Loads all attributes for a Card object to the passed Card object. This method is
    useful for building a SINGLE card at a time from a CardSet that was retreived with
    build_cards=False. If needing to build all the cards at once, use the much faster
    build_cards_in_set() function. For building an arbitrary list of cards, pass the list
    to get_card_list().

    :param card: The Card object to populate.
    """
    results = None
    if card.id:
        req_url = '{0}/{1}/{2}'.format(MTG_DB_URL, CARDS_PATH, card.id)
        results = _process_simple_request(req_url, error_msg='No card by that id')
        for attribute_name in results:
            setattr( card, attribute_name, results[attribute_name])
    elif card.name:
        req_url = '{0}/{1}/{2}'.format(MTG_DB_URL, CARDS_PATH, clean_card_name(card.name))
        results = _process_simple_request(req_url, error_msg='No card by that name')
        for attribute_name in results:
            setattr( card, attribute_name, results[attribute_name])
    else:
        raise Exception('No identifying attributes in Card object')

def build_cards_in_card_set(card_set):
    """
    """
    cards = get_card_list(card_set.card_ids)

    card_set.cards = cards

def get_card_list(card_list):
    """
    """
    req_url = '{0}/{1}/{2}'.format(MTG_DB_URL, CARDS_PATH, ','.join(str(id) for id in card_list))
    results = _process_simple_request(req_url,
                                      error_msg='There was a problem building the \
                                                card list. Ensure the list contains \
                                                only valid card ids.')
    cards = []
    for card_data in results:
        cards.append(Card(card_data))

    return cards
