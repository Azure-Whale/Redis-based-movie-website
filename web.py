#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : web.py
@Time    : 4/5/2020 3:24 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''
from flask import Flask, redirect, url_for, request, session
from flask import render_template
import json
import redis
import ast

'''Import Data'''
r = redis.StrictRedis(host='localhost', port=6379, db=1)   # Connect to it
with open('movies.json', 'rb') as f:  # Reading json file into the system
    movies_dict = json.load(f)   # Return a set of dictionary

for unit in movies_dict: # Traverse the set of dictionary
    r.set(str(unit['Title']), str(unit))    # title of movie name as the key, and the all dictionary as the value




'''Index Initilization '''
director_index= []

for key in movies_dict:
    director_index.append(key['Director'])
    #r.set(str(key['Title']), str(key))
#print(director_index)

test= dict()
for person in director_index:
    each=[]
    for key in movies_dict:
        if key['Director'] == person:
            each.append(key['Title'])
    test[person]=each
#print(test)

for key,value in test.items():
    #print(str(key),str(value))
    r.set(str(key),str(value))


#c=4 func a func b

'''Web Start'''
app = Flask(__name__)
app.secret_key = "super secret key"

# The Home Page
@app.route("/", methods=['POST','GET'])  # If you page needs a method, define it in prior
def home():
    if request.method == "POST":  # If the page got request, it start running these code as it got a POST request
        mn = request.form["mn"]  #  Retrive the var called mn from the web
        session["Searched"] = mn  # define a temporary var of web, which does as a global var serving for other pages
        return redirect(url_for("Find"))
    else:
        return render_template("index.html")   # When there is no method done, the code would end up with this place. In other words, it would initiliza the home page


@app.route("/Find")  # It enables me to input anything in the url bar then it would redirct to a new page I want to
def Find():
    try:
        if "Searched" in session:  # Check whether the parameter has been passed
            Searched = session['Searched']  # Received
            if Searched in director_index:  # If the user is searching by the name of director
                director_name = Searched
                movie_list = r.get(director_name)  # Get a list of movie title made from this director
                movie_list = movie_list.decode('utf-8')
                res = ast.literal_eval(movie_list)  # Transfer the string presentation of list into real list
                movie_list = []
                for name in res:  # For each movie in the our list, search the DB by title of movie
                    movie = r.get(name)
                    movie = movie.decode('utf-8')
                    movie = json.dumps(ast.literal_eval(movie))
                    movie = json.loads(movie)
                    movie_list.append(movie)
                return render_template('Results.html', mv = movie_list)
                # If the user search by title of movie
            else:
                reply = r.get(Searched)  # Get the value according to the key in redis

                '''Transformation'''
                reply = reply.decode('utf-8')
                reply = json.dumps(ast.literal_eval(reply))
                movie = json.loads(reply)

                movie_list=[]
                movie_list.append(movie)

                return render_template('Results.html', mv = movie_list)  # Present with new html and pass your result to it
        else:
            return render_template("404.html")
    except:
        return render_template("404.html")


@app.route('/add',methods=['POST', 'GET'])  # This method help us redirect user to defined page
def add():
    if request.method == "POST":
        mn = request.form["mn"]
        di = request.form["di"]
        mg = request.form["mg"]
        ug = request.form["ug"]
        wg = request.form["wg"]
        pb = request.form["pb"]
        rt = request.form["rt"]
        '''session["mn"] = mn
        session["di"] = di
        session["mg"] = mg
        session["ug"] = ug
        session["wg"] = wg
        session["pb"] = pb
        session["rt"] = rt'''

        temp = {'Title': mn, 'Director': di, 'Major_Genre': mg, 'US_Gross': ug, 'Worldwide_Gross': wg, 'Production_Budget': pb, 'Rotten_Tomatoes_Rating': rt}
        #temp = json.dumps(temp)
        #print(temp)
        r.set(str(temp['Title']), str(temp))
        return render_template("Operation Confirm.html")
    else:
        return render_template("add.html")

@app.route('/Delete',methods=['POST', 'GET'])  # This method help us redirect user to defined page
def Delete():
    if request.method == "POST":
        mn = request.form["mn"]
        #session["mn"] = mn
        try:
            r.delete(mn)
            return render_template("Operation Confirm.html")
        except:
            return render_template("Operation Fail.html")
    else:
        return render_template("delete.html")


@app.route('/update', methods=['POST', 'GET'])  # This method help us redirect user to defined page
def update():
    if request.method == "POST":
        session["update_movie_name"] = request.form["update_movie_name"]
        try:
            return redirect(url_for("updating"))
        except:
            return render_template("Operation Fail.html")
    else:
        return render_template("/update.html")

@app.route('/updating', methods=['POST', 'GET'])  # This method help us redirect user to defined page
def updating():
    reply = r.get(session["update_movie_name"])
    '''Transformation string to dict'''
    reply = reply.decode('utf-8')
    reply = json.dumps(ast.literal_eval(reply))
    movie = json.loads(reply)

    if request.method == "POST":
        try:
            mn = request.form["mn"]
            di = request.form["di"]
            mg = request.form["mg"]
            ug = request.form["ug"]
            wg = request.form["wg"]
            pb = request.form["pb"]
            rt = request.form["rt"]
            session["mn"] = mn
            session["di"] = di
            session["mg"] = mg
            session["ug"] = ug
            session["wg"] = wg
            session["pb"] = pb
            session["rt"] = rt

            temp = {'Title': mn, 'Director': session["di"], 'Major_Genre': mg, 'US_Gross': ug, 'Worldwide_Gross': wg,
                    'Production_Budget': pb, 'Rotten_Tomatoes_Rating': rt}

            r.set(str(temp['Title']), str(temp))
            return render_template("Operation Confirm.html")
        except:
            return render_template("Operation Fail.html")
    return render_template("updating.html", movie=movie)


if __name__ == '__main__':
    app.run(debug=True)  # debug makes your web update without restart
    app.run()
