const jsonfile = require('jsonfile');
const moment = require('moment');
const simpleGit = require('simple-git');
const FILE_PATH = './data.json';

const makeCommit = (n) => {
    if (n === 0) return simpleGit().push();

    // Generate random numbers for date calculation
    const x = Math.floor(Math.random() * 55); // Random number between 0 and 54
    const y = Math.floor(Math.random() * 7);  // Random number between 0 and 6

    // Generate a date based on the random numbers
    const DATE = moment().subtract(1, 'y').add(1, 'd')
        .add(x, 'w').add(y, 'd').format();
    
    // Data to write to the JSON file
    const date = { date: DATE };
    console.log(`Committing for date: ${DATE}`);    

    // Write the date to JSON file and then commit
    jsonfile.writeFile(FILE_PATH, date, (err) => {
        if (err) return console.error("Error writing file:", err);

        // Add and commit the file using simpleGit
        simpleGit()
            .add([FILE_PATH])
            .commit(DATE, { '--date': DATE })
            .then(() => {
                // Recursive call to make the next commit
                makeCommit(n - 1);
            })
            .catch((err) => console.error("Error during git commit:", err));
    });
}

// Start the commit process with 500 commits
makeCommit(500);


