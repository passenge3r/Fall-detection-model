param(
    [int]$BatchSize = 128
)

$ErrorActionPreference = "Stop"
$Project = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Project ".venv\Scripts\python.exe"
$Trainer = Join-Path $PSScriptRoot "train_prefall_multihorizon_stgcnpp.py"
$OutputRoot = Join-Path $Project "outputs\prevfall_rtmpose_stgcnpp_300e_b128"
$RunLog = Join-Path $OutputRoot "run_status.log"

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
Set-Location $Project

foreach ($Fold in 1..9) {
    $FoldDir = Join-Path $OutputRoot "fold_$Fold"
    $Metrics = Join-Path $FoldDir "metrics.json"
    $History = Join-Path $FoldDir "history.csv"
    $Complete = $false
    if ((Test-Path $Metrics) -and (Test-Path $History)) {
        $MetricObject = Get-Content $Metrics -Raw | ConvertFrom-Json
        $HistoryRows = (Import-Csv $History).Count
        $Complete = ($MetricObject.epochs_ran -eq 300) -and ($HistoryRows -eq 300)
    }
    if ($Complete) {
        "$(Get-Date -Format o) SKIP fold=$Fold complete" | Add-Content $RunLog
        continue
    }

    New-Item -ItemType Directory -Force -Path $FoldDir | Out-Null
    $FoldLog = Join-Path $FoldDir "train.log"
    "$(Get-Date -Format o) START fold=$Fold batch=$BatchSize" | Add-Content $RunLog
    & $Python $Trainer `
        --data "data/gcn/prevfall_rtmpose_prefall_w64_s16_h123.npz" `
        --splits "data/splits/prevfall_prefall_loso9" `
        --fold $Fold `
        --output $FoldDir `
        --epochs 300 `
        --batch-size $BatchSize `
        --device cuda *>&1 | Tee-Object -FilePath $FoldLog
    if ($LASTEXITCODE -ne 0) {
        "$(Get-Date -Format o) FAILED fold=$Fold exit=$LASTEXITCODE" | Add-Content $RunLog
        exit $LASTEXITCODE
    }
    "$(Get-Date -Format o) DONE fold=$Fold" | Add-Content $RunLog
}

& $Python "scripts/summarize_prefall_loso.py" `
    --root $OutputRoot `
    --fold-count 9
"$(Get-Date -Format o) ALL_DONE" | Add-Content $RunLog
