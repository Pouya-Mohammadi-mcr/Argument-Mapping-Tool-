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

#    def testClose(self):
#        with self.app.app_context():
#            self.db.close()
#        self.assertFalse(self.db, "The connection was not closed")

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

    def testCreateArgumentAndRelation(self):
        with self.app.app_context():
            relatedElements = self.db.createArgumentAndRelation("Pouya","some text for the second test argument", 6, "Supports")
            argID = relatedElements[0]['a']
            relationID = relatedElements[0]['r']
            relatedElementID = relatedElements[0]['e']
            #delete the argument created
            self.db.deleteElement(argID)
            self.db.deleteElement(relationID)

        self.assertEqual(relatedElementID, 6, "The argument and relation creation transaction was not run correctly")

    def testCreateIssue(self):
        with self.app.app_context():
            issue = self.db.createIssue("Pouya","some text for the test issue")
            #delete the issue created
            self.db.deleteElement(issue.id)
        self.assertEqual(issue['title'], "some text for the test issue" ,"The issue was not created")

    def testCreatePosition(self):
        with self.app.app_context():
            positionAndIssue = self.db.createPosition("Pouya","some text for the test position", 1)
            posID = positionAndIssue[0]['p']
            issueID = positionAndIssue[0]['i']
            #delete the position created
            self.db.deleteElement(posID)
        self.assertEqual(issueID, 1,"The position was not created")

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
        self.assertEqual(node1ID, 7,"The relation was not created")
        self.assertEqual(node2ID, 3,"The relation was not created")

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

    def testGetSignleElement(self):
        with self.app.app_context():
            element = self.db.getSingleElement(1)
            self.assertEqual(element['title'],"Should X company be allowed to sponsor a conference? " , "The element's title was not returned correctly")
            self.assertEqual(element.id, 1, "The element's id was not returned correctly")
            self.assertEqual(element['date'], "June 30, 2021", "The element's date was not returned correctly")
        


if __name__ == '__main__':
    unittest.main()
