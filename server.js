const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const bodyParser = require('body-parser');
const app = express();
const port = 3001;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.post('/run-python-script', (req, res) => {
  console.log("hiii", req.body);
  const loginData = req.body;
  const condaEnvName = 'airsenalenv'; // Modify with your Conda environment name
  const scriptPath = '/Users/oliverlewis/development/airsenal-app/AIrsenal/scripts/automate_commands.py';

  // Construct the command to activate the Conda environment
  const activateCommand = `conda activate ${condaEnvName}`;

  // Or the path to your Python executable
  const pythonExecutable = 'python';

  // Arguments for the Python script
  const scriptArgs = [
    scriptPath,
    '--fpl_login', loginData.login,
    '--fpl_password', loginData.password,
    '--fpl_team_id', loginData.fplId.toString(),
    // Add more arguments as needed
  ];

  const options = { shell: true };
  let hasError = false;

  // Execute the activation command first
  // const activateProcess = spawn(activateCommand, [], options);

  // Handle activation process output and errors
  // activateProcess.on('error', (err) => {
  //   console.error(`Activation process error: ${err.message}`);
  //   hasError = true;
  // });



    // Now execute the Python script
    const pythonProcess = spawn(pythonExecutable, scriptArgs, options);

    pythonProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      hasError = true;
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python script process exited with code ${code}`);

      if (!hasError) {
        res.json({ message: 'Python script execution started.' });
      } else {
        res.status(500).json({ error: 'Python script execution failed.' });
      }
    });
  });


app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});
