# Amanda Foun

from flask import Flask, render_template, request, jsonify, redirect, flash, session, g
from flask.ext.login import current_user, LoginManager, UserMixin, login_required, login_user, logout_user, url_for 
from forms import LoginForm  
from user import User
from flask.ext.wtf import Form
from functools import wraps 
from wtforms import StringField, PasswordField, Form, BooleanField, RadioField, TextField, validators, widgets,SelectMultipleField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import recipeQueries
import sys
import operator
import json

app = Flask(__name__) # create instance of Flask class
#app.config.from_object(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

curr_user = ""

# LOGIN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():

        #user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        user = User(form.username.data)
        print (user)
        curr_user = user

        if user and User.validate_login(user.password, form.password.data): # ensure that user exists
        	# user_obj = User(user['_id'])
        	login_user(user)
        	flash("Logged in successfully!", category='success')
        	return redirect(url_for("search"))
        else:  
            flash("Wrong username or password!", category='error') # could not find in database
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login')) # go back to login page


@login_manager.user_loader # user_loader callback is used to reload the user object from the user ID stored in the session
def load_user(username): 
    user = User()
    return user.get(username)
	# u = app.config['USERS_COLLECTION'].find_one({"_id": username})
	# if not u:
	# 	return None
	# return User(u)

# Sign up/Registration
# After registering with a username, email, and password, users are redirected to the 
# sign up questionnaire

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
                print ("in try")
                collection = app.config['USERS_COLLECTION'] # Connect to the DB
                print (collection)
                collection.insert({"_id": username, "password": pass_hash})
                print ("after insert")
                flash("Thank you for registering!")
                session['logged_in'] = True # session allows us to store information specific to a user from one request to the next
                session['username'] = username
                # login_user=username
                # print (login_user)
                return redirect(url_for('questions')) # if registration was successful, 

            except DuplicateKeyError: 
                flash("Username already taken. Please choose another.")
                return render_template('register.html', form=form)
        
        return render_template('register.html', form=form)
    
    except Exception as e:
        return(str(e))

# Sign up questionnaire

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class QuestionsForm(Form):
    string_restrictions = ['Gluten-Free\r\nVegan\r\nVegetarian\r\n']
    list_restrictions = string_restrictions[0].split()
    files_restrictions = [(x, x) for x in list_restrictions]
    restrictions = MultiCheckboxField('Restrictions', choices=files_restrictions)

    string_allergies = ['Peanuts\r\nTree-nuts\r\nMilk\r\nEgg\r\nSoy\r\nFish\r\nShell-Fish\r\n']
    list_allergies = string_allergies[0].split()
    files_allergies = [(x, x) for x in list_allergies]
    allergies = MultiCheckboxField('Allergies', choices=files_allergies)

    zipcode = TextField('Zipcode',[validators.Length(min=5, max=5)])
    time = RadioField('How much time do you usually have to cook per meal?', choices=[('option1','Less than 30 minutes'),('option2','1 hour'),('option3','1.5 hours'),('option4','2 hours')])
    meal = RadioField('Which meals are you interested in cooking?', choices=[('option1','Breakfast'),('option2','Lunch'),('option3','Dinner')])


@app.route('/questions' , methods=['POST', 'GET'])
def questions():
    try:
        form = QuestionsForm(request.form) # allows us to render the form

        if request.method == "POST" and form.validate(): # if user hit submit button and form is complete
            print ("submitted form")
            restrictions = form.restrictions.data 
            allergies = form.allergies.data
            zipcode = form.zipcode.data
            time = form.time.data
            meal = form.meal.data

            try:
                #username = {{current_user.name }}
                collection = app.config['USERS_COLLECTION'] # Connect to the DB
                collection.update({"_id":curr_user},{"restrictions": restrictions, "allergies": allergies, "zipcode": zipcode, "time": time, "meal": meal})
                flash("Thank you!")
                return redirect(url_for('search')) # if registration was successful, 

            except Exception as e: 
                return(str(e))
        
        return render_template('questions.html', form=form)
    
    except Exception as e:
        return(str(e))

# OTHER
@app.route('/')
@app.route('/search' , methods=['POST', 'GET'])
def search():
    if not current_user.is_anonymous():
        print (current_user.username)
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
def list(recipe_id):
    recipe = recipeQueries.get_recipe(recipe_id)
    return render_template('list.html',recipe=recipe)



if __name__ == '__main__':
    app.run(debug=True)
    