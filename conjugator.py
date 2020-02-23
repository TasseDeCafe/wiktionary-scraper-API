from language_functions import conjugate, decline_noun, decline_adjective
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'sebastien', 'RDvNifgjtJ6p1DA')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.config['SECRET_KEY'] = '0075e7f61334ae26a0e0fd2be0e1f4dd4241a6291bffbec1d9c403c3b9f1'

jwt = JWT(app, authenticate, identity)


@app.route('/conjugate_polish', methods=['POST'])
@jwt_required()
def conjugate_polish():
    language = 'Polish'
    verb = request.form['verb']
    tense = request.form['tense']
    person = request.form['person']
    aspect = request.form['aspect']
    try:
        conjugation_cell = conjugate(language, verb, tense, person, aspect)
        return conjugation_cell
    except Exception:
        return 'Bad request or no data.'

@app.route('/decline_polish_noun', methods=['POST'])
@jwt_required()
def decline_polish_noun():
    language = 'Polish'
    noun = request.form['noun']
    # "case" is a reserved word in JS
    noun_case = request.form['noun_case']
    number = request.form['number']
    try:
        declined_noun = decline_noun(language, noun, noun_case, number)
        return declined_noun
    except Exception:
        return 'Bad request or no data.'

@app.route('/decline_polish_adjective', methods=['POST'])
@jwt_required()
def decline_polish_adjective():
    language = 'Polish'
    adjective = request.form['adjective']
    adjective_case = request.form['adjective_case']
    gender_and_number = request.form['gender_and_number']
    try:
        declined_adjective = decline_adjective(language, adjective, adjective_case, gender_and_number)
        return declined_adjective
    except Exception:
        return 'Bad request or no data.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
