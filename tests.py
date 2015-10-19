import unittest
import main

class totalInfectionTest(unittest.TestCase):

    def createUser(self, name, teacher=None):
        TEST_PW = "correct horse battery staple"
        if teacher is None:
            return main.User(name, TEST_PW)
        else:
            return main.User(name, TEST_PW, teacher=teacher)

    def isVersionChangedUser(self, user, newVersion):
        return user.getVersion() == newVersion

    def isVersionChangedUserArray(self, users, newVersion, start, end):
        return False not in [self.isVersionChangedUser(user, newVersion) for user in users[start:end]]

    def setUp(self):
        self.users = []

        NUM_CLASSES = 2
        STUDENTS_PER_CLASS = 20

        for x in range(NUM_CLASSES):
            teacher = self.createUser("teacher_%d" % x)

            for y in range(STUDENTS_PER_CLASS):
                self.users.append(self.createUser("student_%d.%d" % (x, y), teacher))

    def test_total_infection(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.users[0], NEW_VERSION)
        print(self.users)
        self.assertTrue(self.isVersionChangedUserArray(self.users, NEW_VERSION, 0, 2))

if __name__ == '__main__':
    unittest.main()
