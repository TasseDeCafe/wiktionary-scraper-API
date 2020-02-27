import pandas as pd
import urllib.parse
import requests
from bs4 import BeautifulSoup


def get_czech_declination_table(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    navframe = None
    h2_elements = soup.find_all('h2')
    for h2_element in h2_elements:
        if h2_element.find('span', attrs={'id': 'Czech'}):
            navframe = h2_element.find_next_siblings('div', attrs={'class': 'NavFrame'})
    tables_scraped = pd.read_html(str(navframe))
    return tables_scraped[0]


def get_czech_conjugation_table(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    div_containing_table = None
    h2_elements = soup.find_all('h2')
    for h2_element in h2_elements:
        if h2_element.find('span', attrs={'id': 'Czech'}):
            list_divs = h2_element.find_next_siblings('div')
            for div in list_divs:
                if div.find('div', attrs={'class': 'NavFrame'}):
                    div_containing_table = div
    tables_scraped = pd.read_html(str(div_containing_table))
    return tables_scraped


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
    navhead_element = soup.find('strong', attrs={'class': 'Latn headword', 'lang': 'cs'})
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
                     'present tense 1st': (2, 1),
                     'present tense 2nd': (3, 1),
                     'present tense 3rd': (4, 1),
                     'present tense 1st pl': (2, 2),
                     'present tense 2nd pl': (3, 2),
                     'present tense 3rd pl': (4, 2),
                     'imperative 2nd': (3, 3),
                     'imperative 1st pl': (2, 4),
                     'imperative 2nd pl': (3, 4),
                     'past participle masculine animate': (8, 1),
                     'past participle masculine inanimate': (9, 1),
                     'past participle feminine': (10, 1),
                     'past participle neuter': (11, 1),
                     'past participle masculine animate pl': (8, 2),
                     'past participle masculine inanimate pl': (9, 2),
                     'past participle feminine pl': (10, 2),
                     'past participle neuter pl': (11, 2),
                     'passive participle masculine animate': (8, 3),
                     'passive participle masculine inanimate': (9, 3),
                     'passive participle feminine': (10, 3),
                     'passive participle neuter': (11, 3),
                     'passive participle masculine animate pl': (8, 4),
                     'passive participle masculine inanimate pl': (9, 4),
                     'passive participle feminine pl': (10, 4),
                     'passive participle neuter pl': (11, 4),
                     'transgressive present masculine': (13, 1),
                     'transgressive present feminine': (14, 1),
                     'transgressive present neuter': (14, 1),
                     'transgressive present plural': (15, 1),
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
    if aspect_verb == 'imperfective' and aspect == 'imperfective' and tense == 'infinitive':
        return verb
    # locate the cell with the requested conjugation
    conjugation_tables = get_czech_conjugation_table(url)
    conjugation_table = pd.concat(conjugation_tables, ignore_index=True)
    location_conjugation = locate_cell(tense, person)
    conjugation_cell = conjugation_table.iloc[location_conjugation[0]][location_conjugation[1]]
    if not conjugation_cell:
        return 'No data.'
    return conjugation_cell


def decline_noun(language, noun, case, number):
    noun = urllib.parse.quote(noun, safe='')
    url = f'https://wiktionary.org/wiki/{noun}#{language}'
    table = get_czech_declination_table(url)
    table.to_csv('sestra.csv')
    # find the row that contains the string of the case
    declension_row = table[table['Unnamed: 0'].str.contains(case, na=False)]
    declension = None
    if number == 'singular':
        declension = declension_row.iloc[0][1]
    elif number == 'plural':
        declension = declension_row.iloc[0][2]
    return declension


def decline_adjective(language, adjective, case, gender_and_number):
    location_dict = {'nominative masculine': (0, 1),
                     'nominative neuter': (0, 4),
                     'nominative feminine': (0, 3),
                     'nominative masculine animate plural': (8, 1),
                     'nominative masculine inanimate plural': (8, 2),
                     'nominative neuter plural': (8, 4),
                     'nominative feminine plural': (8, 3),
                     'genitive masculine': (1, 1),
                     'genitive neuter': (1, 4),
                     'genitive feminine': (1, 3),
                     'genitive masculine animate plural': (9, 1),
                     'genitive masculine inanimate plural': (9, 2),
                     'genitive neuter plural': (9, 4),
                     'genitive feminine plural': (9, 3),
                     'dative masculine': (2, 1),
                     'dative neuter': (2, 4),
                     'dative feminine': (2, 3),
                     'dative masculine animate plural': (10, 1),
                     'dative masculine inanimate plural': (10, 2),
                     'dative neuter plural': (10, 4),
                     'dative feminine plural': (10, 3),
                     'accusative masculine animate': (3, 1),
                     'accusative neuter': (3, 4),
                     'accusative feminine': (3, 3),
                     'accusative masculine inanimate': (3, 2),
                     'accusative masculine animate plural': (11, 1),
                     'accusative masculine inanimate plural': (11, 2),
                     'accusative neuter plural': (11, 4),
                     'accusative feminine plural': (11, 3),
                     'instrumental masculine': (6, 1),
                     'instrumental neuter': (6, 4),
                     'instrumental feminine': (6, 3),
                     'instrumental masculine animate plural': (14, 1),
                     'instrumental masculine inanimate plural': (14, 2),
                     'instrumental neuter plural': (14, 4),
                     'instrumental feminine plural': (14, 3),
                     'vocative masculine': (4, 1),
                     'vocative neuter': (4, 4),
                     'vocative feminine': (4, 3),
                     'vocative masculine animate plural': (12, 1),
                     'vocative masculine inanimate plural': (12, 2),
                     'vocative neuter plural': (12, 4),
                     'vocative feminine plural': (12, 3),
                     'locative masculine': (5, 1),
                     'locative neuter': (5, 4),
                     'locative feminine': (5, 3),
                     'locative masculine animate plural': (13, 1),
                     'locative masculine inanimate plural': (13, 2),
                     'locative neuter plural': (13, 4),
                     'locative feminine plural': (13, 3),
                     }
    adjective = urllib.parse.quote(adjective, safe='')
    url = f'https://wiktionary.org/wiki/{adjective}#{language}'
    table = get_czech_declination_table(url)
    search_key = f'{case} {gender_and_number}'.strip()
    declension = table.iloc[location_dict[search_key][0]][location_dict[search_key][1]]
    declension = declension
    return declension


if __name__ == "__main__":

    # verb tests
    # print(set_url('Czech', 'jíst', 'perfective'))
    # print(conjugate('Czech', 'jíst', 'infinitive', '', 'perfective'))
    # print(conjugate('Czech', 'jíst', 'infinitive', '', 'imperfective'))
    # print(conjugate('Czech', 'jíst', 'present tense', '1st', 'imperfective'))
    # print(conjugate('Czech', 'jíst', 'transgressive present', 'plural', 'imperfective'))
    # print(conjugate('Czech', 'jíst', 'imperative', '2nd pl', 'imperfective'))
    # print(conjugate('Czech', 'jíst', 'past participle', 'neuter', 'imperfective'))

    # adjective tests
    # print(decline_adjective('Czech', 'impozantní', 'genitive', 'neuter'))
    # print(decline_adjective('Czech', 'impozantní', 'instrumental', 'feminine plural'))
    # print(decline_adjective('Czech', 'pěkný', 'instrumental', 'masculine inanimate plural'))
    # print(decline_adjective('Czech', 'pěkný', 'accusative', 'masculine inanimate'))
    # print(decline_adjective('Czech', 'pěkný', 'dative', 'neuter'))

    # noun tests
    print(decline_noun('Czech', 'sestra', 'instrumental', 'plural'))
    print(decline_noun('Czech', 'sestra', 'accusative', 'singular'))
    print(decline_noun('Czech', 'sestra', 'vocative', 'singular'))
    print(decline_noun('Czech', 'sestra', 'dative', 'plural'))

    # other tests
    # print(get_czech_noun_declination_table('https://en.wiktionary.org/wiki/sestra#Czech'))
    # print(get_czech_conjugation_table('https://en.wiktionary.org/wiki/j%C3%ADst'))