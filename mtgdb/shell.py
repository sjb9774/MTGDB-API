from api.models import Card, CardSet
import requests
from init import MTG_DB
import os
import readline

os.environ['PYTHONINSPECT'] = 'True'

def getCard(id):
    requested_card = requests.get(MTG_DB+str(id))
    if( requested_card.status_code != 200 ):
        print 'No card found with that id'
        return None
    card_json = requested_card.json()
    return Card(card_json)
