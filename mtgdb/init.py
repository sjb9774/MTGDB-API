from models.Card import Card
import requests


def __init__():
    req = requests.get( 'http://api.mtgdb.info/cards/20')
    c = Card(req.json())
    print c.name
    print c.cardSetName


if __name__ == "__main__":
    __init__()
