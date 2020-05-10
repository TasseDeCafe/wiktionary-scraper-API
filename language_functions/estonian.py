import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_table(word):
    headers = {"Host": "www.eki.ee",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    url = f'http://www.eki.ee/dict/efi/index.cgi?Q={word}&F=M&C06=en'
    request = requests.get(url, headers=headers)
    html_soup = BeautifulSoup(request.text, 'html.parser')
    div_attributes = html_soup.find('div', attrs={'class': 'mmumm'}).attrs
    data_guid = div_attributes['data-guid']
    table_url = f'http://www.eki.ee/dict/efi/paradigma.cgi?G={data_guid}&M={word}'
    request_table = requests.get(table_url, headers=headers)
    table = pd.read_html(request_table.text)[0]
    return table


def conjugate_verb(verb, tense):
    conjugation_table = get_table(verb)
    conjugation_table.columns = ['tense', 'conjugation']
    conjugation_table = conjugation_table.set_index('tense')
    return conjugation_table.loc[tense, 'conjugation']


def decline_noun(noun, case):
    declination_table = get_table(noun)
    declination_table.columns = ['case', 'declination']
    declination_table = declination_table.set_index('case')
    return declination_table.loc[case, 'declination']


def decline_adjective(adjective, case):
    declination_table = get_table(adjective)
    declination_table.columns = ['case', 'declination']
    declination_table = declination_table.set_index('case')
    return declination_table.loc[case, 'declination']

if __name__ == '__main__':
    # tests
    # print(conjugate_verb('tegema', 'ind pr sg 3'))
    # print(conjugate_verb('tegema', 'ind pr impers'))
    # print(conjugate_verb('tegema', 'ind imperf sg 1'))
    # print(conjugate_verb('tegema', 'ind imperf sg 3'))
    # print(conjugate_verb('tegema', 'imperat pr sg 3'))
    # print(conjugate_verb('tegema', 'ma-infinitiiv'))
    # print(conjugate_verb('tegema', 'da-infinitiiv'))
    # print(conjugate_verb('tegema', 'tud-partitsiip'))
    # example of noun: vesi
    print(decline_noun('vesi', 'sg genitiiv'))
    # example of adjective: eestlane
    print(decline_adjective('eestlane', 'sg partitiiv'))
    print(decline_adjective('eestlane', 'sg illatiiv'))
