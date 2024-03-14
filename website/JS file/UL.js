document.getElementById('filename').addEventListener('change', function() {
    var input = this;
    if (input.files.length > 0) {
        var file = input.files[0];
        var reader = new FileReader();
        
        reader.onload = function(event) {
            var csvData = event.target.result;
            sessionStorage.setItem('csvData', csvData); // Store CSV data in session storage
            window.location.href = 'PC.html'; // Redirect to PC.html
        };
        
        reader.readAsText(file);
    }
});


