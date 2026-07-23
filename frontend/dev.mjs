import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const frontendDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(frontendDir, "..");
const backendDir = path.join(projectDir, "backend");
const command = process.platform === "win32" ? "npm.cmd" : "npm";

// Keep the API process attached to Vite. Closing `npm run dev` also closes
// Flask, preventing a login page without its login server.
const backend = spawn("python", ["app.py"], {
  cwd: backendDir,
  env: { ...process.env, PORT: "5001" },
  stdio: "inherit",
  shell: process.platform === "win32",
});
const frontend = spawn(command, ["exec", "vite", "--", "--host", "127.0.0.1"], {
  cwd: frontendDir,
  stdio: "inherit",
  shell: process.platform === "win32",
});

function stop() {
  backend.kill();
  frontend.kill();
}
process.on("SIGINT", stop);
process.on("SIGTERM", stop);
frontend.on("exit", (code) => { backend.kill(); process.exit(code ?? 0); });
backend.on("exit", (code) => {
  if (code && !frontend.killed) console.error(`EvalAI backend stopped unexpectedly (exit code ${code}).`);
});
