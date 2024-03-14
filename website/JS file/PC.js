// display.js
document.addEventListener('DOMContentLoaded', function() {
    const csvData = sessionStorage.getItem('csvData');
    if (csvData) {
        displayCSVData(csvData);
        sessionStorage.removeItem('csvData'); // Remove CSV data from session storage
    }
});

function displayCSVData(csvData) {
    const table = document.getElementById('csvTable');
    const rows = csvData.split('\n');
    rows.forEach(function(row) {
        const cells = row.split(',');
        const tableRow = document.createElement('tr');
        cells.forEach(function(cell) {
            const tableCell = document.createElement('td');
            tableCell.textContent = cell;
            tableRow.appendChild(tableCell);
        });
        table.appendChild(tableRow);
    });
}
