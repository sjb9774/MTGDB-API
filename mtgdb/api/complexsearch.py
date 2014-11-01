"""
This module introduces methods for dealing with complex searches of the database.
"""

import dbaccess
import requests
from api.models import Card, CardList
from config import MTG_DB_URL, SIMPLE_SEARCH_PATH
from mtgconsts import FIELDS

kw_map = { "contains" : "m",
           "equals" : "eq",
           "not_equals" : "not",
           "greater_than" : "gt",
           "greater_or_equals" : "gte",
           "less_than" : "lt",
           "less_or_equals" : "lte" }


class Search():
    """
    This class deals with the complex searches on the database. Initialize a search
    object and modify the parameters of your query simply, for example:

    s = Search()
    s.name(contains='Cloud')
    s.converted_mana_cost(equals=1)
    s.description(contains='evolve')

    s.process()
    s.search() # returns list containing a card object for Cloudfin Raptor
    """

    def __init__(self):
        """
        Creates a new Search object.
        """
        self.query_dict = {}
        self.count = False
        self.query = "?q="

        for field in FIELDS:
            self.query_dict[field] = {}
            for key in kw_map:
                self.query_dict[field][key] = []

        for field in FIELDS:
            # dynamically creates functions to deal with each field
            setattr(self, field, self._make_query_dict_modifier(field))

    def _make_query_dict_modifier(self, field):

        def fn(**kwargs):
            for key, value in kwargs.items():
                if key in kw_map:
                    self.query_dict[field][key].append(value)
                else:
                    raise Exception("{0} is not a valid keyword.".format(key))
            return self

        return fn

    def process(self):
        """
        Analyzes all parameters and criteria defined for the search and readies the
        query for searching against the database. Use this method to "apply" any changes
        to the a Search object before calling search().

        :returns: A reference to the Search object.
        """
        q = "?q="
        lst = []
        for field in self.query_dict:
            for keyword in self.query_dict[field]:
                for criteria in self.query_dict[field][keyword]:
                    lst.append("{0} {1} '{2}'".format(field, kw_map[keyword], criteria))

        q += " and ".join(lst)

        if self.count:
            q +="&count=True"
        self.query = q

        return self


    def search(self):
        """
        Submits the query to the database and returns the results of the search.

        :returns: A CardList containing the results of the search.
        """
        url = "{0}/{1}/{2}".format(MTG_DB_URL, SIMPLE_SEARCH_PATH, self.query)
        results = dbaccess._process_simple_request(url)
        cards = []
        for card_data in results:
            cards.append(Card(card_data))
        return CardList(cards)


    def __str__(self):
        return str(self.query)
