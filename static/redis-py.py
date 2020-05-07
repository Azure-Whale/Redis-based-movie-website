#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : redis-py.py
@Time    : 4/3/2020 4:55 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''
import json
import redis
import ast
r = redis.StrictRedis(host='localhost', port=6379, db=1)
'''Method 1'''
#with open('movies.json', 'rb') as f:
#  data = json.load(f)
'''Method 2'''
with open('movies.json', 'rb') as f:
    movies_dict = json.load(f)


for key in movies_dict:
    r.set(str(key['Title']), str(key))
reply = r.get('The Mask of Zorro')
#reply = reply.decode('utf-8')
reply = json.dumps(ast.literal_eval(reply.decode('utf-8')))
print(reply)
temp = json.loads(reply)
print(temp)
'''Movie performance'''
Movie_name = temp['Title']
Movie_Grade = temp['US_Gross']
Movie_Worldwide_Gross = temp['Worldwide_Gross']
Movie_US_DVD_Sales = temp['US_DVD_Sales']
Movie_Production_Budget = temp['Production_Budget']
Movie_Release_Date = temp['Release_Date']
Movie_MPAA_Rating = temp['MPAA_Rating']
Movie_Running_Time_min = temp['Running_Time_min']
Movie_Source = temp['Source']
'''Movie Introduction'''
Movie_Major_Genre = temp['Major_Genre']
Movie_Creative_Type = temp['Creative_Type']
Movie_Director = temp['Director']
'''Audience Grade'''
Movie_Rotten_Tomatoes_Rating = temp['Rotten_Tomatoes_Rating']
Movie_IMDB_Rating = temp['IMDB_Rating']
Movie_IMDB_Votes = temp['IMDB_Votes']


print(temp['Title'],temp['US_Gross'])




'''reply = reply.decode('utf-8')
print(reply)
reply = str(reply)
reply = json.dumps(reply).replace("'", '"',2)
print(reply)
temp = json.loads(reply)
print(temp.dumps())'''
#r.set('movies_dict',movies_dict)
#reply = r.get('The Mask of Zorro')
#r.execute_command('JSON.SET', str(key['Title']), '.', json.dumps(str(key)))
#reply = json.loads(r.execute_command('JSON.GET', 'The Mask of Zorro'))
#print(reply)


'''#print(data)
print(json.dumps(data, indent = 4, sort_keys=True))
print(data)
#with open('movies.json', 'rb') as data_file:
#    test_data = json.load(data_file)
#r.set('hello', 'world')
a = r.get('hello')
print(a.decode('utf-8'))'''


