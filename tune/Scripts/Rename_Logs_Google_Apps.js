// Main function to check and process new files
function checkNewFiles() {
  var folderId = 'YOUR_FOLDER_ID'; // Your folder ID
  var folder = DriveApp.getFolderById(folderId);
  Logger.log("Checking for new files in folder: " + folderId);

  var files = folder.getFiles();
  while (files.hasNext()) {
    var file = files.next();
    Logger.log("Found file: " + file.getName());

    if (!file.getName().startsWith('simos')) { // Only process files starting with "simos"
      Logger.log(`Skipping file ${file.getName()} as it does not start with "simos"`);
      continue;
    }

    Logger.log("Processing file: " + file.getName());
    renameCsvWithRpm(file.getId());
  }
}

// Function to rename the CSV file based on its content
function renameCsvWithRpm(fileId) {
  try {
    var file = DriveApp.getFileById(fileId);
    var fileName = file.getName();
    
    Logger.log(`Processing CSV file: ${fileName}`);

    var csvData = Utilities.parseCsv(file.getBlob().getDataAsString());
    Logger.log(`CSV Data: ${JSON.stringify(csvData)}`);

    var headers = csvData[0];
    var rpmIndex = headers.findIndex(header => /RPM/i.test(header));
    var gearIndex = headers.findIndex(header => /Gear/i.test(header));
    var tuneIndex = headers.findIndex(header => /SimosTools/i.test(header));

    if (rpmIndex === -1) {
      Logger.log(`Skipping file ${fileName} as no column containing 'RPM' was found`);
      return;
    }

    var rpmValues = csvData.slice(1).map(row => parseInt(row[rpmIndex], 10)); // Truncate RPM values
    Logger.log(`RPM Values: ${rpmValues}`);
    var minRpm = padStart(Math.floor(Math.min(...rpmValues) / 100), 2);
    var maxRpm = padStart(Math.floor(Math.max(...rpmValues) / 100), 2);
    var rpmPart = `${minRpm}-${maxRpm}`;
    Logger.log(`RPM values extracted: min ${minRpm}, max ${maxRpm}`);

    var gearPart = '';
    if (gearIndex !== -1) {
      var gearValues = csvData.slice(1).map(row => parseInt(row[gearIndex], 10)).filter(val => val !== 0);
      if (gearValues.length > 0) {
        var minGear = Math.min(...gearValues);
        var maxGear = Math.max(...gearValues);
        gearPart = (minGear !== maxGear) ? `${minGear}-${maxGear}` : `${maxGear}`;
      }
    }
    Logger.log(`Gear values extracted: ${gearPart}`);

    var tuneName = '';
    if (tuneIndex !== -1) {
      var tuneField = headers[tuneIndex];
      Logger.log(`Debug: tune_field type: ${typeof tuneField}, content: ${tuneField}`);
      var match = tuneField.match(/:([^:]+)\.bin/);
      tuneName = match ? match[1] : '';
    }
    Logger.log(`Tune name extracted: ${tuneName}`);

    var patterns = [
      /(\d{4}[-_]\d{2}[-_]\d{2})[-_](\d{2}[-_]\d{2}[-_]\d{2})/,
      /(\d{8})[-_](\d{6})/,
      /(\d{8})(\d{6})/
    ];

    var result = null;
    for (var pattern of patterns) {
      result = fileName.match(pattern);
      if (result) break;
    }

    var date = '';
    var time = '';
    if (result) {
      date = result[1].replace(/[_-]/g, '');
      time = result[2].replace(/[_-]/g, '');
    }
    Logger.log(`Extracted date: ${date}, time: ${time}`);

    var extension = fileName.split('.').pop();
    var newFileName = `${tuneName}_${gearPart}_${rpmPart}HRPM_${date}_${time}.${extension}`;
    Logger.log(`Renaming file to: ${newFileName}`);

    // Rename the file
    file.setName(newFileName);
  } catch (error) {
    Logger.log(`Error processing file ${fileId}: ${error}`);
  }
}

// Utility function to pad the start of a number with zeros
function padStart(num, length) {
  return num.toString().padStart(length, '0');
}