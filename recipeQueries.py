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


def get_matches(query):
    '''Takes in the user's search box input and returns the
    matching results from the mongodb database'''
   # query = request.form['q']

   #  text_results = recipes_collection.find({"$text": {"$search": query}})
   #  results = [doc["title"] for doc in text_results]
   #  print results
   #  return results
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

    # Amanda commented the following two lines. It was not
    # yielding any search results when these two lines were included.
    # Unsure why this is.
   # if ("result") in text_results:
    #  returned_docs = text_results["result"]

    for doc in returned_docs:
    # for doc in text_results:
      results.append(doc)
    return results

def get_recipe(recipe_id):
  result = recipes_collection.find_one({"_id": int(recipe_id)})
  return result

