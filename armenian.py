import pandas as pd
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re


def get_armenian_conjugation_table(url, language):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    h2_elements = soup.find_all('h2')
    tables = []
    list_navframes = []
    for h2_element in h2_elements:
        if h2_element.find('span', attrs={'id': language}):
            list_navframes = h2_element.find_next_siblings('div', attrs={'class': 'NavFrame'})
    for navframe in list_navframes:
        tables.append(pd.read_html(str(navframe))[0])
    return tables[0]


def locate_cell(tense, person):
    location_dict = {'infinitive': (0, 2),
                     'passive': (1, 2),
                     'causative': (2, 2),
                     'aorist stem': (3, 2),
                     'resultative participle': (4, 2),
                     'subject participle': (5, 2),
                     'imperfective converb': (0, 6),
                     'simultaneous converb': (1, 6),
                     'perfective converb': (2, 6),
                     'future converb I': (3, 6),
                     'future converb II': (4, 6),
                     'connegative converb': (5, 6),
    }

    search_key = f'{tense} {person}'.strip()
    location_conjugation = location_dict[search_key]
    return location_conjugation


def conjugate(language, verb, tense, person=''):
    url = f'https://wiktionary.org/wiki/{verb}'
    # locate the cell with the requested conjugation
    conjugation_table = get_armenian_conjugation_table(url, language)
    location_conjugation = locate_cell(tense, person)
    conjugation_cell = conjugation_table.iloc[location_conjugation[0]][location_conjugation[1]]
    if not conjugation_cell:
        return 'No data.'
    # remove the romanization in parentheses
    conjugation_cell = re.sub(r'\([^)]*\)', '', conjugation_cell).strip()
    return conjugation_cell



if __name__ == "__main__":

    # verb tests
    print(conjugate('Armenian', 'խոսել', 'infinitive'))
    print(conjugate('Armenian', 'խոսել', 'causative'))
    print(conjugate('Armenian', 'խոսել', 'aorist stem'))
    print(conjugate('Armenian', 'խոսել', 'future converb I'))
    print(conjugate('Armenian', 'խոսել', 'connegative converb'))


    # other tests
    # print(get_armenian_conjugation_table('https://en.wiktionary.org/wiki/%D5%AD%D5%B8%D5%BD%D5%A5%D5%AC', 'խոսել'))