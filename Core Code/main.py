class User(object):
    """
    Represents a single user, as a node in a graph.

    Various getters and setters are included for encapsulation.
    """
    def __init__(self, name, password, version="Production_1.1", teacher=None):
        self.username = name
        self.password = password
        self.teacher = None
        self.students = [] # Adjacency list in graph
        self.version = version

        if teacher is not None:
            self.addToClass(teacher)

    def addToClass(self, teacher):
        """
        Adds the user to the teacher's class by setting its teacher attribute
        to a reference to the teacher, and adding a reference to the user's
        object to the teacher's student list
        """
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
    """
    Implementation of Breadth-First search, which will traverse through the
    entire graph containing the user. A set called 'users' is maintained to
    keep track of which users have been visited already (set searches occur
    in constant time, hence their use here). The frontier is a list of all
    users that are currently adjacent to current set of users.
    """
    users = {user}
    frontier = [user]

    while frontier:
        next = []
        for usr in frontier:

            # Get teacher if exists
            if usr.teacher and usr.teacher not in users:
                next.append(usr.teacher)
                users.add(usr.teacher)

            # Get students if exist
            for student in usr.getStudents():
                if student not in users:
                    next.append(student)
                    users.add(student)

            # Get classmates if exist
            for classmate in usr.getClassmates():
                if classmate not in users:
                    next.append(classmate)
                    users.add(classmate)

        # The frontier will now be all these users that we have found
        frontier = next

    return users


def totalInfection(user, newVersion):
    """
    Performs total infection to update the version of every user found
    in the graph containing the target user. Uses BFS algorithm to find
    these users.
    """
    toInfect = BFS(user)

    for user in toInfect:
        user.setVersion(newVersion)

# Used for debugging
def printSubsetTable(table, n, target):
    for i in range(n):
        out = ""
        for j in range(target+1):
            out += str(table[(i, j)])[0] + " "
        print(out.strip())


def builtSubsetTruthTable(sizes, target, n):
    """
    Builds a boolean table that where each entry (i, j) represents whether or
    not sum(sizes[0:i]) will total j. The table overall will represent
    what subsets can be formed to create certain totals.
    """
    subsetTable = {}

    # First column is all True because the subset [] can always form 0
    for i in range(n):
        subsetTable[(i, 0)] = True

    # First row is true only when sizes[i] == j
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

    return subsetTable


def buildSubset(sizes, target, n, subsetTable):
    """
    Once the subset truth table is formed, it can be traversed starting from
    the bottom right corner to trace which values compose the subset that will
    sum to the intended total
    """
    subset = []

    row, col = n-1, target
    subsetTotal = 0

    while col > 0 and row >= 0:
        if(row == 0 and subsetTable[(row, col)] == True):
            subsetTotal += sizes[row][1]
            subset.append(sizes[row])
            break
        else:
            while row >= 1 and subsetTable[(row-1, col)] == True:
                row -= 1
            subset.append(sizes[row])
            col -= sizes[row][1]
            subsetTotal += sizes[row][1]
            row -= 1

    # If, after traversing, the total is not equal to the target, there is is
    # no subset that can sum to the target
    if subsetTotal != target:
        raise ValueError("Target value is unreachable")

    return subset


def limitedInfection(users, target, newVersion):
    """
    Performs limited infection to update the version of only the target number
    of users. This is related to the subset sum problem, which asks whether or
    not some subset of a list (in this cast, that of the sizes of each graph)
    can be summed to total the target.
    """
    sizes = []

    # Realistically, we would perhaps instead give all members of the same
    # graph an identical key, so that we could store that key in the
    # following set instead of each user.
    passed = set()

    sizeTotal = 0
    # Populate sizes array with sizes of classes and individual users
    for user in users:
        if user not in passed:
            userGraph = BFS(user)
            passed.update(userGraph)
            # Only need to store the first user in the graph to infect all of it
            sizes.append((next(iter(userGraph)), len(userGraph)))
            sizeTotal += len(userGraph)

    # If the total number of users is less than the target, the target is
    # impossible to reach.
    if sizeTotal < target:
        raise ValueError("Target value is unreachable")

    # Filter to remove graphs that have sizes larger than the target
    sizes = [s for s in sizes if s[1] <= target]

    n = len(sizes)

    subsetTable = builtSubsetTruthTable(sizes, target, n)

    subset = buildSubset(sizes, target, n, subsetTable)

    # If a subset is found, go through it and infect all the users in the
    # selected graphs
    for user in subset:
        totalInfection(user[0], newVersion)

    return subset
