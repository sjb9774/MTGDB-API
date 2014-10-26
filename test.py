import requests

BASE_URL = 'http://api.mtgdb.info/'

def __init__():
    inp = raw_input("Need a card?\n\t")
    req_params = "cards/{0}".format(inp)
    req = requests.get(BASE_URL + req_params)
    print req.json()['name']


if __name__ == "__main__":
    __init__()
