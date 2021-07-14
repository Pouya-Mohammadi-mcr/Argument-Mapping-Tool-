from flask import current_app, g
from flask.cli import with_appcontext
import csv
import os

import bcrypt
import uuid
import datetime

from neo4j import GraphDatabase
import logging
from neo4j.exceptions import *

class Database():
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
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.read_transaction(self.findAndReturnIssues)
            return result

    @staticmethod
    def findAndReturnIssues(tx):
        query = (
            "MATCH (i:Issue) "
            "RETURN i "
            "ORDER BY -i.rateSum/i.ratesNo"

        )
        issues = tx.run(query)
        try:
            return [row["i"] for row in issues]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise    

    def findUser(self, username):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.read_transaction(self.findAndReturnUser,username)
            if len(result)>0:
                #only one user with the username
                return result[0]
            else:
                return False

    @staticmethod
    def findAndReturnUser(tx, username):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "RETURN u"
        )
        user = tx.run(query, username=username)
        try:
            return [row["u"] for row in user]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def register(self, username, password):
        if not self.findUser(username):
            with self.driver.session(database=current_app.config['database']) as session:
            # Write transactions allow the driver to handle retries and transient errors
                result = session.write_transaction(self.createAndReturnUser, username, password)
                return True
        else:
            return False

    @staticmethod
    def createAndReturnUser(tx, username, password):
        query = (
            "CREATE (u:User { username: $username, password: $password }) "
        )
        #fix .encode 
        result = tx.run(query, username=username, password= bcrypt.hashpw(password.encode(), bcrypt.gensalt()) )
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createArgument(self, username, title):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnArgument, username, title)
            return result

    @staticmethod
    def createAndReturnArgument(tx, username, title):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "CREATE (a:Argument { title: $title, date: $date, author: $username }) "
            "CREATE (u)-[:MADE]->(a) "
            "RETURN a"
        )
        result = tx.run(query, title=title, username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            record = result.single()
            value = record.value()
            return value
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createArgumentAndRelation(self, username, title, elementID, relation ):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnArgumentAndRelation, username, title, elementID, relation)
            return result

    @staticmethod
    def createAndReturnArgumentAndRelation(tx, username, title, elementID, relation):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (e) "
            "WHERE id(e) = $elementID "

            "CREATE (a:Argument { title: $title, date: $date, author: $username }) "
            "CREATE (u)-[:MADE]->(a) "

            "CREATE (r:Relation { title: $relation, date: $date }) "
            "CREATE (u)-[:CREATED]->(r) "
            "CREATE (r)-[:FROM]->(a) "
            "CREATE (r)-[:TO]->(e) "

            "RETURN a, r, e"
        )
        result = tx.run(query, title=title, username=username, elementID=int(elementID), relation=relation, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            relatedElements = ( [{"a": row["a"].id, "author": row["a"]["author"], "r": row["r"].id, "e": row["e"].id}
                    for row in result] )
            if len(relatedElements) == 0:
                return "ERROR"
            else:
                return relatedElements
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createArgumentAnonymous(self, username, title):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnArgumentAnonymous, username, title)
            return result

    @staticmethod
    def createAndReturnArgumentAnonymous(tx, username, title):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "CREATE (a:Argument { title: $title, date: $date, author: 'Anonymous' }) "
            "CREATE (u)-[:MADE]->(a) "
            "RETURN a"
        )
        result = tx.run(query, title=title, username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            record = result.single()
            value = record.value()
            return value
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createArgumentAndRelationAnonymous(self, username, title, elementID, relation ):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnArgumentAndRelationAnonymous, username, title, elementID, relation)
            return result

    @staticmethod
    def createAndReturnArgumentAndRelationAnonymous(tx, username, title, elementID, relation):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (e) "
            "WHERE id(e) = $elementID "

            "CREATE (a:Argument { title: $title, date: $date, author: 'Anonymous' }) "
            "CREATE (u)-[:MADE]->(a) "

            "CREATE (r:Relation { title: $relation, date: $date }) "
            "CREATE (u)-[:CREATED]->(r) "
            "CREATE (r)-[:FROM]->(a) "
            "CREATE (r)-[:TO]->(e) "

            "RETURN a, r, e"
        )
        result = tx.run(query, title=title, username=username, elementID=int(elementID), relation=relation, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            relatedElements = ( [{"a": row["a"].id, "author": row["a"]["author"], "r": row["r"].id, "e": row["e"].id}
                    for row in result] )
            if len(relatedElements) == 0:
                return "ERROR"
            else:
                return relatedElements
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createIssue(self, username, title):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnIssue, username, title)
            return result

    @staticmethod
    def createAndReturnIssue(tx, username, title):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "CREATE (i:Issue { title: $title, date: $date, author: $username  }) "
            "CREATE (u)-[:RAISED]->(i) "
            "Return i"
        )
        #fix .encode 
        result = tx.run(query, title=title, username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            record = result.single()
            value = record.value()
            return value
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createIssueAnonymous(self, username, title):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnIssueAnonymous, username, title)
            return result

    @staticmethod
    def createAndReturnIssueAnonymous(tx, username, title):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "CREATE (i:Issue { title: $title, date: $date, author: 'Anonymous' }) "
            "CREATE (u)-[:RAISED]->(i) "
            "Return i"
        )
        #fix .encode 
        result = tx.run(query, title=title, username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            record = result.single()
            value = record.value()
            return value
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    
    def createPosition(self, username, title, issueID):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnPosition, username, title, issueID)
            return result

    @staticmethod
    def createAndReturnPosition(tx, username, title, issueID):
        #Does not check if the issueID is actually an ID for an ISSUE
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (i) "
            "WHERE id(i) = $issueID "
            "CREATE (p:Position { title: $title, date: $date, author: $username }) "
            "CREATE (u)-[:TOOK]->(p) "
            "CREATE (p)-[:ANSWERS]->(i) "
            "RETURN i, p"

        )
        #fix .encode 
        result = tx.run(query, title=title, issueID=int(issueID), username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            relatedElements = ( [{"i": row["i"].id, "p": row["p"].id, "author": row["p"]["author"], }
                    for row in result] )
            if len(relatedElements) == 0:
                return "ERROR"
            else:
                return relatedElements
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createPositionAnonymous(self, username, title, issueID):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnPositionAnonymous, username, title, issueID)
            return result

    @staticmethod
    def createAndReturnPositionAnonymous(tx, username, title, issueID):
        #Does not check if the issueID is actually an ID for an ISSUE
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (i) "
            "WHERE id(i) = $issueID "
            "CREATE (p:Position { title: $title, date: $date, author:'Anonymous' }) "
            "CREATE (u)-[:TOOK]->(p) "
            "CREATE (p)-[:ANSWERS]->(i) "
            "RETURN i, p"

        )
        #fix .encode 
        result = tx.run(query, title=title, issueID=int(issueID), username=username, date=datetime.datetime.now().strftime("%B %d, %Y"))
        try:
            relatedElements = ( [{"i": row["i"].id, "p": row["p"].id, "author": row["p"]["author"],}
                    for row in result] )
            if len(relatedElements) == 0:
                return "ERROR"
            else:
                return relatedElements
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def matchPassword(self, username, givenPassword):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.findAndReturnPassword, username)
            if len(result)>0:
                storedPassword = result[0]
                if bcrypt.checkpw(givenPassword.encode(), storedPassword):
                    return True
                else:
                    return False 

    @staticmethod
    def findAndReturnPassword(tx, username):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "RETURN u.password AS password"
        )
        result = tx.run(query, username=username)
        try:
            return [row["password"] for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createRelation(self, username, node1, node2, relationType):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.createAndReturnRelation, username, node1, node2, relationType)
            return result

    @staticmethod
    def createAndReturnRelation(tx, username, node1, node2, relationType):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (n1) "
            "WHERE id(n1) = $node1 "
            "MATCH (n2) "
            "WHERE id(n2) = $node2 "
            "CREATE (r:Relation { title: $title, date: $date }) "
            "CREATE (u)-[:CREATED]->(r) "
            "CREATE (r)-[:FROM]->(n1) "
            "CREATE (r)-[:TO]->(n2) "

            "RETURN n1, r, n2"

        )
        #fix .encode 
        result = tx.run(query, title=relationType, username=username, date=datetime.datetime.now().strftime("%B %d, %Y"), node1=int(node1), node2=int(node2))
        try:
            foundNodes = ( [{"n1": row["n1"].id, "r": row["r"].id, "n2": row["n2"].id}
                    for row in result] )
            if len(foundNodes) == 0:
                return "ERROR"
            else:
                return foundNodes
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def deleteUser(self, username):
        with self.driver.session(database=current_app.config['database']) as session:
            session.write_transaction(self.findAndDeleteUser,username)


    @staticmethod
    def findAndDeleteUser(tx, username):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "DELETE (u)"
        )
        try:
            tx.run(query, username=username)
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def deleteElement(self, elementID):
        with self.driver.session(database=current_app.config['database']) as session:
            session.write_transaction(self.findAndDeleteElement,elementID)


    @staticmethod
    def findAndDeleteElement(tx, elementID):
        query = (
            "MATCH (e) "
            "WHERE id(e) = $elementID "
            "DETACH DELETE (e)"
        )
        try:
            tx.run(query, elementID=elementID)
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

