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
    return i - 1

def findWBar(s, b):
    total = 0
    for x in range(b):
        total += s[x]
    return total

def s_set(s_dict, u, val):
    s_dict[u] = val

def s_get(s_dict, u):
    return s_dict[u]

def limitedInfection(users, target):
    sizes = users
    s_t_minus_one = {}

    r = max(users)

    b = findB(users, target)

    wBar = findWBar(users, b)

    # Populate sizes array with sizes of classes and individual users
    # for user in users:
    #     if(len(user.students) > 0): # Is a teacher
    #         sizes.append(len(user.students))
    #     elif(user.teacher is None and len(user.students) == 0): # Is an individual user
    #         sizes.append(1)

    if sum(sizes) < target:
        raise ValueError("Target value is unreachable")

    sizes = [s for s in sizes if s <= target]

    
