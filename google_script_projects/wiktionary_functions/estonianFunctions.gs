/**
 * Returns the conjugation of a verb in Estonian.
 *
 * @param {verb} input the verb to conjugate.
 * @param {tense} input the tense.
 * @returns the conjugation of a verb in Estonian.
 * @customfunction
 */

function conjugateEstonian(verb, tense) {
        var url = "http://kindledatabaseconverter.com/conjugate_estonian";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "verb" : verb,
              "tense" : tense
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }