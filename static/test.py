#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : test.py
@Time    : 4/9/2020 3:14 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''
from flask import Flask, redirect, url_for, request, session
from flask import render_template
import json
import redis
import ast

with open('movies.json', 'rb') as f:
    movies_dict = json.load(f)
r = redis.StrictRedis(host='localhost', port=6379, db=1)


'''Set a secondary index for Director'''
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

director_name = "David Dobkin"  # Receive it
movie_list = r.get(director_name)
movie_list = movie_list.decode('utf-8')
#print(movie_list)
res = ast.literal_eval(movie_list)
#print(res[0])

for name in res:
    movie = r.get(name)
    movie = movie.decode('utf-8')
    movie = json.dumps(ast.literal_eval(movie))
    movie = json.loads(movie)
    print(movie['US_Gross'])



