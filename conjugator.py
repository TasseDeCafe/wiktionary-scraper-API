import polish
import russian
import czech
import armenian
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from users_password import users

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

bad_request_or_no_data = 'BRDN'

# ******************* Polish functions *******************


@app.route('/conjugate_polish', methods=['POST'])
@jwt_required()
def conjugate_polish():
    language = 'Polish'
    verb = request.form['verb']
    tense = request.form['tense']
    person = request.form['person']
    aspect = request.form['aspect']
    try:
        conjugation_cell = polish.conjugate(language, verb, tense, person, aspect)
        return conjugation_cell
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_polish_noun', methods=['POST'])
@jwt_required()
def decline_polish_noun():
    language = 'Polish'
    noun = request.form['noun']
    # "case" is a reserved word in JS
    noun_case = request.form['noun_case']
    number = request.form['number']
    try:
        declined_noun = polish.decline_noun(language, noun, noun_case, number)
        return declined_noun
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_polish_adjective', methods=['POST'])
@jwt_required()
def decline_polish_adjective():
    language = 'Polish'
    adjective = request.form['adjective']
    adjective_case = request.form['adjective_case']
    gender_and_number = request.form['gender_and_number']
    try:
        declined_adjective = polish.decline_adjective(language, adjective, adjective_case, gender_and_number)
        return declined_adjective
    except Exception:
        return bad_request_or_no_data


# ******************* Russian functions *******************

@app.route('/conjugate_russian', methods=['POST'])
@jwt_required()
def conjugate_russian():
    language = 'Russian'
    verb = request.form['verb']
    tense = request.form['tense']
    person = request.form['person']
    aspect = request.form['aspect']
    try:
        conjugation_cell = russian.conjugate(language, verb, tense, person, aspect)
        return conjugation_cell
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_russian_noun', methods=['POST'])
@jwt_required()
def decline_russian_noun():
    language = 'Russian'
    noun = request.form['noun']
    # "case" is a reserved word in JS
    noun_case = request.form['noun_case']
    number = request.form['number']
    try:
        declined_noun = russian.decline_noun(language, noun, noun_case, number)
        return declined_noun
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_russian_adjective', methods=['POST'])
@jwt_required()
def decline_russian_adjective():
    language = 'Russian'
    adjective = request.form['adjective']
    adjective_case = request.form['adjective_case']
    gender_and_number = request.form['gender_and_number']
    try:
        declined_adjective = russian.decline_adjective(language, adjective, adjective_case, gender_and_number)
        return declined_adjective
    except Exception:
        return bad_request_or_no_data

# ******************* Czech functions *******************

@app.route('/conjugate_czech', methods=['POST'])
@jwt_required()
def conjugate_czech():
    language = 'Czech'
    verb = request.form['verb']
    tense = request.form['tense']
    person = request.form['person']
    aspect = request.form['aspect']
    try:
        conjugation_cell = czech.conjugate(language, verb, tense, person, aspect)
        return conjugation_cell
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_czech_noun', methods=['POST'])
@jwt_required()
def decline_czech_noun():
    language = 'Czech'
    noun = request.form['noun']
    # "case" is a reserved word in JS
    noun_case = request.form['noun_case']
    number = request.form['number']
    try:
        declined_noun = czech.decline_noun(language, noun, noun_case, number)
        return declined_noun
    except Exception:
        return bad_request_or_no_data

@app.route('/decline_czech_adjective', methods=['POST'])
@jwt_required()
def decline_czech_adjective():
    language = 'Czech'
    adjective = request.form['adjective']
    adjective_case = request.form['adjective_case']
    gender_and_number = request.form['gender_and_number']
    try:
        declined_adjective = czech.decline_adjective(language, adjective, adjective_case, gender_and_number)
        return declined_adjective
    except Exception:
        return bad_request_or_no_data

# ******************* Armenian functions *******************

@app.route('/conjugate_armenian', methods=['POST'])
@jwt_required()
def conjugate_armenian():
    language = 'Armenian'
    verb = request.form['verb']
    tense = request.form['tense']
    person = request.form['person']
    try:
        conjugation_cell = armenian.conjugate(language, verb, tense, person)
        return conjugation_cell
    except Exception:
        return bad_request_or_no_data

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
