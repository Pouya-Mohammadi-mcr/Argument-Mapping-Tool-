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
            self.db.deleteArgument(argID)
        self.assertEqual(argument['title'], "some text for the test argument")

    def testCreateArgumentAndRelation(self):
        with self.app.app_context():
            relatedElement = self.db.createArgumentAndRelation("Pouya","some text for the second test argument", 6, "Supports")
            relatedElementID = relatedElement.id
            #delete the argument created
            self.db.deleteArgument(relatedElementID)
        self.assertEqual(relatedElement.id, 6)


if __name__ == '__main__':
    unittest.main()
