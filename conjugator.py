import polish
import russian
import czech
import armenian
import estonian
import requests
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from users_password import users
import thai_to_ipa
import japanese
import pandas as pd
from big_list_generator.big_list_generator import generate_big_list
from mandarin_flashcard_generator.mandarin_flashcard_generator import generate_dataframe

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


# ******************* Thai functions *******************

@app.route('/thai_to_ipa', methods=['POST'])
@jwt_required()
def send_ipa():
    thai_text = request.form['thai_text']
    try:
        ipa = thai_to_ipa.thai_to_ipa(thai_text)
        return ipa
    except Exception:
        return bad_request_or_no_data


# ******************* Japanese functions *******************


@app.route('/baidu_translate', methods=['POST'])
@jwt_required()
def send_baidu_translation():
    source_text = request.form['sourceText']
    source_language = request.form['sourceLanguage']
    target_language = request.form['targetLanguage']
    try:
        translator = japanese.Translator()
        translation = translator.translate(source_language, target_language, source_text)
        return translation
    except Exception:
        return bad_request_or_no_data


@app.route('/mirai_translate', methods=['POST'])
@jwt_required()
def send_mirai_translation():
    source_text = request.form['sourceText']
    source_language = request.form['sourceLanguage']
    target_language = request.form['targetLanguage']
    try:
        session = requests.session()
        translation = japanese.mirai_translate(source_text, source_language, target_language, session)
        return translation
    except Exception:
        return bad_request_or_no_data


# ******************* Estonian functions *******************


@app.route('/conjugate_estonian', methods=['POST'])
@jwt_required()
def conjugate_estonian():
    language = 'Polish'
    verb = request.form['verb']
    tense = request.form['tense']
    try:
        conjugation_cell = estonian.conjugate(verb, tense)
        return conjugation_cell
    except Exception:
        return bad_request_or_no_data


# ******************* Chinese functions *******************

@app.route('/generate_biglist', methods=['GET', 'POST'])
@jwt_required()
def send_big_list():
    json_array = request.json
    chinese_big_list = []
    chinese_sentences_column = []
    for element in json_array:
        try:
            chinese_sentences_column.append(element[0][0])
        # exception handling is necessary because some elements are None and cannot be subscripted
        except TypeError:
            chinese_sentences_column.append('')
        try:
            chinese_big_list.append(element[1][0])
        except TypeError:
            chinese_big_list.append('')
    # each row is a list of lists: [[el_1], [el_2]]. We "flatten" so it becomes like this: [el_1, el_2]
    flattened_json = []
    for element in json_array:
        row = []
        for cell in element:
            try:
                row.append(cell[0])
            except TypeError:
                row.append('')
        flattened_json.append(row)
    # create the dataframe with the resulting json
    df = pd.DataFrame(flattened_json, columns=['Chinese sentence', 'Chinese keyword'])
    # generate the dataframe to send back to google sheets
    dataframe_to_send = generate_big_list(df)
    dataframe_to_send_json = dataframe_to_send.to_json(orient='values')
    return dataframe_to_send_json


@app.route('/generate_mandarin_flashcards', methods=['GET', 'POST'])
@jwt_required()
def generate_mandarin_flashcards():
    json_array = request.json
    print(json_array)
    mandarin_lesson_dataframe = pd.DataFrame.from_dict(json_array, orient='columns')
    flashcards_dataframe = generate_dataframe(mandarin_lesson_dataframe)
    flashcards_dataframe.to_csv('flashcards_dataframe.csv')
    flashcards_dataframe_json = flashcards_dataframe.to_json(orient='values')
    print(flashcards_dataframe_json)
    return flashcards_dataframe_json


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
