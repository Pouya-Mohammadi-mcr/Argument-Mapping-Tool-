from os import error
from AMT.Database import Database
from AMT import create_app

import unittest



class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'DATABASE': 'test',
        })    
        with self.app.app_context():
            self.db = Database()

    def testClose(self):
        with self.app.app_context():
            self.db.close()

    def testFindIssues(self):
        with self.app.app_context():
            issues = self.db.findIssues()
        self.assertEqual(issues[0].id, 1, "The first issue id was not returned correctly")
    
    def testFindUser(self):
        with self.app.app_context():
            user1 = self.db.findUser("Pouya")
            #This user will later be created and deleted
            user2 = self.db.findUser("usernametest")
        self.assertEqual(user1.id, 0, "The first user id was not returned correctly")
        self.assertFalse(user2, "The deleteUser function did not work in the previous run")

    def testRegisterUser(self):
        with self.app.app_context():
            registration = self.db.register("usernametest","passwordtest")
        self.assertTrue(registration, "The user was not registered")
        with self.app.app_context():
            registration = self.db.register("usernametest","passwordtest")
            #delete the user created in the last step
            self.db.deleteUser('usernametest')
        self.assertFalse(registration, "Two users with same username were registered")

    def testCreateArgument(self):
        with self.app.app_context():
            argument = self.db.createArgument("Pouya","some text for the test argument")
            argID = argument.id
            #delete the argument created
            self.db.deleteElement(argID)
        self.assertEqual(argument['title'], "some text for the test argument", "The argument creation transaction was not run correctly")
        self.assertEqual(argument['author'], "Pouya", "The argument's author is not correct")

    def testCreateArgumentAndRelation(self):
        with self.app.app_context():
            relatedElements = self.db.createArgumentAndRelation("Pouya","some text for the second test argument", 6, "Supports")
            argID = relatedElements[0]['a']
            relationID = relatedElements[0]['r']
            relatedElementID = relatedElements[0]['e']
            argumentAuthor = relatedElements[0]['author']

            #delete the argument and relation created
            self.db.deleteElement(argID)
            self.db.deleteElement(relationID)

            #test return error with an invalid node id
            relatedElements2 = self.db.createArgumentAndRelation("Pouya","some text for the second test argument", 9999999999, "Supports")

        self.assertEqual(relatedElementID, 6, "The argument and relation creation transaction was not run correctly")
        self.assertEqual(argumentAuthor, "Pouya", "The argument's author is not correct")

        self.assertEqual(relatedElements2, "ERROR", "It should have returned an error")

    def testCreateArgumentAnonymous(self):
        with self.app.app_context():
            argument = self.db.createArgumentAnonymous("Pouya","some text for the test argument")
            argID = argument.id
            #delete the argument created
            self.db.deleteElement(argID)
        self.assertEqual(argument['title'], "some text for the test argument", "The argument creation transaction was not run correctly")
        self.assertEqual(argument['author'], "Anonymous", "The argument's author is not correct")

    def testCreateArgumentAndRelationAnonymous(self):
        with self.app.app_context():
            relatedElements = self.db.createArgumentAndRelationAnonymous("Pouya","some text for the second test argument", 6, "Supports")
            argID = relatedElements[0]['a']
            relationID = relatedElements[0]['r']
            relatedElementID = relatedElements[0]['e']
            argumentAuthor = relatedElements[0]['author']

            #delete the argument and relation created
            self.db.deleteElement(argID)
            self.db.deleteElement(relationID)

            #test return error with an invalid node id
            relatedElements2 = self.db.createArgumentAndRelationAnonymous("Pouya","some text for the second test argument", 9999999999, "Supports")

        self.assertEqual(relatedElementID, 6, "The argument and relation creation transaction was not run correctly")
        self.assertEqual(argumentAuthor, "Anonymous", "The argument's author is not correct")

        self.assertEqual(relatedElements2, "ERROR", "It should have returned an error")

    def testCreateIssue(self):
        with self.app.app_context():
            issue = self.db.createIssue("Pouya","some text for the test issue")
            #delete the issue created
            self.db.deleteElement(issue.id)
        self.assertEqual(issue['title'], "some text for the test issue" ,"The issue was not created")
        self.assertEqual(issue['author'], "Pouya" ,"The issue's author is not correct")

    def testCreateIssueAnonymous(self):
        with self.app.app_context():
            issue = self.db.createIssueAnonymous("Pouya","some text for the test issue")
            #delete the issue created
            self.db.deleteElement(issue.id)
        self.assertEqual(issue['title'], "some text for the test issue" ,"The issue was not created")
        self.assertEqual(issue['author'], "Anonymous" ,"The issue's author is not correct")

    def testCreatePosition(self):
        with self.app.app_context():
            positionAndIssue = self.db.createPosition("Pouya","some text for the test position", 1)
            posID = positionAndIssue[0]['p']
            issueID = positionAndIssue[0]['i']
            positionAuthor = positionAndIssue[0]['author']
            #delete the position created
            self.db.deleteElement(posID)

            #test return error with an invalid node id
            positionAndIssue2 = self.db.createPosition("Pouya","some text for the test position", 9999999999)

        self.assertEqual(issueID, 1,"The position was not created")
        self.assertEqual(positionAuthor, "Pouya","The position was not created")

        self.assertEqual(positionAndIssue2, "ERROR","It should have returned an error")

    def testCreatePositionAnonymous(self):
        with self.app.app_context():
            positionAndIssue = self.db.createPositionAnonymous("Pouya","some text for the test position", 1)
            posID = positionAndIssue[0]['p']
            issueID = positionAndIssue[0]['i']
            positionAuthor = positionAndIssue[0]['author']
            #delete the position created
            self.db.deleteElement(posID)

            #test return error with an invalid node id
            positionAndIssue2 = self.db.createPositionAnonymous("Pouya","some text for the test position", 9999999999)

        self.assertEqual(issueID, 1,"The position was not created")
        self.assertEqual(positionAuthor, "Anonymous","The position was not created")

        self.assertEqual(positionAndIssue2, "ERROR","It should have returned an error")

    def testMatchPassword(self):
        with self.app.app_context():
            self.assertTrue(self.db.matchPassword("Jack","sewnuw-sYhqyb-9domti"))
            self.assertFalse(self.db.matchPassword("Jack","12345"))

    def testCreateRelation(self):
        with self.app.app_context():
            elementsAndRelation = self.db.createRelation("Pouya", 7, 3, "Opposes")
            relationID = elementsAndRelation[0]['r']
            node1ID = elementsAndRelation[0]['n1']
            node2ID = elementsAndRelation[0]['n2']
            #delete the relation created
            self.db.deleteElement(relationID)

            #test return error with an invalid node id
            elementsAndRelation2 = self.db.createRelation("Pouya", 9999999999, 99999999999999, "Opposes")

        self.assertEqual(node1ID, 7,"The relation was not created")
        self.assertEqual(node2ID, 3,"The relation was not created")

        self.assertEqual(elementsAndRelation2, "ERROR","It should have returned an error")

