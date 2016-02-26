# Amanda Foun

from flask import Flask, render_template, request, jsonify
import recipeQueries
import sys
import operator
import json

app = Flask(__name__) # create instance of Flask class
app.config.from_object(__name__)

@app.route('/') # route decorator

@app.route('/search' , methods=['POST', 'GET'])
def search():
	results = None
	if request.method=='POST':
		query = request.form['text']
 		results = recipeQueries.get_matches(query)
	return render_template('search.html' ,results=results)

@app.route('/searchResults', methods=['POST', 'GET']) 
def search_results():
 	#recipeQueries.get_matches(request.get('id'))
 	#recipeQueries.get_matches(request.json['id'])
 	print "in search_results"
 	if request.method=='POST':
 		print "in search_results if"
 		query = request.json['id']
 		results = recipeQueries.get_matches(query)
 		print (results)
	return render_template("searchResults.html")


if __name__ == '__main__':
    app.run(debug=True)