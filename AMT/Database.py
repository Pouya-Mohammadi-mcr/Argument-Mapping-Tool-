import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from py2neo import Graph
import csv
import os

def getDB():
    if 'db' not in g:
        absolutePath = os.path.dirname(os.path.abspath(__file__))
        fileName= absolutePath+"/static/Credentials.txt"
        with open(fileName) as f1:
            data=csv.reader(f1,delimiter=",")
            for row in data:
                username=row[0]
                pwd=row[1]
                uri=row[2]
        g.db = Graph(uri, auth=(username, pwd))

    return g.db


#def close_db(e=None):
#    db = g.pop('db', None)

#    if db is not None:
#        db.close()



