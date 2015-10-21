from flask import Flask,request, render_template
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
    resp = requests.get(FIREBASE_URL).json()

    return json.dumps(setAdjacencies(resp))


@app.route('/addUser/', methods=['POST'])
def addUser():

    form = request.get_json()

    username = form['username']
    password = form['password']
    teacher = form['teacher']
    version = form['version']

    newUser = createUser(username, password, teacher, version)

    req = requests.post(FIREBASE_URL, data = newUser)

    return req.text


@app.route('/totalInfection/', methods=['POST'])
def totalInfection():

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

    if sizeTotal < target:
        return "Target value is unreachable"

    # Filter to remove graphs that have sizes larger than the target
    sizes = [s for s in sizes if s[1] <= target]

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
        return "Target value is unreachable"

    for user in subset:
        toInfect = BFS(user[0], users)

        for usr in toInfect:
            users[usr]['version'] = newVersion

    req = requests.patch(FIREBASE_URL, data = json.dumps(users))
    return req.text



##################
# Helper methods #
##################

def createUser(username, password, teacher, version):
    user = {}
    user['username'] = username
    user['password'] = password
    user['teacher'] = teacher
    user['students'] = '[]'
    user['version'] = version

    return json.dumps(user)


def BFS(user, dbData):
    users = {user}
    frontier = [user]

    while frontier:
        next = []
        for usr in frontier:

            # Get teacher
            if dbData[usr]['teacher'] != 'None' and dbData[usr]['teacher'] not in users:
                next.append(dbData[usr]['teacher'])
                users.add(dbData[usr]['teacher'])

            # Get students
            for student in eval(dbData[usr]['students']):
                if student not in users:
                    next.append(student)
                    users.add(student)

            classmates = []
            if dbData[usr]['teacher'] != 'None':
                classmates = eval(dbData[dbData[usr]['teacher']]['students'])

            # Get classmates
            for classmate in classmates:
                if classmate not in users:
                    next.append(classmate)
                    users.add(classmate)

        frontier = next

    return users


def setAdjacencies(resp):
    for (key, data) in resp.items():
        adjacency = []
        if data['teacher'] != 'None':
            classmates = resp[data['teacher']]['students'] # Array will be a string
            adjacency += (eval(classmates))
            adjacency.append(data['teacher'])

        # Check if has students
        students = eval(data['students'])
        if len(students) > 0:
            adjacency += students

        resp[key].update({'adjacencies' : adjacency})

    return resp



###################
#    Start app    #
###################

if __name__ == "__main__":
    app.run(debug=True)
