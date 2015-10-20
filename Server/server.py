from flask import request, render_template
from flask.ext.api import FlaskAPI
import requests
import json

FIREBASE_URL = "https://ka-interview.firebaseio.com/users.json/"

app = FlaskAPI(__name__)


@app.route("/")
def home():
    data = {"key" : "value"}
    r = requests.post(FIREBASE_URL, data = json.dumps(data))
    print(r)
    print(requests.get(FIREBASE_URL).json())
    return render_template('index.html')

@app.route('/example/', methods=['GET', 'POST'])
def example():




    print('nice')
    print(request.args)
    return {'request data': request.args}


if __name__ == "__main__":
    app.run()

##################
# Helper methods #
##################

def createUser(username, password, teacher, students, version):
    user = {}
    user['username'] = username
    user['password'] = password
    user['teacher'] = 'None' if teacher is None else teacher
    user['students'] = students
    user['version'] = version
