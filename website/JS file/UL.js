
document.getElementById('filename').addEventListener('change', function() {
    var input = this;
    var output = document.getElementById('selectedFileName');
    if (input.files.length > 0) {
        var fileName = input.files[0].name;
        var truncatedName = fileName.length > 17 ? fileName.substring(0, 14) + "...csv" : fileName;
        output.textContent = truncatedName;
    } else {
        output.textContent = "";
    }
});


