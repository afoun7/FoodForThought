# The User class represents users
# The following methods are specified on the Flask documentation

from werkzeug.security import check_password_hash

class User():

    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticated(self): # if provide valid credentials
        return True

    def is_active(self): # if account is activated
        return True

    def is_anonymous(self): # if this is an anonymous user
        return False

    def get_id(self): # returns a unicode that uniquely identifies the user
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)