import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
from language_functions.all_language_functions import get_table


def remove_romanization(cell_with_romanization):
    cell_no_romanization = re.search("[а-яА-Яіу́ё ]+", cell_with_romanization)[0]
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
    navhead_element = soup.find('strong', attrs={'class': 'Cyrl headword', 'lang': 'ru'})
    imperfective_abbr = navhead_element.find_next_sibling('span', attrs={'class': 'gender'}).find('abbr', attrs={'title': 'imperfective aspect'})
    perfective_abbr = navhead_element.find_next_sibling('span', attrs={'class': 'gender'}).find('abbr', attrs={'title': 'perfective aspect'})
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


def locate_cell(tense, person):
    location_dict = {'infinitive': (0, 1),
                     'present tense active participle': (2, 1),
                     'present tense passive participle': (3, 1),
                     'present tense adverbial participle': (4, 1),
                     'past tense active participle': (2, 2),
                     'past tense passive participle': (3, 2),
                     'past tense adverbial participle': (4, 2),
                     'present tense 1st': (6, 1),
                     'present tense 2nd': (7, 1),
                     'present tense 3rd': (8, 1),
                     'present tense 1st pl': (9, 1),
                     'present tense 2nd pl': (10, 1),
                     'present tense 3rd pl': (11, 1),
                     'future tense 1st': (6, 2),
                     'future tense 2nd': (7, 2),
                     'future tense 3rd': (8, 2),
                     'future tense 1st pl': (9, 2),
                     'future tense 2nd pl': (10, 2),
                     'future tense 3rd pl': (11, 2),
                     'imperative': (13, 1),
                     'imperative pl': (13, 2),
                     'past tense masculine': (15, 1),
                     'past tense feminine': (16, 1),
                     'past tense neuter': (17, 1),
                     'past tense pl': (16, 2),
    }

    search_key = f'{tense} {person}'.strip()
    location_conjugation = location_dict[search_key]
    return location_conjugation


def conjugate(language, verb, tense, person='', aspect="imperfective"):
    url, verb_of_other_aspect, aspect_verb = set_url(language, verb, aspect)
    # if the aspect of the verb is different than the input aspect and the requested tense is the infinitive, we return
    # the verb of the other aspect if it exists.
    if verb_of_other_aspect and aspect_verb != aspect and tense == 'infinitive':
        return verb_of_other_aspect
    # locate the cell with the requested conjugation
    conjugation_table = get_table(url, language)
    location_conjugation = locate_cell(tense, person)
    conjugation_cell = conjugation_table.iloc[location_conjugation[0]][location_conjugation[1]]
    conjugation_cell = remove_romanization(conjugation_cell)
    if not conjugation_cell:
        return 'No data.'
    return conjugation_cell


def decline_noun(language, noun, case, number):
    noun = urllib.parse.quote(noun, safe='')
    url = f'https://wiktionary.org/wiki/{noun}#{language}'
    table = get_table(url, language)
    table.to_csv('брат.csv')
    # find the row that contains the string of the case
    declension_row = table[table['Unnamed: 0'].str.contains(case, na=False)]
    declension = None
    if number == 'singular':
        declension = declension_row.iloc[0][1]
    elif number == 'plural':
        declension = declension_row.iloc[0][2]
    return remove_romanization(declension)


def decline_adjective(language, adjective, case, gender_and_number):
    location_dict = {'nominative masculine': (0, 2),
                     'nominative neuter': (0, 3),
                     'nominative feminine': (0, 4),
                     'nominative plural': (0, 5),
                     'genitive masculine': (1, 2),
                     'genitive neuter': (1, 3),
                     'genitive feminine': (1, 4),
                     'genitive plural': (1, 5),
                     'dative masculine': (2, 2),
                     'dative neuter': (2, 3),
                     'dative feminine': (2, 4),
                     'dative plural': (2, 5),
                     'accusative masculine animate': (3, 2),
                     'accusative neuter': (3, 3),
                     'accusative feminine': (3, 4),
                     'accusative plural animate': (3, 5),
                     'accusative masculine inanimate': (4, 2),
                     'accusative plural inanimate': (4, 5),
                     'instrumental masculine': (5, 2),
                     'instrumental neuter': (5, 3),
                     'instrumental feminine': (5, 4),
                     'instrumental plural': (5, 5),
                     'prepositional masculine': (6, 2),
                     'prepositional neuter': (6, 3),
                     'prepositional feminine': (6, 4),
                     'prepositional plural': (6, 5),
                     'short form masculine': (6, 2),
                     'short form neuter': (6, 3),
                     'short form feminine': (6, 4),
                     'short form plural': (6, 5)
                     }
    adjective = urllib.parse.quote(adjective, safe='')
    url = f'https://wiktionary.org/wiki/{adjective}#{language}'
    table = get_table(url, language)
    search_key = f'{case} {gender_and_number}'.strip()
    declension = table.iloc[location_dict[search_key][0]][location_dict[search_key][1]]
    declension = remove_romanization(declension).strip()
    return declension


if __name__ == "__main__":

    # verb tests
    print(set_url('Russian', 'уходить', 'perfective'))
    print(conjugate('Russian', 'уходить', 'infinitive', '', 'perfective'))
    print(conjugate('Russian', 'уходить', 'infinitive', '', 'imperfective'))
    print(conjugate('Russian', 'уходить', 'present tense', '1st', 'imperfective'))
    print(conjugate('Russian', 'уходить', 'present tense', '1st pl', 'imperfective'))
    print(conjugate('Russian', 'уходить', 'future tense', '2nd pl', 'imperfective'))
    # print(conjugate('Russian', 'уходить', 'imperative', 'pl', 'imperfective'))
    # print(conjugate('Russian', 'уходить', 'past tense', 'neuter', 'imperfective'))

    # adjective tests
    # print(decline_adjective('Russian', 'впечатлённый', 'prepositional', 'plural'))
    # print(decline_adjective('Russian', 'глянцевый', 'instrumental', 'plural'))
    # print(decline_adjective('Russian', 'глянцевый', 'short form', 'feminine'))
    # print(decline_adjective('Russian', 'съедобный', 'accusative', 'masculine inanimate'))
    # print(decline_adjective('Russian', 'съедобный', 'dative', 'neuter'))

    # noun tests
    # print(decline_noun('Russian', 'брат', 'instrumental', 'plural'))
    # print(decline_noun('Russian', 'брат', 'accusative', 'singular'))
    # print(decline_noun('Russian', 'брат', 'vocative', 'singular'))
    print(decline_noun('Russian', 'брат', 'dative', 'plural'))