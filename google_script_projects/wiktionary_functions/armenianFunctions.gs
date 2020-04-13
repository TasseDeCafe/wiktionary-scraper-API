/**
 * Returns the conjugation of a verb in Armenian.
 *
 * @param {verb} input the verb to conjugate.
 * @param {tense} input the tense.
 * @param {person} input the person.
 * @returns the conjugation of a verb in Armenian.
 * @customfunction
 */

function conjugateArmenian(verb, tense, person, aspect) {
        var url = "http://kindledatabaseconverter.com/conjugate_armenian";
        var jwt = auth()
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "verb" : verb,
              "tense" : tense,
              "person" : person
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result)
        return result.getContentText()
    }