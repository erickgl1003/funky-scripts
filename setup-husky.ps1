# ==========================
# setup-husky-venv.ps1
# One-command Husky + Python + Commitlint setup with automated venv (Windows)
# ==========================

param(
    [string]$VenvName = ".venv"  # Name of the virtual environment folder
)

# Step 0: Ensure npm is installed
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm is not installed. Please install Node.js first." -ForegroundColor Red
    exit
}

# Step 1: Create venv if missing
if (-not (Test-Path $VenvName)) {
    Write-Host "Creating virtual environment '$VenvName'..."
    python -m venv $VenvName
} else {
    Write-Host "Virtual environment '$VenvName' already exists."
}

# Step 2: Activate the venv for this script
$ActivateScript = Join-Path $VenvName "Scripts\Activate.ps1"
Write-Host "Activating virtual environment..."
& $ActivateScript

# Step 3: Detect the Python executable inside venv
$PythonExe = Join-Path $VenvName "Scripts\python.exe"
Write-Host "Using Python: $PythonExe"

# Step 4: Upgrade pip and install dev packages
Write-Host "Installing Python packages: black, isort, pytest..."
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install black isort pytest

# Step 5: Initialize npm if missing
if (-not (Test-Path "package.json")) {
    Write-Host "Initializing npm..."
    npm init -y
}

# Step 6: Install Husky + Commitlint
Write-Host "Installing Husky and Commitlint..."
npm install --save-dev husky @commitlint/config-conventional @commitlint/cli

# Step 7: Initialize Husky (modern)
Write-Host "Initializing Husky..."
npx husky-init
npm install

# Step 8: Create pre-commit hook (Python checks)
Write-Host "Creating pre-commit hook..."
@"
#!/bin/sh
. .husky/_/husky.sh

echo 'Running pre-commit Python checks...'

`"$PythonExe`" -m black .
`"$PythonExe`" -m isort .

echo 'Pre-commit checks finished.'
"@ | Set-Content ".husky/pre-commit"

git update-index --add --chmod=+x .husky/pre-commit

# Step 9: Create pre-push hook (Python tests)
Write-Host "Creating pre-push hook..."
@"
#!/bin/sh
. .husky/_/husky.sh

echo 'Running pre-push tests...'

`"$PythonExe`" -m pytest

echo 'Pre-push tests finished.'
"@ | Set-Content ".husky/pre-push"

git update-index --add --chmod=+x .husky/pre-push

# Step 10: Create commit-msg hook (Commitlint)
Write-Host "Creating commit-msg hook..."
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'

# Step 11: Create commitlint config
Write-Host "Creating commitlint.config.ts..."
@"
export default {
    extends: ['@commitlint/config-conventional']
};
"@ | Set-Content "commitlint.config.ts"

Write-Host "Full Husky + Python venv + Commitlint setup complete" -ForegroundColor Green
Write-Host "venv is activated, Python dev packages installed, Husky hooks ready."
Write-Host "Future commits and pushes will automatically use the venv Python."
