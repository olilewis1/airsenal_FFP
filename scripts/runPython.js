const { spawn } = require('child_process');

const runPythonScript = (loginData,  scriptPath) => {
  const command = 'python'; // Or the path to your Python executable
  console.log(loginData, 'login')
  const args = [
    scriptPath,
    '--fpl_login', loginData.login,
    '--fpl_password', loginData.password,
    '--fpl_team_id', loginData.fplId.toString(),
    // Add more arguments as needed
  ];

  // Execute the Python script
  const process = spawn(command, args);

  // Handle process output and errors if needed
  process.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  process.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
};

// Export the runPythonScript function
module.exports = runPythonScript;
