#!usr/bin/env python
import os
import sys
os.environ['PYTHONINSPECT'] = 'True'
sys.dont_write_bytecode = True

from api import config, dbaccess as db, models
from api.config import MTG_DB_URL, CARDS_PATH, SETS_PATH
from api.models import Card, CardSet
import requests
import readline
