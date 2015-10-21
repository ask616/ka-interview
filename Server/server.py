from flask import Flask, request, render_template
import requests
import json

FIREBASE_URL = "https://ka-interview.firebaseio.com/users.json/"

app = Flask(__name__)


##################
#     Routes     #
##################

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/users/", methods=['GET'])
def users():
    """
    Returns a list of all users in the database
    """
    resp = requests.get(FIREBASE_URL).json()

    return json.dumps(setAdjacencies(resp))


@app.route('/totalInfection/', methods=['POST'])
def totalInfection():
    """
    Performs total infection to update the version of every user found
    in the graph containing the target user. Uses BFS algorithm to find
    these users.
    """
    form = request.get_json()

    infectedUser = form['infectedUser']
    newVersion = form['newVersion']

    users = requests.get(FIREBASE_URL).json()

    toInfect = BFS(infectedUser, users)

    for user in toInfect:
        users[user]['version'] = newVersion

    req = requests.patch(FIREBASE_URL, data = json.dumps(users))

    return json.dumps(setAdjacencies(eval(req.text)))


@app.route('/limitedInfection/', methods=['POST'])
def limitedInfection():
    """
    Performs limited infection to update the version of only the target number
    of users. This is related to the subset sum problem, which asks whether or
    not some subset of a list (in this cast, that of the sizes of each graph)
    can be summed to total the target.
    """
    form = request.get_json()

    target = int(form['target'])
    newVersion = form['newVersion']

    users = requests.get(FIREBASE_URL).json()

    sizes = []

    # Realistically, we would perhaps instead give all members of the same
    # graph an identical key, so that we could store that key in the
    # following set instead of each user.
    passed = set()

    sizeTotal = 0
    # Populate sizes array with sizes of classes and individual users
    for user in users:
        if user not in passed:
            userGraph = BFS(user, users)
            passed.update(userGraph)
            # Only need to store the first user in the graph to infect all of it
            sizes.append((next(iter(userGraph)), len(userGraph)))
            sizeTotal += len(userGraph)

    # If the total number of users is less than the target, the target is
    # impossible to reach.
    if sizeTotal < target:
        return "Target value is unreachable"

    # Filter to remove graphs that have sizes larger than the target
    sizes = [s for s in sizes if s[1] <= target]

    n = len(sizes)

    subsetTable = builtSubsetTruthTable(sizes, target, n)

    subset = buildSubset(sizes, target, n, subsetTable)

    # If a subset is found, go through it and infect all the users in the
    # selected graphs
    for user in subset:
        toInfect = BFS(user[0], users)

        for usr in toInfect:
            users[usr]['version'] = newVersion

    req = requests.patch(FIREBASE_URL, data = json.dumps(users))
    return req.text



##################
# Helper methods #
##################

def BFS(user, dbData):
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
            if dbData[usr]['teacher'] != 'None' and dbData[usr]['teacher'] not in users:
                next.append(dbData[usr]['teacher'])
                users.add(dbData[usr]['teacher'])

            # Get students if exist
            for student in eval(dbData[usr]['students']):
                if student not in users:
                    next.append(student)
                    users.add(student)

            classmates = []
            if dbData[usr]['teacher'] != 'None':
                classmates = eval(dbData[dbData[usr]['teacher']]['students'])

            # Get classmates if exist
            for classmate in classmates:
                if classmate not in users:
                    next.append(classmate)
                    users.add(classmate)

        # The frontier will now be all these users that we have found
        frontier = next

    return users


def setAdjacencies(resp):
    """
    Takes the response JSON from Firebase and adds a field to each user
    containing a list of all adjacent users in their graph, including
    teachers, classmates, and students.
    """
    for (key, data) in resp.items():
        adjacency = []
        if data['teacher'] != 'None':
            classmates = resp[data['teacher']]['students'] # Array will be a string
            adjacency += (eval(classmates)) # Add classmates to adjacency list
            adjacency.append(data['teacher']) # Add teacher to the adjacency list

        # Check if has students
        students = eval(data['students'])
        if len(students) > 0:
            adjacency += students

        resp[key].update({'adjacencies' : adjacency})

    return resp


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
        return "Target value is unreachable"

    return subset



###################
#    Start app    #
###################

if __name__ == "__main__":
    app.run(debug=True)
