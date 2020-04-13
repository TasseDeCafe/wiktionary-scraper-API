import http.client
import hashlib
import json
import urllib
import random
from translator_wrappers.baidu_api import Translator

# source: https://blog.csdn.net/LCYong_/article/details/79068636

def baidu_translate(content, source_language, target_language):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + source_language + '&to=' + target_language + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return dst
    except Exception as e:
        return e
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    # content = 'Je parle français.'
    # print(baidu_translate(content, 'fr', 'jp'))
    translator = Translator()
    print(translator.translate('en', 'jp', 'I am a cat.'))