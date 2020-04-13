// todo: add error handling and clean up the code

function onOpen() {
  // https://stackoverflow.com/questions/43594248/google-sheets-you-do-not-have-permission-to-call-appendrow
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Big List Generator')
      .addItem('Generate the new words', 'bigListGenerator')
  .addToUi();
}

function bigListGenerator() {

  // SpreadsheetApp.getUi().alert('Generating the list...');

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  var sheet = ss.getActiveSheet();
  var url = "http://kindledatabaseconverter.com/generate_biglist";
  var jwt = auth();
  var payload = convertRangeToJSON();

  var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "contentType": "application/json",
            "payload": payload
        };
  var result = UrlFetchApp.fetch(url, options);
  var biglist = JSON.parse(result.getContentText());
  var lastRow = sheet.getLastRow();
  Logger.log(lastRow);
  sheet.getRange(lastRow + 1, 1, biglist.length, 2).setValues(biglist);
}

function convertRangeToJSON() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  // var bigListSheet = spreadsheet.getSheetByName("Mandarin");
  var conversations = spreadsheet.getRange("Conversations!C:C").getValues();
  var bigList = spreadsheet.getRange("Mandarin!D:D").getValues();
  var mergedArrays = mergeArrays(conversations, bigList);
  return JSON.stringify(mergedArrays);
}

/* functions to merge the arrays */

function appendArrays() {
    var temp = [];
    for (var i = 0; i < arguments.length; i++) {
        temp.push(arguments[i]);
    }
    return temp;
}

function mergeArrays(firstArray, secondArray) {
    var merged = [];

    for (i = 0; i < maxLengthArrays(firstArray, secondArray); i++) {
        merged.push(appendArrays(firstArray[i], secondArray[i]));
    }
    return merged;
}

function maxLengthArrays(firstArray, secondArray) {
    if (firstArray.length >= secondArray.length) {
        return firstArray.length;
    } else {
        return secondArray.length;
    }
}