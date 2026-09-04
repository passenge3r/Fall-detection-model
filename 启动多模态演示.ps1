param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:MULTIMODAL_ENABLED = "true"
$env:MULTIMODAL_ALLOW_DOWNLOAD = "false"

& (Join-Path $ProjectRoot "start_api.ps1") -HostAddress $HostAddress -Port $Port
