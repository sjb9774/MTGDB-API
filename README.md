MTGDB-API
==========
A python API for using the MtgDb.info database

## Get Started

The only requirement for this project is the requests module, pip install requests allows for easy installation. Click [here](http://docs.python-requests.org/en/latest/) for more information on requests.

With the requirements in place you can clone the repo and get started! mtgdb.api.dbaccess will be used for most of your basic needs and mtgdb.api.complexsearch should take care of the rest. Use shell.py for playing around and testing some of the functions.

## Short Example

You can get a lot of use out of this API if you know how to use nothing other than the complexsearch.Search class, so here's an example: Let's say we want to find all of the green enchantment-creatures from Theros with power less than 4
``` python
from api.complexsearch import Search

# this will be the search object that's gonna get all the love
s = Search()


s.color(equals='green').type(contains='enchant').type(contains='creature').setId(equals='THS').power(less_than=4)

# process() is important! Effectively crunches all the criteria we just specified into a query
s.process()

# search() returns special CardList item that behaves mostly like a list
resulting_card_list = s.search()

for card in resulting_card_list:
  print card
  
##########
# Output #
##########

# Nylea's Emmisary
# Leafcrown Dryad

# But that's not all...

for card in resulting_card_list:
  print card.card_set_name
  print card.power, '/', card.toughness
  print card.description
  print '------------'

##########
# Output #
##########

# Theros
# 3 / 3
# Bestow {5}{Green}(If you cast this card for its bestow cost, it's an Aura spell with enchant creature. It becomes a creature again if it's not attached to a creature.)
# Trample
# Enchanted creature gets +3/+3 and has trample.
# ------------
# Theros
# 2 / 2
# Bestow {3}{Green}(If you cast this card for its bestow cost, it's an Aura spell with enchant creature. It becomes # a creature again if it's not attached to a creature.)
# Reach
# Enchanted creature gets +2/+2 and has reach.
# ------------

```
