MTGDB-API
==========
A python API for using the MtgDb.info database

## Get Started

The only requirement for this project is the requests module, pip install requests allows for easy installation. Click here for more information on requests.

With the requirements in place you can clone the repo and get started! mtgdb.api.dbaccess will be used for most of your basic needs and mtgdb.api.complexsearch should take care of the rest. Use shell.py for playing around and testing some of the functions.

## Short Example

You can get a lot of use out of this API if you know how to use nothing other than the complexsearch.Search class, so here's an example: Let's say we want to find all of the green enchantment-creatures from Theros with power less than 4
``` python
from api.complexsearch import Search

s = Search()  # this will be the search object that's gonna get all the love


s.color(equals='green').type(contains='enchant').type(contains='creature').setId(equals='THS').power(less_than=4)

s.process()  # This is important! Effectively crunches all the criteria we just specified into a query

resulting_card_list = s.search()  # special CardList item that behaves mostly like a list

for card in resulting_card_list:
  print card

##########
# Output #
##########

# Nylea's Emmisary
# Leafcrown Dryad
```
