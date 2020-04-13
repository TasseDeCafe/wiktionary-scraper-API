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
    try {
        var url = "http://kindledatabaseconverter.com/baidu_translate";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
                "Authorization": "JWT " + jwt
            },
            "payload": {
                "sourceText": sourceText,
                "sourceLanguage": sourceLanguage,
                "targetLanguage": targetLanguage
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    } catch (e) {
        Logger.log(e)
    }
}

/**
 * Returns the translation of a text with Mirai.
 *
 * @param {sourceText} input the text to translate.
 * @param {sourceLanguage} input the source language.
 * @param {targetLanguage} input the target language.
 * @returns the translation of the text in the target language.
 * @customfunction
 */

function miraiTranslate(sourceText, sourceLanguage, targetLanguage) {
    try {
        var url = "http://kindledatabaseconverter.com/mirai_translate";
    var jwt = auth();
    var options = {
        "method": "post",
        "headers": {
            "Authorization": "JWT " + jwt
        },
        "payload": {
            "sourceText": sourceText,
            "sourceLanguage": sourceLanguage,
            "targetLanguage": targetLanguage
        }
    };
    var result = UrlFetchApp.fetch(url, options);
    Logger.log(result);
    return result.getContentText()
    } catch (e) {
        Logger.log(e)
    }

}