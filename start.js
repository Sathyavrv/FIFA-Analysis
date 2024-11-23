const { exec } = require("child_process");

const os = require("os");
const path = require("path");

// Backend and Frontend paths
const BACKEND_PATH = path.join(__dirname, "backend", "main.py");
const FRONTEND_PATH = __dirname;


// Helper function to execute commands
const runCommand = (command, cwd = null) => {
  const process = exec(command, { cwd });
  process.stdout.on("data", data => console.log(data.toString()));
  process.stderr.on("data", err => console.error(err.toString()));
};

// Start backend
console.log("Starting backend...");
runCommand(`python ${BACKEND_PATH}`);

// Start frontend
console.log("Starting frontend...");
runCommand("npm start", FRONTEND_PATH);
