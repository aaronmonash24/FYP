window.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var csvData = urlParams.get('data');
    if (csvData) {
        var parsedData = parseCSV(csvData);
        displayData(parsedData);
    }
});

function parseCSV(csvData) {
    // Parse CSV data and return as an array of arrays
    // Example implementation:
    var lines = csvData.split('\n');
    var data = [];
    lines.forEach(function(line) {
        data.push(line.split(','));
    });
    return data;
}

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


// Sample data
const products = [
    { id: 1, name: "Product A", category: "Category X" },
    { id: 2, name: "Product B", category: "Category Y" },
    // Add more sample data
];

// Function to populate the table with data
function populateTable(data) {
    const table = document.getElementById("dataTable");
    // Clear previous data
    table.innerHTML = "";
    // Add table headers
    const headers = Object.keys(data[0]);
    const headerRow = table.insertRow();
    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header.toUpperCase();
        headerRow.appendChild(th);
    });
    // Add table data
    data.forEach(item => {
        const row = table.insertRow();
        headers.forEach(header => {
            const cell = row.insertCell();
            let value = item[header];
            if (header === "Gender" && !value) {
                value = item["Organization Country"]; // Fill missing Gender with Organization Country
            }
            cell.textContent = value || '-';
            
        });
    });
}



// Function to filter data based on search input
function filterData(searchValue, filterBy) {
    const filteredData = products.filter(product => {
        return product[filterBy].toLowerCase().includes(searchValue.toLowerCase());
    });
    populateTable(filteredData);
}

// Event listener for search input
document.getElementById("searchInput").addEventListener("input", function() {
    const searchValue = this.value.trim();
    const filterBy = document.getElementById("filterDropdown").value;
    filterData(searchValue, filterBy);
});

// Function to show pop-up
function showPopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "block";
    // Customize pop-up content and functionality as needed
}

// Function to close pop-up
function closePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "none";
}
