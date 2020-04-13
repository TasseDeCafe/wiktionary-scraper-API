import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    print(thai_to_ipa('คิดว่าเราต้องเดาว่าอะไรเป็นของขวัญที่นิมชอบที่สุด'))
