function auth() {
    try {
//        var url = "http://68.183.56.98:5000/auth";
        var url = "https://spreadsheetfunction.club/auth";
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
        var result = UrlFetchApp.getRequest(url, options);
        Logger.log(result)
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result)
        var data = JSON.parse(result);
        return data["access_token"]
    } catch (e) {
        Logger.log(e)
    }
}


/**
 * Returns the IPA of a sentence or a word in French.
 *
 * @param {sentence} input The sentence to convert into IPA.
 * @returns the IPA of a sentence.
 * @customfunction
 */

function IPA(sentence) {
        var url = "https://spreadsheetfunction.club/french_to_IPA";
        var jwt = auth()

//        payload = JSON.stringify(payload);
        var options = {
            "method": "post",
            "headers": {
//            "Content-Type" : "application/json", don't use this!!!
            "Authorization": "JWT " + jwt
            },
            "payload" : {
            "sentence" : sentence
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result)
        return result.getContentText()
    }

/**
 * Returns the translation of a sentence with deepL.
 *
 * @param {sentence;target language} input the sentence to translate.
 * @returns the translation of a sentence.
 * @customfunction
 */

function deeplapi(text, targetLanguage) {
        var authKey = "30928739-08ba-d7e5-6672-d90c2bd9fbb4";
        var url = "https://api.deepl.com/v2/translate";
        var options = {
            "method": "get",
            "payload" : {
            "text" : text,
            "target_lang" : targetLanguage,
            "auth_key" : authKey
            }
        };
        var resultJson = UrlFetchApp.fetch(url, options);
        Logger.log(result)
        var result = JSON.parse(resultJson);
        return result["translations"][0]["text"]
    }