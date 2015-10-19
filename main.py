class User(object):

    def __init__(self, name, pass, version="Production 1.1"):
        self.username = name
        self.password = pass
        self.teacher = None
        self.students = [] # Adjacency list in graph
        self.version = version

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
            return None
        else:
            return self.teacher.students


# Breadth first search to traverse graph containing user
def totalInfection(user, newVersion):
    frontier = [user]

    while frontier:
        next = []
        for usr in frontier:
            usr.setVersion(newVersion) # Set new version for user
            for classmate in usr.getClassmates():
                if classmate.getVersion != newVersion:
                    next.append(classmate)
        frontier = next
