# Starts the only backend/frontend pair used by this project.
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $projectRoot "frontend")
npm.cmd run dev
