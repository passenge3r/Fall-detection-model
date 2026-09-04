param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found. Create .venv and install requirements first."
}

if (-not $env:FALL_SERVICE_API_KEY -and $HostAddress -notin @("127.0.0.1", "localhost", "::1")) {
    throw "Set FALL_SERVICE_API_KEY before binding to a non-loopback address."
}

$env:FALL_ROUTE = if ($env:FALL_ROUTE) { $env:FALL_ROUTE } else { "rtmpose_stgcnpp" }
$env:FALL_CHECKPOINTS_ROOT = if ($env:FALL_CHECKPOINTS_ROOT) { $env:FALL_CHECKPOINTS_ROOT } else { Join-Path $ProjectRoot "weights\stgcnpp" }
$env:FALL_YOLO_MODEL = if ($env:FALL_YOLO_MODEL) { $env:FALL_YOLO_MODEL } else { Join-Path $ProjectRoot "weights\yolo26n-pose.pt" }
$env:FALL_DEVICE = if ($env:FALL_DEVICE) { $env:FALL_DEVICE } else { "cuda" }
$env:PREFALL_ENABLED = if ($env:PREFALL_ENABLED) { $env:PREFALL_ENABLED } else { "true" }
$env:PREFALL_CHECKPOINTS_ROOT = if ($env:PREFALL_CHECKPOINTS_ROOT) { $env:PREFALL_CHECKPOINTS_ROOT } else { Join-Path $ProjectRoot "weights\prefall" }
$env:PREFALL_MIN_POSITIVE_FOLDS = if ($env:PREFALL_MIN_POSITIVE_FOLDS) { $env:PREFALL_MIN_POSITIVE_FOLDS } else { "5" }
$env:MULTIMODAL_ENABLED = if ($env:MULTIMODAL_ENABLED) { $env:MULTIMODAL_ENABLED } else { "false" }
$env:MULTIMODAL_MODEL = if ($env:MULTIMODAL_MODEL) { $env:MULTIMODAL_MODEL } else { "Qwen/Qwen3-VL-2B-Instruct" }
$env:MULTIMODAL_DEVICE = if ($env:MULTIMODAL_DEVICE) { $env:MULTIMODAL_DEVICE } else { $env:FALL_DEVICE }
$env:MULTIMODAL_FRAMES = if ($env:MULTIMODAL_FRAMES) { $env:MULTIMODAL_FRAMES } else { "8" }
$env:MULTIMODAL_BUFFER_FRAMES = if ($env:MULTIMODAL_BUFFER_FRAMES) { $env:MULTIMODAL_BUFFER_FRAMES } else { "160" }
$env:MULTIMODAL_MAX_NEW_TOKENS = if ($env:MULTIMODAL_MAX_NEW_TOKENS) { $env:MULTIMODAL_MAX_NEW_TOKENS } else { "112" }
$env:MULTIMODAL_COOLDOWN_SECONDS = if ($env:MULTIMODAL_COOLDOWN_SECONDS) { $env:MULTIMODAL_COOLDOWN_SECONDS } else { "15" }
$env:MULTIMODAL_POST_TRIGGER_SECONDS = if ($env:MULTIMODAL_POST_TRIGGER_SECONDS) { $env:MULTIMODAL_POST_TRIGGER_SECONDS } else { "2.5" }
$env:MULTIMODAL_TRIGGER_LEVELS = if ($env:MULTIMODAL_TRIGGER_LEVELS) { $env:MULTIMODAL_TRIGGER_LEVELS } else { "HIGH,FALL_CONFIRMED" }

Push-Location $ProjectRoot
try {
    & $Python "scripts\run_fall_api.py" --host $HostAddress --port $Port
}
finally {
    Pop-Location
}
