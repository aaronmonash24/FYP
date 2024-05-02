// Global variables to store dropdown bars
var dropdownCount = 0; // Initial dropdown count
var dropdownIds = []; // Array to store dropdown IDs

function addDropdown(fieldNames) {
    dropdownCount++;
    var newDropdownId = 'dropdown' + dropdownCount;
    dropdownIds.push(newDropdownId);
    
    var dropdownContainer = document.getElementById('dropdownContainer');
    var newDropdown = document.createElement('select');
    newDropdown.id = newDropdownId;
    
    // Add options to the dropdown based on fieldNames
    fieldNames.forEach(function(fieldName) {
        var option = document.createElement('option');
        option.value = fieldName;
        option.textContent = fieldName;
        newDropdown.appendChild(option);
    });
    
    dropdownContainer.appendChild(newDropdown);
}


// Function to remove the last dropdown bar
function removeDropdown() {
    if (dropdownCount > 0) {
        var lastDropdownId = dropdownIds.pop();
        var lastDropdown = document.getElementById(lastDropdownId);
        lastDropdown.remove();
        dropdownCount--;
    }
}

// Function to handle submission of selected fields
function submitSelection() {
    // Add functionality to handle selection submission
    var selectedFields = [];
    dropdownIds.forEach(function(dropdownId) {
        selectedFields.push(document.getElementById(dropdownId).value);
    });
    
    console.log('Selected fields:', selectedFields);
    closePopup(); // Close the popup after submission
}

// Function to open the popup
function openPopup() {
    document.getElementById('popup').style.display = 'block';
}

// Function to close the popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

// Function to populate the dropdown options based on field names
function createDropdownOptions(fieldNames) {
    var dropdownContainer = document.getElementById('dropdownContainer');
    
    // Clear existing dropdowns
    dropdownContainer.innerHTML = '';

    // Create options for dropdowns
    fieldNames.forEach(function(fieldName) {
        var newDropdown = document.createElement('select');
        var option = document.createElement('option');
        option.value = fieldName;
        option.textContent = fieldName;
        newDropdown.appendChild(option);
        dropdownContainer.appendChild(newDropdown);
    });
}

window.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var csvData = urlParams.get('data');
    if (csvData) {
        var parsedData = parseCSV(csvData);
        displayData(parsedData);
        createDropdownOptions(parsedData[0]); // Pass the first row (field names) to create dropdown options
    }
});
// Function to display data in the table
function displayData(data) {
    var table = document.getElementById('dataTable');
    var thead = table.querySelector('thead');
    var tbody = table.querySelector('tbody');

    // Clear existing content
    thead.innerHTML = '';
    tbody.innerHTML = '';

    // Add table headers
    var headerRow = document.createElement('tr');
    data[0].forEach(function(cell) {
        var th = document.createElement('th');
        th.textContent = cell;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Add table rows
    for (var i = 1; i < data.length; i++) {
        var row = data[i];
        var tr = document.createElement('tr');
        row.forEach(function(cell) {
            var td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    }
}

// Function to parse CSV data
function parseCSV(csvData) {
    var lines = csvData.split('\n');
    var data = [];
    lines.forEach(function(line) {
        data.push(line.split(','));
    });
    return data;
}

