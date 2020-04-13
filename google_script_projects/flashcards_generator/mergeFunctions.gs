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