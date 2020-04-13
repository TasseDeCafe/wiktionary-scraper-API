function getLastRowSpecial(range){
  var rowNum = 0;
  var blank = false;
  for(var row = 0; row < range.length; row++){

    if(range[row][0] === "" && !blank){
      rowNum = row;
      blank = true;
    }else if(range[row][0] !== ""){
      blank = false;
    };
  };
  return rowNum;
};

function convertSheet2Json(sheet) {
  // first line(title)
  var firstRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  var firstRowValues = firstRange.getValues();
  Logger.log(firstRowValues);
  var titleColumns = firstRowValues[0];

  // after the second line(data)
  var columnToCheck = sheet.getRange("B:B").getValues();
  var lastRow = getLastRowSpecial(columnToCheck);
  var rowValues = [];
  for(var rowIndex=2; rowIndex<=lastRow; rowIndex++) {
    var colStartIndex = 1;
    var rowNum = 1;
    var range = sheet.getRange(rowIndex, colStartIndex, rowNum, sheet.getLastColumn());
    var values = range.getValues();
    rowValues.push(values[0]);
  }

  // create json
  var jsonArray = [];
  for(var i=0; i<rowValues.length; i++) {
    var line = rowValues[i];
    var json = new Object();
    for(var j=0; j<titleColumns.length; j++) {
      json[titleColumns[j]] = line[j];
    }
    jsonArray.push(json);
  }
  return jsonArray;
}

function test() {

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("29/03/2020");
  var payload = convertSheet2Json(sheet);
  Logger.log(payload);
}