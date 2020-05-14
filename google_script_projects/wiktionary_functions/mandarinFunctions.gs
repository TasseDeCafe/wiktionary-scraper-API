/**
 * Returns the pinyin of a text in Mandarin Chinese.
 *
 * @param {sentence} input the sentence to tokenize.
 * @returns the pinyin version of a sentence in Mandarin Chinese.
 * @customfunction
 */

function pinyin(sentence) {
        var url = "http://kindledatabaseconverter.com/pinyin";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "sentence" : sentence,
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }