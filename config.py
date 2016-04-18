from pymongo import MongoClient

WTF_CSRF_ENABLED = True # WTForms are a built in forms module under Flask
SECRET_KEY = '7\xde%\xeb\xc8\xf2-\xfaX\xe7vk1\xbdn\x02\xc7~\xceJ\xe8\x0c\xfe\xdc'
DB_NAME = 'recipes_users'

client = MongoClient('mongodb://viral:ViralViral@ds011271.mlab.com:11271/recipes_users')
DATABASE = client[DB_NAME]
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True