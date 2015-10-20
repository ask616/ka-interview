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

def limitedInfection(users, target):
    sizes = users

    # Populate sizes array with sizes of classes and individual users
    # for user in users:
    #     if(len(user.students) > 0): # Is a teacher
    #         sizes.append(len(user.students))
    #     elif(user.teacher is None and len(user.students) == 0): # Is an individual user
    #         sizes.append(1)

    if sum(sizes) < target:
        raise ValueError("Target value is unreachable")

    sizes = [s for s in sizes if s <= target]

    n = len(users)

    subsetTable = {}

    for i in range(n):
        subsetTable[(i, 0)] = True

    for i in range(1, target + 1):
        subsetTable[(0, i)] = True if i == sizes[0] else False

    for i in range(1, n):
        for j in range(1, target + 1):
            if sizes[i] > j:
                subsetTable[(i, j)] = subsetTable[(i-1, j)]
            else:
                if subsetTable[(i-1, j)] == True:
                    subsetTable[(i, j)] = True
                else:
                    subsetTable[(i, j)] = subsetTable[(i-1, j-sizes[i])]

    subset = []

    row, col = n-1, target

    for i in range(n):
        out = ""
        for j in range(target+1):
            out += str(subsetTable[(i, j)])[0] + " "
        print(out.strip())


    while col > 0 and row > 0:
        while row >= 1 and subsetTable[(row-1, col)] == True:
            row -= 1
        subset.append(sizes[row])
        col -= sizes[row]

    return subset
