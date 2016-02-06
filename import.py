from __future__ import division

import sys

from config import *
from pymongo import MongoClient

catalog_file = 'catalog.txt'
messier_catalog = []
client = MongoClient(mongodb_url)
astronomydb = client.AstronomyCatalogs
messier_collection = astronomydb.Messier

# create a list of lists
with open(catalog_file, 'r') as catalog:
    messier_list = [messier_object.strip().split('\t') for messier_object in catalog]

# create a new list with dictionaries of each Messier object 
for messier_object in messier_list:
    new_messier_object = {'mid': messier_object[0],
                          'ngcid': messier_object[1],
                          'constellation': messier_object[2],
                          'loc': {
                              "type": "Point",
                              "coordinates": [int(messier_object[3]) / 100000, int(messier_object[4]) / 10000]
                          },
                          'remarks': messier_object[5],
                          }
    messier_catalog.append(new_messier_object)

del messier_list

# insert all objects into a mongodb collection
for messier_object in messier_catalog:
    # lookup the object first
    sys.stdout.write("Inserting %s with coordinates: %s %s " % (messier_object['mid'],
                                                                messier_object['loc']['coordinates'][0],
                                                                messier_object['loc']['coordinates'][1]))
    if not messier_collection.find_one({'mid': messier_object['mid']}):
        insert_result = messier_collection.insert_one(messier_object)
        insert_id = insert_result.inserted_id
        sys.stdout.write(str(insert_id) + " done.\n")
    else:
        sys.stdout.write("found \n")
