import unittest
import main

class totalInfectionTest(unittest.TestCase):

    def createUser(self, name, teacher=None):
        TEST_PW = "correct horse battery staple"
        if teacher is None:
            return main.User(name, TEST_PW)
        else:
            return main.User(name, TEST_PW, teacher=teacher)

    def setUp(self):
        self.users = []

        NUM_CLASSES = 10
        STUDENTS_PER_CLASS = 2

        for x in range(NUM_CLASSES):
            teacher = self.createUser("teacher_" + str(x))

            for y in range(STUDENTS_PER_CLASS):
                self.users.append(self.createUser("student_%d.%d" % (x, y), teacher))

    def test_test(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
