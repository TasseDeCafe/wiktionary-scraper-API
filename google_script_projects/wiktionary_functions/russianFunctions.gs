/**
 * Returns the conjugation of a verb in Russian.
 *
 * @param {verb} input the verb to conjugate.
 * @param {tense} input the tense.
 * @param {person} input the person.
 * @param {aspect} input the aspect of the verb.
 * @returns the conjugation of a verb in Russian.
 * @customfunction
 */

function conjugateRussian(verb, tense, person, aspect) {
        var url = "http://kindledatabaseconverter.com/conjugate_russian";
        var jwt = auth()

//        payload = JSON.stringify(payload);
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "verb" : verb,
              "tense" : tense,
              "person" : person,
              "aspect" : aspect              
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }

/**
 * Returns the declination of a noun in Russian.
 *
 * @param {noun} input the noun to decline.
 * @param {noun_case} input the case.
 * @param {number} input the number.
 * @returns the declination of a noun in Russian.
 * @customfunction
 */

function declineRussianNoun(noun, noun_case, number) {
        var url = "http://kindledatabaseconverter.com/decline_russian_noun";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "noun" : noun,
              "noun_case" : noun_case,
              "number" : number       
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }

/**
 * Returns the declination of a noun in Russian.
 *
 * @param {adjective} input the adjective to decline.
 * @param {adjective_case} input the case.
 * @param {gender_and_number} input the gender and number.
 * @returns the declination of an adjective in Russian.
 * @customfunction
 */

function declineRussianAdjective(adjective, adjective_case, gender_and_number) {
        var url = "http://kindledatabaseconverter.com/decline_russian_adjective";
        var jwt = auth();
        var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "payload" : {
              "adjective" : adjective,
              "adjective_case" : adjective_case,
              "gender_and_number" : gender_and_number       
            }
        };
        var result = UrlFetchApp.fetch(url, options);
        Logger.log(result);
        return result.getContentText()
    }