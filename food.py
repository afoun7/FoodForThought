# Amanda Foun

from flask import Flask, render_template, request, jsonify, redirect, flash
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, url_for
from forms import LoginForm  
from user import User
from flask.ext.wtf import Form  
from wtforms import StringField, PasswordField  
from wtforms.validators import DataRequired
import recipeQueries
import sys
import operator
import json

app = Flask(__name__) # create instance of Flask class
# app.config.from_object(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

# LOGIN INFORMATION
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data): # ensure that user exists
        	print "worked"
        	user_obj = User(user['_id'])
        	login_user(user_obj)
        	flash("Logged in successfully!", category='success')
        	return redirect(request.args.get("next") or url_for("search")) # checks if user has permission to access next url
        print "yes"
        flash("Wrong username or password!", category='error') # could not find in database
        print "tes2"
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login')) # go back to login page

@login_manager.user_loader # user_loader callback is used to reload the user object from the user ID stored in the session
def load_user(username): 
	'''takes in the user ID and returns the corresponding user object'''
	u = app.config['USERS_COLLECTION'].find_one({"_id": username})
	if not u:
		return None
	return User(u['_id'])

@app.route('/')
@app.route('/search' , methods=['POST', 'GET'])
def search():
	results = None
	if request.method=='POST':
		query = request.form['text']
 		results = recipeQueries.get_matches(query)
	return render_template('search.html' ,results=results)

@app.route('/newsfeed' , methods=['POST', 'GET'])
@login_required # need to login to see newsfeed
def newsfeed():
	return render_template('newsfeed.html')



if __name__ == '__main__':
    app.run(debug=True)
    