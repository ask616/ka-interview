from flask import request, render_template
from flask.ext.api import FlaskAPI
import requests
import json

FIREBASE_URL = "https://ka-interview.firebaseio.com/users.json/"

app = FlaskAPI(__name__)



##################
#     Routes     #
##################

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/users")
def users():
    data = {"key" : "value"}

    resp = requests.get(FIREBASE_URL).json()

    for (key, data) in resp.items():
        adjacency = []
        if data['teacher'] != 'None':
            classmates = resp[data['teacher']] # Array will be a string
            adjacency.append(eval(classmates))
            adjacency.append(data['teacher'])

        # Check if has students
        students = eval(data['students'])
        if len(students) > 0:
            adjacency += students

        resp[key].update({'adjacencies' : adjacency})

    return resp


@app.route('/example/', methods=['GET', 'POST'])
def example():
    print('nice')
    print(request.args['hello'])
    return {'request data': request.args}


@app.route('/addUser', methods=['POST'])
def addUser():
    username = request.args['username']
    password = request.args['password']
    teacher = request.args['teacher']
    version = request.args['version']

    newUser = createUser(username, apssword, teacher, version)



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



###################
#    Start app    #
###################

if __name__ == "__main__":
    app.run(debug=True)
