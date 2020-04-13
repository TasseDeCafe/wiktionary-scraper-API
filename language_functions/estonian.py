import requests
from bs4 import BeautifulSoup
import pandas as pd


def conjugate(verb, tense):
    headers = {"Host": "www.eki.ee",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    url = f'http://www.eki.ee/dict/efi/index.cgi?Q={verb}&F=M&C06=en'
    request = requests.get(url, headers=headers)
    html_soup = BeautifulSoup(request.text, 'html.parser')
    div_attributes = html_soup.find('div', attrs={'class': 'mmumm'}).attrs
    data_guid = div_attributes['data-guid']
    conjugation_table_url = f'http://www.eki.ee/dict/efi/paradigma.cgi?G={data_guid}&M={verb}'
    request_conjugation_table = requests.get(conjugation_table_url, headers=headers)
    conjugation_table = pd.read_html(request_conjugation_table.text)[0]
    conjugation_table.columns = ['tense', 'conjugation']
    conjugation_table = conjugation_table.set_index('tense')
    return conjugation_table.loc[tense, 'conjugation']


if __name__ == '__main__':
    # tests
    print(conjugate('tegema', 'ind pr sg 3'))
    print(conjugate('tegema', 'ind pr impers'))
    print(conjugate('tegema', 'ind imperf sg 1'))
    print(conjugate('tegema', 'ind imperf sg 3'))
    print(conjugate('tegema', 'imperat pr sg 3'))
    print(conjugate('tegema', 'ma-infinitiiv'))
    print(conjugate('tegema', 'da-infinitiiv'))
    print(conjugate('tegema', 'tud-partitsiip'))
