import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv
import os

from py2neo import Graph, Node, Relationship, NodeMatcher
import bcrypt
import uuid
import datetime


from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class Database():
    #this should substitute getDB
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
        
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
        
    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]


def getIssues():
    graph = Database().getDB()
    issues = graph.run("MATCH (a:Issue) RETURN ID(a), a.title, a.date, a.text ").data()
    return issues


class User:
    def __init__(self, username):
        self.username = username
        self.graph = Database().getDB()

    def find(self):
        matcher = NodeMatcher(self.graph)
        user = matcher.match("User", username=self.username).first()
        return user
    
    def register(self, password):
        if not self.find():
            user = Node("User", username = self.username, password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            self.graph.create(user)
            return True
        else:
            return False

    def createArgument(self, title, text):
        user = self.find()
        argument = Node(
            "Argument",
#            id=str(uuid.uuid4()),
            title=title,
            text=text,
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        rel = Relationship(user, "MADE", argument)
        self.graph.create(rel)

    def createIssue(self, title, text):
        user = self.find()
        issue = Node(
            "Issue",
#            id=str(uuid.uuid4()),
            title=title,
            text=text,
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        rel = Relationship(user, "RAISED", issue)
        self.graph.create(rel)

    def createPosition(self, title, text):
        user = self.find()
        position = Node(
            "Position",
#            id=str(uuid.uuid4()),
            title=title,
            text=text,
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        rel = Relationship(user, "TOOK", position)
        self.graph.create(rel)

    def createRelation(self, node1, node2, relationType):
        user = self.find()
        relation = Node(
            "Relation",
            title=relationType,
#            id=str(uuid.uuid4()),
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        matcher = NodeMatcher(self.graph)
        firstNode = matcher.get(int(node1))
        secondNode = matcher.get(int(node2))

        rel = Relationship(user, "CREATED", relation)
        rel1 = Relationship(relation, "FROM", firstNode)
        rel2 = Relationship(relation, "TO", secondNode)

        self.graph.create(rel) 
        self.graph.create(rel1)
        self.graph.create(rel2)

    def matchPassword(self, givenPassword):

        storedPassword = self.graph.run("MATCH (user) WHERE user.username=$x RETURN user.password", x=self.username).evaluate()
        print(storedPassword)
        print(self)
        if bcrypt.checkpw(givenPassword.encode(), storedPassword.encode()):
            return True
        else:
            return False 

#def getIssuePositions(issueID):
#    graph = getDB()
#    matcher = NodeMatcher(graph)
#    issue = matcher.get(issueID)


#def close_db(e=None):
#    db = g.pop('db', None)

#    if db is not None:
#        db.close()



