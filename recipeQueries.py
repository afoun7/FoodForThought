# Amanda Foun

from __future__ import print_function
from flask import Flask, request
import os
import random
import math
import sys
from pymongo import MongoClient, TEXT
import time
import re
import json
from bson.son import SON
from bson.json_util import dumps
#from util import #log

MONGO_URL = 'mongodb://viral:ViralViral@ds011218.mlab.com:11218/all_recipes'

client = MongoClient(MONGO_URL)
db = client.all_recipes
recipes_collection = db['recipes']
ingredients_collection = db['ingredients']

# searches in the title rank higher than matches in the body
# so we handle this by setting weights on the fields below

#recipes_collection.ensure_index([
ingredients_collection.ensure_index([
      ('title', 'text')
  ],
  name="search_index",
  weights={
      'title':100,
      'description':25
  }
)


def get_matches(query, allergies):
    '''Takes in the user's search box input and returns the
    matching results from the mongodb database. Does not return
    any recipes that the user is allergic to.'''

    text_results = recipes_collection.aggregate(
        [
            {"$match": {"$text": {"$search": query}}},
            {"$sort": {
                "ratingAverage": -1
            }},
            {"$limit": 5}
            
        ])
    results = []
    returned_docs = text_results

   # if ("result") in text_results:
    #  returned_docs = text_results["result"]

    for doc in returned_docs:
      allergic = False
      for ingred in (doc["ingredients"]): # doc["ingredients"] is a list of dictionaries
          if allergic == False: 
            ingred_cursor = ingredients_collection.find({"_id":ingred["ingredientID"]})
            for ing in ingred_cursor:
                if allergic == True:
                  break
                else:
                  for allergy in allergies:
                    if allergy.lower() in ing["name"].lower():
                      print (allergy)
                      print (ing["name"])
                      allergic = True
                      break 
          else: # allergic == True
            break # move onto next recipe 
      if allergic == False:
          results.append(doc)
    return results

def get_recipe(recipe_id):
  result = recipes_collection.find_one({"_id": int(recipe_id)})
  return result

