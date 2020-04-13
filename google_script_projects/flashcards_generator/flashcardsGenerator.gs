function onOpen() {
  // https://stackoverflow.com/questions/43594248/google-sheets-you-do-not-have-permission-to-call-appendrow
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Generate the flashcards')
  .addItem('Generate the flashcards', 'flashcardsGenerator')
  .addToUi();
}

function flashcardsGenerator() {

  // SpreadsheetApp.getUi().alert('Generating the list...');

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var url = "http://kindledatabaseconverter.com/generate_mandarin_flashcards";
  var jwt = auth();
  var sheetJson = convertSheet2Json(sheet);
  var payload = JSON.stringify(sheetJson);
  var options = {
            "method": "post",
            "headers": {
            "Authorization": "JWT " + jwt
            },
            "contentType": "application/json",
            "payload": payload
        };
  var response = UrlFetchApp.fetch(url, options);
  var flashcardsArray = JSON.parse(response.getContentText());
  var flashcardsSheet = ss.insertSheet();
  flashcardsSheet.setName(sheet.getName() + " flashcards");
  flashcardsSheet.getRange(1, 1, flashcardsArray.length, flashcardsArray[0].length).setValues(flashcardsArray);
}

function convertRangeToJSON() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  // var bigListSheet = spreadsheet.getSheetByName("Mandarin");
  var conversations = spreadsheet.getRange("Conversations!A:A").getValues();
  var bigList = spreadsheet.getRange("Mandarin!B:B").getValues();
  var mergedArrays = mergeArrays(conversations, bigList);
  return JSON.stringify(mergedArrays);
}