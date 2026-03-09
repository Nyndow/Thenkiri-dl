[CmdletBinding()]
param(
    [switch]$SkipSystemDeps
)

$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $RootDir ".venv"
$ReqFile = Join-Path $RootDir "requirements.txt"
$EnvFile = Join-Path $RootDir ".env"

function Write-Info {
    param([string]$Message)
    Write-Host "`n[install] $Message"
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WithWinget {
    param(
        [string]$Id,
        [string]$Name
    )

    if (-not (Test-Command winget)) {
        return $false
    }

    Write-Info "Installing $Name with winget..."
    winget install --id $Id --accept-source-agreements --accept-package-agreements --silent
    return $true
}

function Install-WithChoco {
    param([string]$Name)

    if (-not (Test-Command choco)) {
        return $false
    }

    Write-Info "Installing $Name with choco..."
    choco install $Name -y
    return $true
}

function Install-WithScoop {
    param([string]$Name)

    if (-not (Test-Command scoop)) {
        return $false
    }

    Write-Info "Installing $Name with scoop..."
    scoop install $Name
    return $true
}

function Ensure-Tool {
    param(
        [string]$CommandName,
        [string]$DisplayName,
        [string]$WingetId,
        [string]$ChocoName,
        [string]$ScoopName
    )

    if (Test-Command $CommandName) {
        Write-Info "$DisplayName already available."
        return
    }

    if ($SkipSystemDeps) {
        throw "$DisplayName is required but not installed. Re-run without -SkipSystemDeps or install manually."
    }

    $installed = $false

    if ($WingetId) {
        $installed = Install-WithWinget -Id $WingetId -Name $DisplayName
    }

    if (-not $installed -and $ChocoName) {
        $installed = Install-WithChoco -Name $ChocoName
    }

    if (-not $installed -and $ScoopName) {
        $installed = Install-WithScoop -Name $ScoopName
    }

    if (-not $installed) {
        throw "Could not auto-install $DisplayName. Install it manually and run this script again."
    }

    if (-not (Test-Command $CommandName)) {
        Write-Info "$DisplayName may require a new terminal session to be visible in PATH."
    }
}

function Resolve-PythonCommand {
    if (Test-Command py) { return "py" }
    if (Test-Command python) { return "python" }
    throw "Python was not found after installation. Open a new terminal and try again."
}

function Setup-Venv {
    if (-not (Test-Path $ReqFile)) {
        throw "Missing requirements.txt at $ReqFile"
    }

    $pythonCmd = Resolve-PythonCommand

    Write-Info "Creating Python virtual environment..."
    if (Test-Path $VenvDir) {
        Remove-Item -Recurse -Force $VenvDir
    }

    if ($pythonCmd -eq "py") {
        & py -3 -m venv $VenvDir
    }
    else {
        & python -m venv $VenvDir
    }

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"

    Write-Info "Installing Python dependencies..."
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r $ReqFile
}

function Ensure-EnvFile {
    if (Test-Path $EnvFile) {
        Write-Info ".env already exists. Leaving it unchanged."
        return
    }

    Write-Info "Creating default .env file..."
    Set-Content -Path $EnvFile -Value "DOWNLOAD_PATH=./downloads"
}

Set-Location $RootDir

Ensure-Tool -CommandName "python" -DisplayName "Python" -WingetId "Python.Python.3.12" -ChocoName "python" -ScoopName "python"
Ensure-Tool -CommandName "aria2c" -DisplayName "aria2" -WingetId "aria2.aria2" -ChocoName "aria2" -ScoopName "aria2"
Ensure-Tool -CommandName "wget" -DisplayName "wget" -WingetId "GnuWin32.Wget" -ChocoName "wget" -ScoopName "wget"

Setup-Venv
Ensure-EnvFile

Write-Host "`nInstallation complete."
Write-Host "Next steps:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  python .\main.py"
