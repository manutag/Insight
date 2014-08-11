from flask import render_template
from app import app
import pymysql as mdb
from flask.json import jsonify

from flask import render_template, flash, redirect, url_for
from app import app
#import forms
#from forms import LoginForm
from flask import request
import MySQLdb
import sys
import numpy
import json
import scipy.stats

from model import read_url, flag_score, flag_score_post


db = mdb.connect(user="root", host="localhost", db="world_innod", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	#return render_template("index.html",
	return render_template("index_js.html",
        title = 'Home', user = { 'nickname': 'Miguel' },
        )

@app.route('/map3')
def map3():
	#return render_template("index.html",
	return render_template("map3.html",
        title = 'Home', user = { 'nickname': 'Miguel' },
        )

@app.route('/port')
def port():
	#return render_template("index.html",
	return render_template("portfolio.html",
        title = 'Home', user = { 'nickname': 'Miguel' },
        )



#@app.route('/login')
#def login():
#	return render_template("login.html",
#        title = 'Home', user = { 'nickname': 'Miguel' },
#        )


@app.route('/index2')
def index2():
	#return render_template("index.html",
	return render_template("index2.html",
        title = 'Home', user = { 'nickname': 'Miguel' },
        )


@app.route('/db')
def cities_page():
	with db: 
		cur = db.cursor()
		cur.execute("SELECT Name FROM City LIMIT 15;")
		query_results = cur.fetchall()
	cities = ""
	for result in query_results:
		cities += result[0]
		cities += "<br>"
	return cities
      
      
@app.route("/db_fancy")
def cities_page_fancy():
	with db:
		cur = db.cursor()
		cur.execute("SELECT Name, CountryCode,Population FROM City ORDER BY Population LIMIT 15;")

		query_results = cur.fetchall()
	cities = []
	for result in query_results:
		cities.append(dict(name=result[0], country=result[1], population=result[2]))
	return render_template('cities.html', cities=cities)       
      
      
      
      
@app.route('/map')
def maps():
	return render_template("map.html",title = 'Home', user = { 'nickname': 'Miguel' },
        )



@app.route('/map2')
def maps2():
	return render_template("map2.html",title = 'Home', user = { 'nickname': 'Miguel' },
        )





@app.route("/db_json")
def cities_json():
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population DESC;")
        query_results = cur.fetchall()
    cities = []
    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))
    return jsonify(dict(cities=cities))
    
    
    
@app.route("/result")
def result_page():
	url = request.args.get('url')
	post = read_url(url)
	score = flag_score(url)
	with db:
		cur = db.cursor()
		cur.execute(
		'''
		SELECT heading, flagged_status, body, external_url
		FROM Postings
		GROUP BY id
		LIMIT 5;
		'''
		)
		query_results = cur.fetchall()
		
	flag_results = []
	for result in query_results:
		flg_score = flag_score_post(result[2])
		flag_results.append(dict(heading=result[0], flagged_status=result[1],body=result[2], url=result[3],flag_score=flg_score))

	flag_results_sorted = sorted(flag_results, key=lambda k: k['flag_score'])
	return render_template('result.html', flag_results=flag_results_sorted,post=post,score=str(score))



@app.route("/rank")

def cities_rank():
        print request.args.get('keywords', '')
        user_input = request.args.get('keywords', '')
	user_input = user_input.lstrip().rstrip()

        country_input = request.args.get('country', '')
	country_input = country_input.lstrip().rstrip()

	with db:
		cur = db.cursor()
		cmnd = "SELECT Name,Population FROM City Limit 15 "

#		if len(user_input.split()) > 0:
#			cmnd = cmnd + "WHERE ("
			# SELECT title, top_words FROM ranking WHERE 
			# (search_terms LIKE "%pub%" AND search_terms LIKE "%bar%") AND
			# (region LIKE "% UNITED %" OR region LIKE "% Australia %");
#			for st in user_input.split():
#				cmnd = cmnd + " search_terms LIKE '%"
#				cmnd = cmnd + "%s" % st
#				cmnd = cmnd + "%'"
#				if user_input.split()[-1] != st:
#					cmnd = cmnd + " AND "
#			cmnd = cmnd + ")"
#
#		if country_input != '':
#			if len(user_input.split()) > 0:
#				cmnd = cmnd + ' AND '
#			else:
#				cmnd = cmnd + 'WHERE '
#			cmnd = cmnd + '('
#      	        	for st in country_input.split(','):
#                      		cmnd = cmnd + " region LIKE '% "
#                       	cmnd = cmnd + "%s" % st
#                        	cmnd = cmnd + " %'"
#                        	if country_input.split(',')[-1] != st:
#                                	cmnd = cmnd + " OR "
#
#			cmnd = cmnd + ");"

		print cmnd
		cur.execute(cmnd)
		query_results = cur.fetchall()
	cities = []
	for result in query_results:
		cities.append(dict(title=result[0], search_terms=result[1]))

	#return "<h3>This is the server response!</h3>"
	tmp = '<table id = "ranklist" class="table table-hover">'
    	tmp = tmp + '<tr><th>Name</th><th>Key Words</th></tr>'

	for city in cities:
    		tmp = tmp + '<tr><td>' + str(city["title"]) + '</td><td>'+ str(city["search_terms"]) + '</td></tr>'
    		
    		
	#tmp = tmp + '<tr><td>' + city["Name"] + '</td><td>'+ city["Population"] + '</td></tr>'    		
	
	tmp = tmp + '</table>'

	return tmp

