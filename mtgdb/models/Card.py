REG_IMAGE_URL = 'http://api.mtgdb.info/content/card_images/{0}.jpeg'
HI_RES_IMAGE_URL = 'http://api.mtgdb.info/content/hi_res_card_images/{0}.jpg'

class Card(object):

    def __init__(self, card_attr_dict):
        for attribute in card_attr_dict:
            setattr(self, attribute, card_attr_dict[attribute])

    def getImage(self, hiRes=False):
        image_url = REG_IMAGE_URL

        if( hiRes ):
            image_url = HI_RES_IMAGE_URL

        return image_url.format(self.id)

    def legalityIn(self, format):
        for legality_format_dict in self.formats:
            if(legality_format_dict['name'] == format):
                return legality_format_dict['legality']
        return u'Legal'  # assume unspecified is legal
