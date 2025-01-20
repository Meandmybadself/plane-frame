import Papa from 'papaparse';

async function fetchAndConvertAirports() {
  try {
    // Fetch the CSV data
    const response = await fetch('https://raw.githubusercontent.com/davidmegginson/ourairports-data/refs/heads/main/airports.csv');
    const csvContent = await response.text();
    
    // Convert to JSON
    const jsonOutput = await convertCSVtoJSON(csvContent);
    
    // Output or use the JSON as needed
    console.log(JSON.stringify(jsonOutput, null, 2));
    return jsonOutput;
  } catch (error) {
    console.error('Error fetching or converting data:', error);
    throw error;
  }
}

async function convertCSVtoJSON(csvContent) {
  return new Promise((resolve, reject) => {
    Papa.parse(csvContent, {
      header: true,
      skipEmptyLines: true,
      complete: function(results) {
        const jsonOutput = {};
        
        const excludedTypes = ['closed', 'helipad', 'heliport'];
        
        results.data.forEach(row => {
          // Only process rows with an ident and not in excluded types
          if (row.ident && !excludedTypes.includes(row.type)) {
            jsonOutput[row.ident] = {
              type: row.type,
              name: row.name,
              latitude_deg: parseFloat(row.latitude_deg) || null,
              longitude_deg: parseFloat(row.longitude_deg) || null
            };
          }
        });
        
        resolve(jsonOutput);
      },
      error: function(error) {
        reject(error);
      }
    });
  });
}

// Usage:
fetchAndConvertAirports()
  .then(json => {
    // Do something with the JSON data
    console.log(`Converted ${Object.keys(json).length} airports`);
  })
  .catch(error => {
    console.error('Failed to process airports:', error);
  });