# The User class represents users
# The following methods are specified on the Flask documentation

from werkzeug.security import check_password_hash
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://viral:ViralViral@ds011271.mlab.com:11271/recipes_users')
users_db = mongo_client['recipes_users']
users_collection = users_db.users

class User():

    def __init__(self, username=None, email=None, password=None, active=True, id=None):
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.isAdmin = False
        self.id = None
        self.allergies = None
        self.restrictions = None
        self.zipcode = None
        self.time = None
        self.meal = None
        self.calendar = {}

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
            self.email = user['email']
            self.updateObject(user)
            return self
        else:
            return None

    def update(self, update_dict):
        # add data to the database
        users_collection.update({"_id":self.username},{"$set": update_dict})
        self.updateObject(update_dict)


    def updateObject(self, update_dict):
        # save data to this object
        if "allergies" in update_dict:
            self.allergies = update_dict["allergies"]
        if "restrictions" in update_dict:
            self.restrictions = update_dict["restrictions"]
        if "zipcode" in update_dict:
            self.zipcode = update_dict["zipcode"]
        if "time" in update_dict:
            self.time = update_dict["time"]
        if "meal" in update_dict:
            self.meal = update_dict["meal"]


    def save(self):
        try:
            users_collection.insert({"_id": self.username, "password": self.password, "email":self.email})
            return True
        except:
            return False

    def addToCalendar(self, date, recipe):
        # values are list of recipe ids
        if date not in self.calendar:
            self.calendar[date] = []
        self.calendar[date].push(recipe)


    # def validate_login(self, password):
    #     return check_password_hash(self.password, password)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

