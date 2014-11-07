#!/usr/bin/env python
import os
import sys
os.environ['PYTHONINSPECT'] = 'True'
sys.dont_write_bytecode = True

from api import config, dbaccess as db, models
from api.complexsearch import *
from api.config import MTG_DB_URL, CARDS_PATH, SETS_PATH
from api.models import Card, CardSet, CardList
import requests
import readline

s = Search()

card = None

def get(id=None, name=None):
    global card
    if id:
        card = db.get_card(id=id)
    elif name:
        card = db.get_card(name=name)
    else:
        print 'Need a name or id...'
