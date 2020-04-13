# みらい翻訳をコマンドラインから利用する
# スクリプトを使うには、以下の2つのパッケージをインストールしてください。
# インストール方法
# pipenv install
# 使い方を見る
# pipenv run python mirai.py
# 使い方の例
# pipenv run python mirai.py JA EN こんにちは

import sys
from time import sleep
import chromedriver_binary
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

def mirai_translate(text, source_language, target_language):

    LANGS = {
       'JA': '日本語',
       'EN': '英語',
       'CH': '中国語',
       'IT': 'イタリア語',
       'ES': 'スペイン語',
       'DE': 'ドイツ語',
       'FR': 'フランス語',
       'PT': 'ポルトガル語',
       'RU': 'ロシア語'
    }

    options = ChromeOptions()
    options.add_argument('--headless')
    driver = Chrome(options=options, executable_path='/usr/bin/chromedriver')

    driver.get('https://miraitranslate.com/trial/')

    assert 'みらい翻訳' in driver.title

    # 原文言語を設定する。
    lang = LANGS[source_language]
    arrows = driver.find_elements_by_css_selector('.select2-selection__arrow')
    arrows[0].click()
    options = driver.find_elements_by_css_selector('.select2-results__option')
    for option in options:
        if lang == option.text:
            option.click()
            break
    else:
        print('Source language is not supported. Supported languages are:', file=sys.stderr)
        for option in options:
            print(option.text, file=sys.stderr)
        sys.exit()

    sleep(1)  # 何かを待たないと下記arrowsが取得できない

    # 訳文言語を設定する。
    lang = LANGS[target_language]
    arrows = driver.find_elements_by_css_selector('.select2-selection__arrow')  # 上で取得したarrowsを使うと失敗する
    arrows[1].click()
    options = driver.find_elements_by_css_selector('.select2-results__option')
    for option in options:
        if lang == option.text:
            option.click()
            break
    else:
        print('Target language is not supported. Supported languages are:', file=sys.stderr)
        for option in options:
            print(option.text, file=sys.stderr)
        sys.exit()

    source = driver.find_element_by_id('translateSourceInput')
    source.send_keys(text)

    button = driver.find_element_by_id('translateButtonTextTranslation')
    button.click()

    sleep(3)  # 待つ

    # スクリーンショットを撮る。
    # driver.save_screenshot('debug.png')

    # 検索結果を表示する。
    result = driver.find_element_by_id('translate-text')
    driver.quit()  # ブラウザーを終了する。
    return result.text

if __name__ == '__main__':
    text = '検索結果を表示する'
    print(mirai_translate(text, 'JA', 'EN'))