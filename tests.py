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
        self.basic_test_users = []
        self.coach_test_users = []

        NUM_CLASSES = 2
        STUDENTS_PER_CLASS = 5

        # Two separate classes with 1 teacher each
        for x in range(NUM_CLASSES):
            teacher = self.createUser("teacher_%d" % x)
            self.basic_test_users.append(teacher)
            for y in range(STUDENTS_PER_CLASS):
                self.basic_test_users.append(self.createUser("student_%d.%d" % (x, y), teacher))

        # Two separate classes, but the last student in the 2nd class coaches the 1st class's teacher
        for x in range(NUM_CLASSES):
            teacher = self.createUser("teacher_%d" % x)
            self.coach_test_users.append(teacher)
            for y in range(STUDENTS_PER_CLASS):
                self.coach_test_users.append(self.createUser("student_%d.%d" % (x, y), teacher))
        self.coach_test_users[0].addToClass(self.coach_test_users[11])

    def test_total_infection_basic_teacher_1(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.basic_test_users[0], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.basic_test_users, NEW_VERSION, 0, 6))

    def test_total_infection_basic_student_1(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.basic_test_users[1], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.basic_test_users, NEW_VERSION, 0, 6))

    def test_total_infection_basic_teacher_2(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.basic_test_users[6], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.basic_test_users, NEW_VERSION, 6, 12))

    def test_total_infection_basic_student_2(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.basic_test_users[7], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.basic_test_users, NEW_VERSION, 6, 12))

    def test_total_infection_coach_1(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.coach_test_users[0], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.coach_test_users, NEW_VERSION, 0, 12))

    def test_total_infection_coach_2(self):
        NEW_VERSION = "Test_0.1"
        main.totalInfection(self.coach_test_users[11], NEW_VERSION)

        self.assertTrue(self.isVersionChangedUserArray(self.coach_test_users, NEW_VERSION, 0, 12))

    # Exhaustive test
    def test_total_infection_coach_3(self):
        NEW_VERSION = "Test_0.1"

        for x in range(12):
            self.setUp()
            main.totalInfection(self.coach_test_users[5], NEW_VERSION)

            self.assertTrue(self.isVersionChangedUserArray(self.coach_test_users, NEW_VERSION, 0, 12))



if __name__ == '__main__':
    unittest.main()
