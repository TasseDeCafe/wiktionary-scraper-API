# /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import http.client
import http.client
from hashlib import md5
import urllib
import random
import traceback
import json
from translator_wrappers.setting import (API_URL, APP_ID, BASE_URL, SECRET_KEY)


# *** Baidu translate ***


class Translator(object):
    def __init__(self):
        pass

    def translate(self, from_lang, to_lang, query_text):
        httpClient = None
        url = self.get_url(from_lang, to_lang, query_text)
        try:
            # API HTTP请求
            httpClient = http.client.HTTPConnection(BASE_URL)
            httpClient.request('GET', url)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result = json.loads(response.read())
            result_list = []
            for ret in result["trans_result"]:
                result_list.append(ret["dst"])
            trans_result = "".join(result_list)
            return trans_result
        except Exception as e:
            traceback.print_exc()
        finally:
            if httpClient:
                httpClient.close()

    @staticmethod
    def get_url(from_lang, to_lang, query_text):
        # 随机数据
        salt = random.randint(32768, 65536)
        # MD5生成签名
        sign = APP_ID + query_text + str(salt) + SECRET_KEY
        m1 = md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        # 拼接URL
        url = API_URL + '?appid=' + APP_ID + '&q=' + urllib.parse.quote(
            query_text) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign
        return url


# *** Mirai translate ***


def get_token(session):
    response = session.get("http://miraitranslate.com/trial/")
    soup = BeautifulSoup(response.content, "html.parser")
    tran = soup.find("input", {"name": "tran"})["value"]
    return tran


def mirai_translate(original_text, source_language, target_language, session):
    tran = get_token(session)
    params = {
        "input": original_text,
        "profile": "nmt",
        "kind": "nmt",
        "bt": "false",
        "tran": tran,
        "source": source_language.lower(),
        "target": target_language.lower()
    }
    response = session.get("https://miraitranslate.com/trial/translate.php", params=params).json()
    if response["status"] != "success":
        return "Response Error!"
    else:
        return response["outputs"][0]["output"]


if __name__ == "__main__":
    # Mirai translate tests
    s = requests.session()
    print(mirai_translate('I am a cat, not a dog.', 'EN', 'JA', s))
    # Baidu translate tests
    translator = Translator()
    print(translator.translate('EN', 'jp', 'I am a huge cat.'))
