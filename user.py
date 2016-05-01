# The User class represents users
# The following methods are specified on the Flask documentation

from werkzeug.security import check_password_hash
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://viral:ViralViral@ds011271.mlab.com:11271/recipes_users')
users_db = mongo_client['recipes_users']
users_collection = users_db.users

class User():

    # def __init__(self, id):
    #     self.username = id

    def __init__(self, email=None, password=None, active=True, id=None):
        self.email = email
        self.password = password
        self.active = active
        self.isAdmin = False
        self.id = None
        self.allergies = None

    def is_authenticated(self): # if provide valid credentials
        return True

    def is_active(self): # if account is activated
        return True

    def is_anonymous(self): # if this is an anonymous user
        return False

    def get_id(self): # returns a unicode that uniquely identifies the user
        return self.username

    def get(self, id):
        user = users_collection.find_one({"_id": id})
        if user:
            self.username = user['_id']
            self.password = user['password']
            #self.email = user['email']
            return self
        else:
            return None


    # def validate_login(self, password):
    #     return check_password_hash(self.password, password)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)