class User(object):

    def __init__(self, name, password, version="Production_1.1", teacher=None):
        self.username = name
        self.password = password
        self.teacher = None
        self.students = [] # Adjacency list in graph
        self.version = version

        if teacher is not None:
            self.addToClass(teacher)

    def addToClass(self, teacher):
        self.teacher = teacher
        teacher.students.append(self)

    def getVersion(self):
        return self.version

    def setVersion(self, newVersion):
        self.version = newVersion

    # Have only the teacher store their class, as having each user store their
    # classmates would be faster for retrieval, but would require more storage
    # and more update operations
    def getClassmates(self):
        if self.teacher is None:
            return []
        else:
            return self.teacher.students

    def getStudents(self):
        return self.students

    def __repr__(self):
        return 'User(username: %s, version: %s)' % (self.username, self.version)


# Breadth first search to traverse graph containing user
def totalInfection(user, newVersion):
    frontier = [user]

    while frontier:
        next = []
        for usr in frontier:
            usr.setVersion(newVersion) # Set new version for user

            # TODO: infect teacher
            # TODO: infect students
            for classmate in usr.getClassmates():
                if classmate.getVersion() != newVersion:
                    next.append(classmate)
        frontier = next

def findB(s, c):
    total, i = 0, 0
    while total <= c:
        total += s[i]
        i += 1
    return i

def wBar(s, b):
    total = 0
    for x in range(b):
        total += s[x]
    return total

def limitedInfection(users, target):
    # sizes = [len(user.students) if len(user.students) > 0 else (1 if user.teacher is None and len(user.students) == 0) for user in users]
    sizes = []
    for user in users:
        if(len(user.students) > 0):
            sizes.append(len(user.students))
        elif(user.teacher is None and len(user.students) == 0):
            sizes.append(1)
    return len(sizes)
