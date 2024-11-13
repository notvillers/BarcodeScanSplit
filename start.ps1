# File's dir.
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activating .venv
.\.venv\Scripts\Activate.ps1

# Starting WSGI
python start.py

# Deactivating .venv
deactivate