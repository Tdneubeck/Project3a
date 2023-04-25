$("#inputFile").on("change", handleFile);

var renderCSVDropdown = function(csv) {
  var dropdown = $('#symbol');
  var elements = csv.split(",");
  for (var i = 0; i < elements.length; i++) {
    var record = elements[i];
    var entry = $('<option>', {value: record, text: record})
    dropdown.append(entry);
  }
};

function handleFile() {
    var file = $(this).prop('files')[0];
    var fileReader = new FileReader();
    fileReader.onload = function (evt) {
      renderCSVDropdown(evt.target.result);
    };
    fileReader.readAsText(file, "UTF-8");
}

$.get(csv_path, function(data) {
  var csv = CSVToArray(data);
  renderCSVDropdown(csv);
});



function CSVToArray(strData, strDelimiter) {

strDelimiter = (strDelimiter || ",");

var objPattern = new RegExp((
  "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

  "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

  "([^\"\\" + strDelimiter + "\\r\\n]*))"
), "gi");


var arrData = [
  []
];

var arrMatches = null;

while (arrMatches = objPattern.exec(strData)) {

  var strMatchedDelimiter = arrMatches[1];

  if (strMatchedDelimiter.length && strMatchedDelimiter !== strDelimiter) {

    arrData.push([]);

  }

  var strMatchedValue;

  if (arrMatches[2]) {

    strMatchedValue = arrMatches[2].replace(new RegExp("\"\"", "g"), "\"");

  } else {
    strMatchedValue = arrMatches[3];

  }

  arrData[arrData.length - 1].push(strMatchedValue);
}

return (arrData);
}