# Remove o wrapper e a pasta do mindmestre (Windows).
$ErrorActionPreference = "Continue"
$cmd = Join-Path $env:LOCALAPPDATA "GenialMindMestre" "bin" "mindmestre.cmd"
if (Test-Path $cmd) { Remove-Item $cmd -Force; Write-Host "removido: $cmd" }
$dest = Join-Path $env:USERPROFILE ".genial-mind-mestre"
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force; Write-Host "removido: $dest" }
Write-Host "Genial Labs · MIND MESTRE removido."
