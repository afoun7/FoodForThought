# Amanda Foun

from flask import Flask, render_template, request, jsonify, redirect, flash, session, g
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, url_for
from forms import LoginForm  
from user import User
from flask.ext.wtf import Form 
from functools import wraps 
from wtforms import StringField, PasswordField, Form, BooleanField, TextField, validators
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import recipeQueries
import sys
import operator
import json

app = Flask(__name__) # create instance of Flask class
# app.config.from_object(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)


# LOGIN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_collection'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data): # ensure that user exists
        	user_obj = User(user['_id'])
        	login_user(user_obj)
        	flash("Logged in successfully!", category='success')
        	return redirect(url_for("search")) 
        flash("Wrong username or password!", category='error') # could not find in database
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login')) # go back to login page


@login_manager.user_loader # user_loader callback is used to reload the user object from the user ID stored in the session
def load_user(username): 
	'''takes in the user ID and returns the corresponding user object'''
	u = app.config['USERS_collection'].find_one({"_id": username})
	if not u:
		return None
	return User(u['_id'])

# SIGN UP/REGISTRATION

# This is the actual form that we want to connect to our webpage
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])  # must be equal to 'confirm', else error message is Passwords must match
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()]) # checkbox


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form) # allows us to render the form

        if request.method == "POST" and form.validate(): # if user hit register button and form is complete
            username = form.username.data # refers to username from RegistrationForm class
            email = form.email.data
            pass_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256') # hash the user's pw

            try:
                collection = MongoClient('mongodb://viral:ViralViral@ds011271.mlab.com:11271/recipes_users')["users"] # Connect to the DB
                collection.insert({"_id": username, "password": pass_hash})
                flash("Thank you for registering!")
                session['logged_in'] = True # session allows us to store information specific to a user from one request to the next
                session['username'] = username
                login_user=username
                return redirect(url_for('questions')) # if registration was successful, 

            except DuplicateKeyError: 
                flash("Username already taken. Please choose another.")
                return render_template('register.html', form=form)
        
        return render_template('register.html', form=form)
    
    except Exception as e:
        return(str(e))


# OTHER

@app.route('/questions' , methods=['POST', 'GET'])
def questions():
    return render_template('questions.html')

@app.route('/')
@app.route('/search' , methods=['POST', 'GET'])
def search():
    results = None
    if request.method=='POST':
        query = request.form['search']
        results = recipeQueries.get_matches(query)
    return render_template('search.html', results=results)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = recipeQueries.get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/newsfeed' , methods=['POST', 'GET'])
#@login_required # need to login to see newsfeed
def newsfeed():
	return render_template('newsfeed.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/coupons')
def coupons():
    return render_template('coupons.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/swipe')
def swipe():
    return render_template('swipe.html')

@app.route('/list')
def list():
    return render_template('list.html')



if __name__ == '__main__':
    app.run(debug=True)
    