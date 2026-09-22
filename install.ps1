# Genial Labs · MIND MESTRE — instalação Windows nativo (PowerShell 5.1+).
# Baixa o repositório, coloca em %USERPROFILE%\.genial-mind-mestre e cria
# o wrapper em %LOCALAPPDATA%\GenialMindMestre\bin (adicionado ao PATH de usuário).
$ErrorActionPreference = "Stop"
Write-Host "Genial Labs · MIND MESTRE — instalação Windows" -ForegroundColor Cyan
Write-Host ""

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { throw "python não encontrado no PATH. Instale em python.org marcando 'Add python.exe to PATH'." }
Write-Host "python ok: $($py.Source)"

$tmp = Join-Path $env:TEMP ("gl-mindmestre-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory $tmp | Out-Null
try {
  Write-Host "[1/4] baixando o MindMestre…" -ForegroundColor DarkGray
  $zip = Join-Path $tmp "pacote.zip"
  Invoke-WebRequest -Uri "https://codeload.github.com/geniallabsai/mind_mestre/zip/refs/heads/main" -OutFile $zip -UseBasicParsing
  $ext = Join-Path $tmp "x"
  Expand-Archive -Path $zip -DestinationPath $ext
  $origem = Get-ChildItem $ext | Select-Object -First 1
  $dest = Join-Path $env:USERPROFILE ".genial-mind-mestre"
  if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
  Copy-Item $origem.FullName $dest -Recurse
  Write-Host "[2/4] instalado em $dest" -ForegroundColor DarkGray
  $bin = Join-Path $env:LOCALAPPDATA "GenialMindMestre" "bin"
  New-Item -ItemType Directory $bin -Force | Out-Null
  $cmd = Join-Path $bin "mindmestre.cmd"
  Set-Content -Path $cmd -Encoding ASCII -Value (@(
    "@echo off",
    "set PYTHONUTF8=1",
    (""{0}" "{1}\mindmestre" %*" -f $py.Source, $dest)
  ) -join "`r`n")
  Write-Host "[3/4] wrapper em $cmd" -ForegroundColor DarkGray
  $pathUser = [Environment]::GetEnvironmentVariable("Path", "User")
  if ($pathUser -notlike "*$bin*") {
    [Environment]::SetEnvironmentVariable("Path", "$pathUser;$bin", "User")
    Write-Host "[4/4] PATH de usuário atualizado — abra um NOVO terminal para o comando valer." -ForegroundColor Yellow
  } else {
    Write-Host "[4/4] PATH já contém o bin — pronto." -ForegroundColor Green
  }
  & $cmd "status" *> $null
  if ($LASTEXITCODE -ne 0) { throw "auto-teste falhou: $cmd status" }
  Write-Host ""
  Write-Host "✓ Genial Labs · MIND MESTRE instalado." -ForegroundColor Green
  Write-Host ""
  Write-Host "  próximos passos (terminal novo):" -ForegroundColor Cyan
  Write-Host "    mindmestre                 ← banner + menu"
    Write-Host "    mindmestre plano .         ← este diretório vira investigação + plano"
    Write-Host "    mindmestre conversa .      ← interrogatório socrático calibrado pela nuance"
} finally {
  Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
