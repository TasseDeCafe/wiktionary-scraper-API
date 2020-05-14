import requests
from bs4 import BeautifulSoup
import deepcut


def thai_to_ipa(thai_text):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
        'anyx': thai_text,
        'submit1': 'go',
        'fmt': '2',
        'bullmode': '0'
    }

    url = 'http://www.thai-language.com/?nav=dictionary&anyxlit=1'
    session = requests.Session()
    r = session.post(url, headers=headers, data=payload)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    ipa = soup.find('span', attrs={'class': 'ipa'})
    return ipa.text


def tokenize_thai(thai_sentence):
    return " ".join(deepcut.tokenize(thai_sentence))


if __name__ == '__main__':
    print(thai_to_ipa('คิดว่าเราต้องเดาว่าอะไรเป็นของขวัญที่นิมชอบที่สุด'))
    print(tokenize_thai('คิดว่าเราต้องเดาว่าอะไรเป็นของขวัญที่นิมชอบที่สุด'))
