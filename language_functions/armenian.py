import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def get_armenian_conjugation_table(url, language):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    h2_elements = soup.find_all('h2')
    tables = []
    list_navframes = []
    table_number = 0
    for h2_element in h2_elements:
        if h2_element.find('span', attrs={'id': language}):
            list_navframes = h2_element.find_next_siblings('div', attrs={'class': 'NavFrame'})
            # some verbs have a declension table before the conjugation table
            for element in h2_element.find_next_sibling('h4'):
                if element.text in ("Declension"):
                    table_number = 2
                # if element.find('span', attrs={'id': 'Declension'}):
                #     print("I'm here")
                #     table_number = 2
    for navframe in list_navframes:
        tables.append(pd.read_html(str(navframe))[0])
    return tables[table_number]


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
                     'aorist 1st singular': (15, 2),
                     'subjunctive future 1st singular': (17, 2),
                     'subjunctive future perfect 1st singular': (18, 2),
                     'imperative 2nd singular': (23, 3)
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
    conjugation_cell = conjugation_cell.split(", ")[0]
    return conjugation_cell


if __name__ == "__main__":

    # verb tests
    # print(conjugate('Armenian', 'խոսել', 'infinitive'))
    # print(conjugate('Armenian', 'խոսել', 'causative'))
    # print(conjugate('Armenian', 'խոսել', 'aorist stem'))
    # print(conjugate('Armenian', 'խոսել', 'future converb I'))
    # print(conjugate('Armenian', 'խոսել', 'connegative converb'))
    # print(conjugate('Armenian', 'զբաղվել', 'infinitive'))
    # print(conjugate('Armenian', 'զբաղվել', 'causative'))
    # print(conjugate('Armenian', 'զբաղվել', 'aorist stem'))
    # print(conjugate('Armenian', 'զբաղվել', 'future converb I'))
    # print(conjugate('Armenian', 'զբաղվել', 'connegative converb'))
    # print(conjugate('Armenian', 'ցանկանալ', 'infinitive'))
    # print(conjugate('Armenian', 'ցանկանալ', 'causative'))
    # print(conjugate('Armenian', 'ցանկանալ', 'aorist stem'))
    # print(conjugate('Armenian', 'ցանկանալ', 'future converb I'))
    # print(conjugate('Armenian', 'ցանկանալ', 'connegative converb'))
    # print(conjugate('Armenian', 'կարողանալ', 'infinitive'))
    # print(conjugate('Armenian', 'զբաղվել', 'infinitive'))
    # print(conjugate('Armenian', 'կարողանալ', 'aorist stem'))
    # print(conjugate('Armenian', 'կարողանալ', 'future converb I'))
    # print(conjugate('Armenian', 'կարողանալ', 'connegative converb'))
    print(conjugate('Armenian', 'լսել', 'aorist 1st singular'))
    print(conjugate('Armenian', 'լսել', 'imperative 2nd singular'))



    # other tests

    # armenian_conjugation_table = get_armenian_conjugation_table('https://en.wiktionary.org/wiki/%D5%AD%D5%B8%D5%BD%D5%A5%D5%AC', 'Armenian')
    # armenian_conjugation_table.to_csv('armenian_conjugation_table.csv')