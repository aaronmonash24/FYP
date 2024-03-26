document.getElementById('selectFileButton').addEventListener('click', function() {
    document.getElementById('filename').click();
});


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

document.getElementById('uploadButton').addEventListener('click', function() {
    var fileInput = document.getElementById('filename');
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var reader = new FileReader();
        
        reader.onload = function(event) {
            var csvData = event.target.result;
            sessionStorage.setItem('csvData', csvData); // Store CSV data in session storage
            window.location.href = 'PC.html'; // Redirect to PC.html
        };
        
        reader.readAsText(file);
    } else {
        // Display a message to the user to select a file
        alert('Please select a file.');
    }
});
