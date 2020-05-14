/**
 * Returns the tokenized version of a text in Thai.
 *
 * @param {thai_text} input the text to tokenize.
 * @returns the tokenized version of a text in Thai.
 * @customfunction
 */

function tokenizeThai(thai_text) {
        var url = "http://kindledatabaseconverter.com/tokenize_thai";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "thai_text" : thai_text,
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }