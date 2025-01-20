const fs = require('fs');
const csv = require('csv-parse');
const https = require('https');

// URL of the CSV file
const csvUrl = 'https://raw.githubusercontent.com/elmoallistair/datasets/refs/heads/main/airlines.csv';

// Function to fetch and process the CSV data
https.get(csvUrl, (response) => {
  let data = '';

  // Collect the data chunks
  response.on('data', (chunk) => {
    data += chunk;
  });

  // Process the complete data
  response.on('end', () => {
    // Parse CSV data
    csv.parse(data, {
      columns: true,
      skip_empty_lines: true,
      trim: true
    }, (err, records) => {
      if (err) {
        console.error('Error parsing CSV:', err);
        return;
      }

      // Create object with ICAO as key and Name as value
      const airlines = records.reduce((acc, record) => {
        // Only include records with valid ICAO codes (not empty or N/A)
        if (record.ICAO && record.ICAO !== 'N/A') {
          acc[record.ICAO] = record.Name;
        }
        return acc;
      }, {});

      // Write to JSON file
      fs.writeFile('airlines.json', JSON.stringify(airlines, null, 2), 'utf8', (err) => {
        if (err) {
          console.error('Error writing JSON file:', err);
          return;
        }
        console.log('Successfully created airlines.json');
      });
    });
  });

}).on('error', (err) => {
  console.error('Error fetching CSV:', err);
});