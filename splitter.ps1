# File's dir.
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activating .venv
.\.venv\Scripts\activate

# Starting WSGI
python -B splitter.py

# Deactivating .venv
deactivate