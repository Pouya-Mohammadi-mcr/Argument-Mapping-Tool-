import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv
import os

import bcrypt
import uuid
import datetime


from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class Database():
    #this should substitute getDB
    def __init__(self):
        if 'db' not in g:
            absolutePath = os.path.dirname(os.path.abspath(__file__))
            fileName= absolutePath+"/static/Credentials.txt"
            with open(fileName) as f1:
                data=csv.reader(f1,delimiter=",")
                for row in data:
                    username=row[0]
                    password=row[1]
                    uri=row[2]
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            #might be unnecessary
            g.db = self.driver
        else:
            self.driver = g.db

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
        
    def findIssues(self):
        with self.driver.session() as session:
            result = session.read_transaction(self.findAndReturnIssues)
            return result


    @staticmethod
    def findAndReturnIssues(tx):
        query = (
            "MATCH (i:Issue) "
            "RETURN i"
        )
        issues = tx.run(query)
        return [row["i"] for row in issues]


class User:
    def __init__(self, username):
        self.username = username
        self.graph = Database()

    def find(self):
        pass
    
    def register(self, password):
        pass

    def createArgument(self, title, text):
        pass

    def createIssue(self, title, text):
        pass

    def createPosition(self, title, text):
        pass

    def createRelation(self, node1, node2, relationType):
        pass

    def matchPassword(self, givenPassword):

        pass

#def getIssuePositions(issueID):
#    graph = getDB()
#    matcher = NodeMatcher(graph)
#    issue = matcher.get(issueID)


#def close_db(e=None):
#    db = g.pop('db', None)

#    if db is not None:
#        db.close()



