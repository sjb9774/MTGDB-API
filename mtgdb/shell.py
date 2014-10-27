import os
import sys
os.environ['PYTHONINSPECT'] = 'True'
sys.dont_write_bytecode = True

from api import config, dbaccess, models
from api.config import MTG_DB_URL, CARDS_PATH, SETS_PATH
from api.models import Card, CardSet
import requests
import readline

def getCard(id):
    requested_card = requests.get(MTG_DB+str(id))
    if( requested_card.status_code != 200 ):
        print 'No card found with that id'
        return None
    card_json = requested_card.json()
    return Card(card_json)
