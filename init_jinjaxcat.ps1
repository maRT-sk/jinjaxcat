## Run this script from the directory where you downloaded JinjaXcat from GitHub.

# This PowerShell script automates the setup and launch of the JinjaXcat Python app:
# 1. Sets the directory to the script's location.
# 2. Checks for a specific Python version and installs it if not found.
# 3. Creates a virtual environment if it doesn't exist.
# 4. Checks and installs dependencies from 'requirements.txt'.
# 5. Launches JinjaXcat using Streamlit.

# Set the current working directory to the directory of the script being run
Set-Location -Path $PSScriptRoot

# Define the desired Python version
$pythonVersion = "3.11.5"

# Check if the specific version of Python is already installed on the system
$pythonExe = Get-Command -CommandType Application -Name "python.exe" -ErrorAction SilentlyContinue | Where-Object { $_.FileVersionInfo.ProductVersion -eq $pythonVersion }

# If the desired version of Python is found, set its path
if ($pythonExe)
{
    $pythonExePath = $pythonExe.Source
}
else
{
    # If not found, notify the user and prepare to download the installer
    Write-Host "Python $pythonVersion not found. Downloading Python $pythonVersion.."
    $pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-$pythonVersion-amd64.exe"
    # Download the Python installer
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    # Install Python
    Write-Host "Installing Python $pythonVersion..."
    Start-Process -Wait -FilePath $pythonInstaller -ArgumentList "/quiet", "PrependPath=1"
    # After installation, check the path of the new Python executable
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    $pythonExe = Get-Command -CommandType Application -Name "python.exe" -ErrorAction SilentlyContinue | Where-Object { $_.FileVersionInfo.ProductVersion -eq $pythonVersion }
    $pythonExePath = $pythonExe.Source
}

if (-Not(Test-Path '.\venv'))
{
    # Set up a virtual environment for the Python project
    Write-Host "Creating virtual environment..."
    & $pythonExePath -m venv 'venv'
    . .\venv\Scripts\Activate
    # Install the dependencies specified in the 'requirements.txt' file
    Write-Host "Checking if virtual environment '$env:VIRTUAL_ENV' matches requirements from requirements.txt..."
    pip install -r 'requirements.txt'
}

# Activate venv and launch the JinjaXcat application using Streamlit
Write-Host "Activating virtual environment '$env:VIRTUAL_ENV'..."
. .\venv\Scripts\Activate
Write-Host "Launching JinjaXcat application..."
streamlit run 'app\jinjaxcat.py'