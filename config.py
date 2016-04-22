from pymongo import MongoClient

WTF_CSRF_ENABLED = True # WTForms are a built in forms module under Flask
SECRET_KEY = '7\xde%\xeb\xc8\xf2-\xfaX\xe7vk1\xbdn\x02\xc7~\xceJ\xe8\x0c\xfe\xdc'
DB_NAME = 'test'

DATABASE = MongoClient()[DB_NAME]
POSTS_collection = DATABASE.posts
USERS_collection = DATABASE.users
SETTINGS_collection = DATABASE.settings

DEBUG = True