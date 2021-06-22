from AMT.Database import getDB
from py2neo import Graph, Node, Relationship, NodeMatcher
import bcrypt
import uuid
import datetime


class User:
    def __init__(self, username):
        self.username = username
        self.graph = getDB()

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


class Argument:
    pass

class Relation:
    pass 