#starting TDD

    def getPositions(self, issueID):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.read_transaction(self.findAndReturnPositions, issueID)
            return result

    @staticmethod
    def findAndReturnPositions(tx, issueID):
        query = (
            "MATCH (i:Issue) "
            "WHERE id(i) = $issueID "
            "MATCH (i)<-[:ANSWERS]-(p:Position) "
            "RETURN p "
            "ORDER BY -p.rateSum/p.ratesNo"
        )
        result = tx.run(query, issueID=issueID)
        try:
            foundPositions = ( [{"title": row["p"]["title"], "id": row["p"].id, "date": row["p"]["date"], "author": row["p"]["author"], "rateSum": row["p"]["rateSum"], "ratesNo": row["p"]["ratesNo"]}
                    for row in result] )
            if len(foundPositions) == 0:
                return "ERROR"
            else:
                return foundPositions
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def getSingleElement(self, elementID):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.findAndReturnElement, elementID)
            return result

    @staticmethod
    def findAndReturnElement(tx, elementID):
        query = (
            "MATCH (e) "
            "WHERE id(e) = $elementID "
            "Return e"
        )
        #fix .encode 
        result = tx.run(query,  elementID=elementID)

        try:
            record = result.single()
            if record:
                value = record.value()
            else:
                value = "ERROR"
            return value
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def getArguments(self, elementID):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.read_transaction(self.findAndReturnArguments, elementID)
            return result

    @staticmethod
    def findAndReturnArguments(tx, elementID):
        query = (
            "MATCH (e) "
            "WHERE id(e) = $elementID "
            "WITH (e)"
            "MATCH (e)<-[:TO]-(r:Relation) "
            "WITH (r)"
            "MATCH (a:Argument)<-[:FROM]-(r:Relation) "
            "RETURN a, r.title, id(r) "
            "ORDER BY -a.rateSum/a.ratesNo"

        )
        result = tx.run(query, elementID=elementID)
        try:
            arguments = ( [{"relation": row['r.title'], "relationID": row['id(r)'], "title": row["a"]["title"], "id": row["a"].id, "date": row["a"]["date"], "author": row["a"]["author"], "rateSum": row["a"]["rateSum"], "ratesNo": row["a"]["ratesNo"]}
                    for row in result] )
            if len(arguments) == 0:
                return "ERROR"
            else:
                return arguments
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def rate(self, username, elementID, rating):
        with self.driver.session(database=current_app.config['database']) as session:
            result = session.write_transaction(self.rateAndReturn, username, elementID, rating)
            return result

    @staticmethod
    def rateAndReturn(tx, username, elementID, rating):
        query = (
            "MATCH (u:User) "
            "WHERE u.username = $username "
            "MATCH (e) "
            "WHERE id(e) = $elementID "
            "SET e.ratesNo = "
            "CASE WHEN e.ratesNo IS NULL THEN 1 ELSE e.ratesNo+1 END "
            "SET e.rateSum = "
            "CASE WHEN e.rateSum IS NULL THEN $rating ELSE e.rateSum+$rating END "
            "MERGE (u)-[r:RATED]->(e) ON CREATE SET r.rate=$rating ON MATCH SET e.rateSum=e.rateSum-r.rate, e.ratesNo=e.ratesNo-1, r.rate=$rating "

            "RETURN e.ratesNo, e.rateSum, r.rate"

        )
        #fix .encode 
        result = tx.run(query, username=username, elementID=int(elementID), rating=int(rating))
        try:
            foundNodes = ( [{"ratesNo": row["e.ratesNo"], "rateSum": row["e.rateSum"], "rate": row["r.rate"]}
                    for row in result] )
            if len(foundNodes) == 0:
                return "ERROR"
            else:
                return foundNodes
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise