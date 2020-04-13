function auth() {
    try {
        var url = "http://kindledatabaseconverter.com/auth";
        var payload = {
            username: "sebastien",
            password: "RDvNifgjtJ6p1DA"
        };

        payload = JSON.stringify(payload);
        var options = {
            method: "post",
            contentType: "application/json",
            payload: payload
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        var data = JSON.parse(result);
        return data["access_token"]
    } catch (e) {
        Logger.log(e)
    }
}

/**
 * Returns the translation of a text with Baidu
 *
 * @param {sourceText} input the text to translate.
 * @param {sourceLanguage} input the source language.
 * @param {targetLanguage} input the target language.
 * @returns the translation of the text in the target language.
 * @customfunction
 */

function baiduTranslate(sourceText, sourceLanguage, targetLanguage) {
        var url = "http://kindledatabaseconverter.com/baidu_translate";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "sourceText" : sourceText,
              "sourceLanguage" : sourceLanguage,
              "targetLanguage" : targetLanguage
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }
