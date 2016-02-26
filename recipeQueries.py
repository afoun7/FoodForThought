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
collection.ensure_index([
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

   #  text_results = collection.find({"$text": {"$search": query}})
   #  results = [doc["title"] for doc in text_results]
   #  print results
   #  return results

    text_results = collection.aggregate(
        [
            {"$match": {"$text": {"$search": query}}},
            {"$sort": {
                "ratingAverage": -1
            }},
            {"$limit": 5}
        ])
    results = [doc for doc in text_results]
    #print (results)
    return results

    #doc_matches = [res['obj'] for res in text_results['results']]
    # text_results = db.command('text', 'recipes', search=query, limit=2)
    # doc_matches = [res['obj'] for res in text_results['results']]


# FROM NEWS APP

def get_trends_for(category, disambiguations=None, limit=5):
    if not disambiguations:
        disambiguations = {}

    cursor = collection.aggregate(
        [
            {"$match": {"date_added": {"$gt": millis_since()}}},
            {"$project": {"entities": 1}},
            {"$unwind": "$entities"},
            {"$group": {
                "_id": {
                    "text": "$entities.text",
                    "type": "$entities.type"
                },
                "count": {"$sum": 1}
            }},
            {"$match": {"_id.type": category}},
            {"$sort": {"count": -1}},
            {"$limit": limit * 2}
        ]
    )
    count_dict = {}
    for obj in cursor:
        text = obj["_id"]["text"]
        count = obj["count"]
        if text in disambiguations:
            text = disambiguations[text]
        if text in count_dict:
            count_dict[text] += count
        else:
            count_dict[text] = count

    ret_val = [{
                   "text": key,
                   "count": value,
                   "media_item": get_random_media_for_entity(key),
                   "scenes": get_scenes_per_entity(key)
               } for key, value in count_dict.iteritems()]
    return sorted(ret_val, key=get_count, reverse=True)[0:limit]


def get_all_trends():
    return {
        "PEOPLE": get_trends_for("Person", {"OBAMA": "BARACK OBAMA", "PRESIDENT OBAMA": "BARACK OBAMA",
                                            "YOGI BERRA.": "YOGI BERRA"}),
        "COUNTRIES": get_trends_for("Country", {"US": "U.S.", "US.": "U.S."}),
        "ORGANIZATIONS": get_trends_for("Organization"),
        "COMPANIES": get_trends_for("Company"),
        "STATES": get_trends_for("StateOrCounty", {"WASHINGTON.": "WASHINGTON"}),
    }


def get_random_media_for_entity(entity):
    cursor = collection.find({"entities.text": entity, "date_added": {"$gt": millis_since()}},
                             {"media_url": 1, "thumbnail": 1}).limit(20)
    results = [obj for obj in cursor]
    if len(results) == 0:
        return None
    random_result = random.choice(results)
    random_result["_id"] = str(random_result["_id"])
    return random_result



def aggregate_scenes_for_trends():
    #log("unwinding subtitles and scenes")
    collection.aggregate(
        [
            {"$match": {
                "date_added": {"$gt": millis_since()}
            }},
            {"$project": {
                "media_url": 1,
                "closed_captions": 1,
                "scenes": 1
            }},
            {"$unwind": "$closed_captions"},
            {"$unwind": "$scenes"},
            {"$project": {
                "_id": 0,
                "media_url": 1,
                "closed_captions": 1,
                "scenes": 1,
                "start_cmp": {"$cmp": ['$closed_captions.start', '$scenes.begin']},
                "end_cmp": {"$cmp": ['$closed_captions.end', '$scenes.end']}
            }},
            {"$match": {
                "start_cmp": {"$gt": 0},
                "end_cmp": {"$lt": 0},
            }},
            {"$out": TRENDS_AGGREGATION_TEMP_COLLECTION_NAME}
        ]
    )
    #log("indexing subtitles and scenes")
    TRENDS_AGGREGATION_TEMP_COLLECTION.create_index([("closed_captions.text", TEXT)])


def get_scenes_per_entity(entity):
    #log("aggregating scenes for", entity)
    cursor = TRENDS_AGGREGATION_TEMP_COLLECTION.aggregate(
        [
            {"$match": {"$text": {"$search": entity}}},
            {"$project": {
                "_id": 1,
                "media_url": 1,
                "scenes": 1,
                "score": {"$meta": "textScore"}
            }},
            {"$group": {
                "_id": {
                    "media_url": "$media_url",
                    "scene_start": "$scenes.begin",
                    "scene_end": "$scenes.end",
                    "scene_length": {"$subtract": ["$scenes.end", "$scenes.begin"]},
                    "scene_thumbnail_url": "$scenes.thumbnail_url",
                },
                "score": {"$sum": "$score"},
            }},
            {"$match": {
                "_id.scene_length": {"$gt": MINIMAL_SCENE_LENGTH}
            }},
            {"$sort": {
                "score": -1
            }},
            {"$limit": 5}
        ]
    )
    return [{
                "media_url": obj["_id"]["media_url"],
                "start": obj["_id"]["scene_start"],
                "end": obj["_id"]["scene_end"],
                "length": obj["_id"]["scene_length"],
                "thumbnail": obj["_id"]["scene_thumbnail_url"] if "scene_thumbnail_url" in obj["_id"] else None,
                "score": obj["score"]
            } for obj in cursor]


def get_trends (time_window, trends_limit):
    cursor = collection.aggregate(
        [
            {"$match": {"date_added": {"$gt": millis_since(time_window)}}},
            {"$project": {"entities": 1}},
            {"$unwind": "$entities"},
            {"$group": {
                "_id":  "$entities.text",
                    #"type": "$entities.type"
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": trends_limit}
        ]
    )
    return {doc["_id"] : doc["count"] for doc in cursor}


def get_all_entities (time_window):
    print ("in get_all_entities")
    cursor = collection.aggregate(
        [
            {"$match": {"date_added": {"$gt": millis_since(time_window)}}},
            {"$project": {"entities": 1}},
            {"$unwind": "$entities"},
            {"$group": {
                "_id":  "$entities.text",
                    #"type": "$entities.type"
                "count": {"$sum": 1}
            }},
            {"$match":{"count":{"$gt":1}}},
            {"$sort": {"count": -1}}
        ]
    )

    result = {doc["_id"]: doc["count"] for doc in cursor}
    print (result)
    return result


# very slow method. run only once at beginning
def entities_per_scene(time_window):
    entities = get_all_entities(time_window)
    cursor = collection.find({"date_added": {"$gt": millis_since(time_window)}})
    result = []
    for video in cursor:
        if "scenes" in video and "closed_captions" in video:
            sorted_captions = sorted(video["closed_captions"], key=lambda x: x["start"])
            sorted_scenes = sorted(video["scenes"], key=lambda x:x["begin"])
            i=0
            for scene in sorted_scenes:
                scene_captions = []
                captions_string = ""
                while i < len(sorted_captions) and sorted_captions[i]["end"] < scene["end"]:
                    if sorted_captions[i]["start"] > scene["begin"]:
                        scene_captions.append(sorted_captions[i])
                        captions_string+=sorted_captions[i]["text"]
                    i += 1
                scene_entities = {}
                just_entities=[]
                for entity in entities:
                    count = len(re.findall(entity, captions_string))
                    if count > 0:
                        scene_entities[entity]=count
                        just_entities.append(entity)
                if len(scene_entities)>0:
                    result.append({
                        "media_url": video["media_url"],
                        "start":scene["begin"],
                        "end":scene["end"],
                        "length": scene["end"] - scene["begin"],
                        "thumbnail":scene["thumbnail_url"] if "thumbnail_url" in scene else None,
                        #"captions": obj["captions"],
                        "entities": scene_entities,
                        "entities_clean":just_entities
                    })
    with open('data.txt', 'w') as outfile:
        json.dump(result, outfile)
    return result

# if __name__ == '__main__':
    #     aggregate_scenes_for_trends()