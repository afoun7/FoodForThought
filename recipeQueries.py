# Amanda Foun

from __future__ import print_function
from flask import Flask, request
import os
import random
import sys
from pymongo import MongoClient, TEXT
import time
import re
import json
from bson.son import SON
from bson.json_util import dumps
#from util import #log

MONGO_DEFAULT_URL = 'mongodb://viral:ViralViral@ds011218.mongolab.com:11218/all_recipes'
MONGO_URL = os.environ.get('MONGO_URL')

if MONGO_URL is None:
    print("No MONGO_URL in environment. Defaulting to", MONGO_DEFAULT_URL, file=sys.stderr)
    MONGO_URL = MONGO_DEFAULT_URL

client = MongoClient(MONGO_URL)
db = client.get_default_database()
collection = db['recipes']

# searches in the title rank higher than matches in the body
# so we handle this by setting weights on the fields below
# collection.ensure_index([
#       ('title', 'text'),
#       ('description', 'text'),
#   ],
#   name="search_index",
#   weights={
#       'title':100,
#       'description':25
#   }
# )


def get_matches(query):
    '''Takes in the user's search box input and returns the
    matching results from the mongodb database'''
   # query = request.form['q']
    text_results = collection.find({"title": query})
    for doc in text_results:
        print ("in loop")
        print (doc)
        return doc["title"]
    #doc_matches = [res['obj'] for res in text_results['results']]
    # text_results = db.command('text', 'recipes', search=query, limit=2)
    # doc_matches = [res['obj'] for res in text_results['results']]

get_matches('apple')
