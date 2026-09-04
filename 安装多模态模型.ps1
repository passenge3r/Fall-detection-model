$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found. Create .venv and install requirements first."
}

Push-Location $ProjectRoot
try {
    & $Python -m pip install -r requirements-multimodal.txt
    & $Python scripts\prepare_multimodal_model.py
}
finally {
    Pop-Location
}
