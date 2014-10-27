SECURE_HTTP = False

MTG_DB_URL = 'http://api.mtgdb.info'
if SECURE_HTTP:
    MTG_DB_URL = 'https://api.mtgdb.info'
CARDS_PATH = 'cards'
SETS_PATH = 'sets'
RANDOM_CARD_PATH = 'random'
REG_IMAGE_URL = MTG_DB_URL + '/content/card_images'
HI_RES_IMAGE_URL = MTG_DB_URL + '/content/hi_res_card_images'
SIMPLE_SEARCH_PATH = 'search'
