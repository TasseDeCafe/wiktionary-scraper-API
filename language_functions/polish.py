import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
from language_functions.all_language_functions import get_table

def eliminate_romanization(cell_with_romanization):
    cell_no_romanization = re.search("[а-яА-Яіу́]+", cell_with_romanization)[0]
    return cell_no_romanization


def set_url(language, verb, aspect):
    verb = urllib.parse.quote(verb, safe='')
    # some verbs have the name of the perfective form, but there is no page. We still want to get this verb even
    # if the conjugation can't be scraped.
    verb_of_other_aspect = None
    url = f'https://wiktionary.org/wiki/{verb}#{language}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.prettify())
    # check the abbr tag at the beginning of the conjugation table to determine if the input verb is pf or impf
    navhead_element = soup.find('div', attrs={'class': 'inflection-table-verb'})
    imperfective_abbr = navhead_element.find('abbr', attrs={'title': 'imperfective aspect'})
    perfective_abbr = navhead_element.find('abbr', attrs={'title': 'perfective aspect'})
    # the aspect of the input verb can be determined by the the abbr tag
    aspect_verb = 'imperfective'
    if perfective_abbr:
        aspect_verb = 'perfective'
    # some verbs have no abbr, like "byc" in Polish. In this case we assume that the verb is imperfective.
    if not perfective_abbr and not imperfective_abbr:
        return url, verb_of_other_aspect, aspect_verb
    elif (aspect == 'imperfective' and imperfective_abbr) or (aspect == 'perfective' and perfective_abbr):
        url = f'https://en.wiktionary.org/wiki/{verb}#{language}'
    elif aspect == 'imperfective' and not imperfective_abbr:
        imperfective_i = soup.find('i', text='imperfective')
        partial_url_impf = imperfective_i.find_next_sibling('b').find('a').attrs['href']
        url = f'https://en.wiktionary.org{partial_url_impf}'
        verb_of_other_aspect = imperfective_i.find_next_sibling('b').find('a').text
    elif aspect == 'perfective' and not perfective_abbr:
        perfective_i = soup.find('i', text='perfective')
        partial_url_perf = perfective_i.find_next_sibling('b').find('a').attrs['href']
        url = f'https://en.wiktionary.org{partial_url_perf}'
        verb_of_other_aspect = perfective_i.find_next_sibling('b').find('a').text

    return url, verb_of_other_aspect, aspect_verb

def locate_cell(conjugation_table, tense, person):
    # todo: refactor this, it is unreadable
    # find location of all cells that contain tense in the conjugation table
    location_list_tense = [
        (conjugation_table[col][conjugation_table[col].eq(tense)].index[i], conjugation_table.columns.get_loc(col)) for
        col in conjugation_table.columns for i in
        range(len(conjugation_table[col][conjugation_table[col].eq(tense)].index))]
    # find location of all cells that contain person in the conjugation table
    location_list_person = [
        (conjugation_table[col][conjugation_table[col].eq(person)].index[i], conjugation_table.columns.get_loc(col)) for
        col in conjugation_table.columns for i
        in range(len(conjugation_table[col][conjugation_table[col].eq(person)].index))]
    location_rows_person = [location[0] for location in location_list_person]
    location_conjugation = None
    for location in location_list_tense:
        # gives the location of a cell in a row where there is both the tense and the person
        if location[0] in location_rows_person:
            location_conjugation = location
            break
    return location_conjugation


def conjugate(language, verb, tense, person='', aspect="imperfective"):
    plural = False
    # some tenses don't have a person, so we set it to the value of tense so that the location algorithm below works
    if not person:
        person = tense
    if person and 'pl' in person.split():
        plural = True
        # the person number is always the first word of the variable person
        person = person.split()[0]
    url, verb_of_other_aspect, aspect_verb = set_url(language, verb, aspect)
    # if the aspect of the verb is different than the input aspect and the requested tense is the infinitive, we return
    # the verb of the other aspect if it exists.
    if verb_of_other_aspect and aspect_verb != aspect and tense == 'infinitive':
        return verb_of_other_aspect
    # locate the cell with the requested conjugation
    conjugation_table = get_table(url, language)
    location_conjugation = locate_cell(conjugation_table, tense, person)
    conjugation_cell = conjugation_table.iloc[location_conjugation[0]][location_conjugation[1] + 2]
    if plural:
        conjugation_cell = conjugation_table.iloc[location_conjugation[0]][location_conjugation[1] + 5]
    if not conjugation_cell:
        return 'No data.'
    return conjugation_cell


def decline_noun(language, noun, case, number):
    noun = urllib.parse.quote(noun, safe='')
    url = f'https://wiktionary.org/wiki/{noun}#{language}'
    table = get_table(url, language)
    # find the row that contains the string of the case
    declension_row = table[table['Unnamed: 0'].str.contains(case, na=False)]
    declension = None
    if number == 'singular':
        declension = declension_row.iloc[0][1]
    elif number == 'plural':
        declension = declension_row.iloc[0][2]
    return declension


def decline_adjective(language, adjective, case, gender_and_number):
    location_dict = {'m pers singular': (0, 1),
                     'm anim singular': (0, 1),
                     'm inan singular': (0, 2),
                     'n singular': (0, 3),
                     'f singular': (0, 4),
                     'm pers plural': (0, 5),
                     'other plural': (0, 6)}
    adjective = urllib.parse.quote(adjective, safe='')
    url = f'https://wiktionary.org/wiki/{adjective}#{language}'
    table = get_table(url, language)
    # I have no idea what this line does, but it removes an error when using str.contains
    table.columns = table.columns.get_level_values(0)
    declension_row = table[table['case'].str.contains(case, na=False)]
    declension = declension_row.iloc[location_dict[gender_and_number][0]][location_dict[gender_and_number][1]]
    return declension


if __name__ == "__main__":
    # Polish tests
    # print(conjugate("Polish", "spać", "infinitive", "infinitive", "perfective"))
    print(conjugate("Polish", "robić", "passive adjectival participle", aspect="perfective"))
    print(decline_noun('Polish', 'brat', 'instrumental', 'plural'))
    print(decline_adjective('Polish', 'niebieski', 'instrumental', 'm pers plural'))
    print(get_table('https://en.wiktionary.org/wiki/t%C5%82umaczy%C4%87', 'Polish'))