#starting TDD

    def testGetPositions(self):
        with self.app.app_context():
            positions = self.db.getPositions(1)
            self.assertEqual(positions[0]['title'], "Yes", "The first position's title was not returned correctly")
            self.assertEqual(positions[0]['id'], 2, "The first position's id was not returned correctly")
            self.assertEqual(positions[0]['date'], "June 30, 2021", "The first position's date was not returned correctly")
            self.assertEqual(positions[1]['title'], "No", "The second position's title was not returned correctly")
            self.assertEqual(positions[1]['id'], 6, "The second position's id was not returned correctly")
            self.assertEqual(positions[1]['date'], "June 30, 2021", "The second position's date was not returned correctly")

            #test return error with an invalid node id
            positions2 = self.db.getPositions(9999999999)
            self.assertEqual(positions2, "ERROR","It should have returned an error")

    def testGetSignleElement(self):
        with self.app.app_context():
            element = self.db.getSingleElement(1)
            self.assertEqual((list(element.labels)[0]),"Issue", "The elemets label was not returned correctly")
            self.assertEqual(element['title'],"Should X company be allowed to sponsor a conference? " , "The element's title was not returned correctly")
            self.assertEqual(element.id, 1, "The element's id was not returned correctly")
            self.assertEqual(element['date'], "June 30, 2021", "The element's date was not returned correctly")

            #test return error with an invalid node id
            element2 = self.db.getSingleElement(9999999999)
            self.assertEqual(element2, "ERROR","It should have returned an error")

    def testGetArguments(self):
        with self.app.app_context():
            arguments = self.db.getArguments(2)
            self.assertEqual(arguments[0]['relation'],"Supports", "The first argument's relation was not returned correctly")
            self.assertEqual(arguments[0]['relationID'],4, "The first argument's relation ID was not returned correctly")
            self.assertEqual(arguments[0]['title'],"X is a popular company.", "The first supporting argument's title was not returned correctly")
            self.assertEqual(arguments[1]['relation'],"Opposes", "The second argument's relation was not returned correctly")
            self.assertEqual(arguments[1]['title'],"This will encourage arms production.", "The opposing argument's title was not returned correctly")
            self.assertEqual(arguments[3]['relation'],"Asks a question", "The third argument's relation was not returned correctly")
            self.assertEqual(arguments[3]['title'],"Does it mean it should be able to sponsor any conference? or some specific ones?", "The custom argument's title was not returned correctly")

            #test return error with an invalid node id
            arguments2 = self.db.getArguments("anything invalid")
            self.assertEqual(arguments2, "ERROR","It should have returned an error")

    def testRate(self):
        with self.app.app_context():
            issue = self.db.createIssue("Pouya","some text for the test issue for rating")
            elementAndRelation = self.db.rate("Pouya", issue.id, 5)
            rate = elementAndRelation[0]['rate']
            rateSum = elementAndRelation[0]['rateSum']
            ratesNo = elementAndRelation[0]['ratesNo']
        self.assertEqual(rate, 5,"The new rating was not returned correctly")
        self.assertEqual(rateSum, 5,"The sum of ratings was not returned correctly")
        self.assertEqual(ratesNo, 1,"The total number of rates was not returned correctly")

        with self.app.app_context():
            elementAndRelation = self.db.rate("Jack", issue.id, 4)
            rate = elementAndRelation[0]['rate']
            rateSum = elementAndRelation[0]['rateSum']
            ratesNo = elementAndRelation[0]['ratesNo']
        self.assertEqual(rate, 4,"The new rating was not returned correctly")
        self.assertEqual(rateSum, 9,"The sum of ratings was not returned correctly")
        self.assertEqual(ratesNo, 2,"The total number of rates was not returned correctly")
        
        with self.app.app_context():
            elementAndRelation = self.db.rate("Pouya", issue.id, 3)
            rate = elementAndRelation[0]['rate']
            rateSum = elementAndRelation[0]['rateSum']
            ratesNo = elementAndRelation[0]['ratesNo']
            #delete the issue created
            self.db.deleteElement(issue.id)

           #test return error with an invalid node id
            elementAndRelation2 = self.db.rate("Pouya", 99999999, 5)

        self.assertEqual(rate, 3,"The new rating was not returned correctly")
        self.assertEqual(rateSum, 7,"The sum of ratings was not returned correctly")
        self.assertEqual(ratesNo, 2,"The total number of rates was not returned correctly")
        self.assertEqual(elementAndRelation2, "ERROR","It should have returned an error")

    def testGetUserRate(self):
        with self.app.app_context():
            ratedRelation = self.db.getUserRate("Pouya",2)
            userRate = ratedRelation['rate']
            nullRatedRelation = self.db.getUserRate("Pouya",4)

        self.assertEqual(userRate, 5,"The user rate was not returned correctly")
        self.assertEqual(nullRatedRelation, "ERROR", "The non existent user rate was not returned correctly")

    def testSearch(self):
        with self.app.app_context():
            searchResults = self.db.search("X")
            node1 = searchResults[0]['title']
            node2 = searchResults[1].id
            node3 = searchResults[2].id
            node4 = searchResults[3].id

            searchResults2 = self.db.search("somewierdtext asada asdasd ")
            
        self.assertEqual(searchResults2, "ERROR","The empty search results not returned correctly")

        self.assertEqual(node1, "X is a popular company.","The title for the first matched node was not returned correctly")
        self.assertEqual(node2, 1, "The id for the second matched node was not returned correctly")
        self.assertEqual(node3, 7, "The id for the third matched node was not returned correctly")
        self.assertEqual(node4, 20, "The id for the fourth matched node was not returned correctly")

    def testGetUserReputation(self):
        with self.app.app_context():
            reputation = self.db.getUserReputation("Pouya")
            reputation2 = self.db.getUserReputation("Rob")

        self.assertEqual(reputation, 'Reputation: 4.67/5, number of rated contributions: 3',"The user's reputation was not returned correctly")
        self.assertEqual(reputation2, 'No ratings avaialable' ,"The user's reputation was not returned correctly")

    def testGetRelFrom(self):
        with self.app.app_context():
            relFrom = Database().getRelFrom(21)
        self.assertEqual(relFrom.id, 20 ,"The relation's 'from' node was not returned correctly")

    def testGetRelTo(self):
        with self.app.app_context():
            relTo = Database().getRelTo(21)
        self.assertEqual(relTo.id, 2 ,"The relation's 'to' node was not returned correctly")

    def testGetParentTopic(self):
        with self.app.app_context():
            relTo = Database().getParentTopic(2)
        self.assertEqual(relTo.id, 1 ,"The position's parent node was not returned correctly")

    def testGetParentTopic(self):
        with self.app.app_context():
            relTo = Database().getParentTopic(2)
        self.assertEqual(relTo.id, 1 ,"The position's parent node was not returned correctly")


    def testGetOutgoingArguments(self):
        with self.app.app_context():
            arguments = self.db.getOutgoingArguments(7)
            self.assertEqual(arguments[0]['relation'],"Supports", "The first argument's relation was not returned correctly")
            self.assertEqual(arguments[0]['relationID'],8, "The first argument's relation ID was not returned correctly")
            self.assertEqual(arguments[0]['title'],"No", "The first supported argument's title was not returned correctly")
            self.assertEqual(list(arguments[0]['label'])[0],"Position", "The first supported argument's label was not returned correctly")

           #test return error with an invalid node id
            arguments2 = self.db.getOutgoingArguments(99999999999)
            self.assertEqual(arguments2, "ERROR","It should have returned an error")

if __name__ == '__main__':
    unittest.main()
