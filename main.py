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

def BFS(user):
    users = set()
    frontier = [user]

    while frontier:
        next = []
        for usr in frontier:

            # Get teacher
            if usr.teacher and usr.teacher not in users:
                next.append(usr.teacher)
                users.add(usr.teacher)

            # Get students
            for student in usr.getStudents():
                if student not in users:
                    next.append(student)
                    users.add(student)

            # Get classmates
            for classmate in usr.getClassmates():
                if classmate not in users:
                    next.append(classmate)
                    users.add(teacher)

        frontier = next

    return users

# Breadth first search to traverse graph containing user
def totalInfection(user, newVersion):
    # frontier = [user]
    #
    # while frontier:
    #     next = []
    #     for usr in frontier:
    #         usr.setVersion(newVersion) # Set new version for user
    #
    #         # Infect teacher
    #         if self.teacher and self.teacher.getVersion() != newVersion:
    #             next.append(teacher)
    #
    #         # Infect students
    #         for student in self.getStudents():
    #             if student.getVersion() != newVersion:
    #                 next.append(student)
    #
    #         # Infect classmates
    #         for classmate in usr.getClassmates():
    #             if classmate.getVersion() != newVersion:
    #                 next.append(classmate)
    #
    #     frontier = next
    toInfect = BFS(user)

    for user in toInfect:
        user.setVersion(newVersion)

def printSubsetTable(table, n, target):
    for i in range(n):
        out = ""
        for j in range(target+1):
            out += str(table[(i, j)])[0] + " "
        print(out.strip())

def limitedInfection(users, target, newVersion):

    sizes = []

    # Realistically, we would perhaps instead give all members of the same
    # graph an identical key, so that we could store that key in the
    # following set instead of each user.
    passed = set()

    # Populate sizes array with sizes of classes and individual users
    for user in users:
        if user not in passed:
            userGraph = BFS(user)
            passed.update(userGraph)
            # Only need to store the first user in the graph to infect all of it
            # sizesDict[next(iter(userGraph))] = len(userGraph)
            sizes.append((next(iter(userGraph))), len(userGraph))

    if sum(sizesDict.values()) < target:
        raise ValueError("Target value is unreachable")

    # Filter to remove graphs that have sizes larger than the target
    sizes = {s for s in sizes if s[1] <= target}

    n = len(sizes)

    subsetTable = {}

    for i in range(n):
        subsetTable[(i, 0)] = True

    for i in range(1, target + 1):
        subsetTable[(0, i)] = True if i == sizes[0][1] else False

    for i in range(1, n):
        for j in range(1, target + 1):
            if sizes[i][1] > j:
                subsetTable[(i, j)] = subsetTable[(i-1, j)]
            else:
                if subsetTable[(i-1, j)] == True:
                    subsetTable[(i, j)] = True
                else:
                    subsetTable[(i, j)] = subsetTable[(i-1, j-sizes[i][1])]

    subset = []

    row, col = n-1, target
    subsetTotal = 0
    while col > 0 and row > 0:
        while row >= 1 and subsetTable[(row-1, col)] == True:
            row -= 1
        subset.append(sizes[row])
        col -= sizes[row][1]
        subsetTotal += sizes[row][1]

    if subsetTotal != target:
        raise ValueError("Target value is unreachable")

    for user in subset:
        limitedInfection(user[0], newVersion)

    return subset
