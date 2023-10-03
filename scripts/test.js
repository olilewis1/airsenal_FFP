// server.js
const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors'); // Import the cors middleware
const bodyParser = require('body-parser'); // Import body-parser
const app = express();
const port = 3001;


app.use(cors());

// Parse application/x-www-form-urlencoded and application/json
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Define a route for running the Python script
app.post('/run-python-script', (req, res) => {
  console.log("hiii", req.body);
  // Assuming you will receive login data in the request body
  const loginData = req.body;
  const condaEnvName = 'airsenalenv'; // Modify with your Conda environment name
  const scriptPath = '/Users/oliverlewis/development/airsenal-app/AIrsenal/scripts/automate_commands.py';
  
  // Construct the command to run within the Conda environment
  const command = `conda activate ${condaEnvName} && python ${scriptPath}`;
  
 // Or the path to your Python executable
  const args = [
    scriptPath,
    '--fpl_login', loginData.login,
    '--fpl_password', loginData.password,
    '--fpl_team_id', loginData.fplId.toString(),
    // Add more arguments as needed
  ];

  const options = { shell: true };

  // Execute the Python script
  const process = spawn(command, args, options);

  // Handle process output and errors if needed
  let hasError = false;

// Handle process output and errors if needed
process.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

process.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
  hasError = true; // Set the error flag
});

process.on('close', (code) => {
  console.log(`child process exited with code ${code}`);

  if (code === 0 && !hasError) {
    // The script ran successfully
    res.json({ message: 'Python script execution started.' });
  } else {
    // Handle the error case (code !== 0 or hasError is true) here
    res.status(500).json({ error: 'Python script execution failed.' });
  }
});
  // Respond to the client with a success message or other relevant data
});

app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});
