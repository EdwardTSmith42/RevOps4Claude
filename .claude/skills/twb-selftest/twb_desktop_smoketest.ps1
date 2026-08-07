# Tableau Desktop open smoke test for a generated/modified .twb/.twbx.
# The ONLY authoritative validation of workbook XML is Tableau Desktop itself
# (no public XSD exists; schema is compiled into the product). D2E8DA72-class
# load errors surface BEFORE any sign-in, so this needs no credentials.
#
# Usage:  powershell -File twb_desktop_smoketest.ps1 -Path "C:\path\book.twb" [-TimeoutSec 120]
# Exit 0 = file loaded with no error dialog (sign-in prompt or canvas reached)
# Exit 1 = Desktop showed a load-error dialog (text is printed)
# Exit 2 = inconclusive (timeout without main window; investigate manually)
param(
    [Parameter(Mandatory = $true)][string]$Path,
    [int]$TimeoutSec = 150,
    [int]$SettleSec = 20,      # window must stay error-free this long to PASS
    [string]$ExpectText = '',  # e.g. dashboard/sheet name; required in UI tree for a strong PASS
    [string]$LogPath = "$env:TEMP\twb_smoketest_last.txt"
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

if (-not (Test-Path $Path)) { Write-Output "NOFILE: $Path"; exit 2 }
$Path = (Resolve-Path $Path).Path

$exe = Get-ChildItem 'C:\Program Files\Tableau\Tableau *\bin\tableau.exe' |
    Sort-Object FullName -Descending | Select-Object -First 1
if (-not $exe) { Write-Output 'NOEXE: Tableau Desktop not found'; exit 2 }

$before = @(Get-Process tableau -ErrorAction SilentlyContinue | ForEach-Object Id)
$proc = Start-Process -FilePath $exe.FullName -ArgumentList ('"' + $Path + '"') -PassThru
Start-Sleep -Seconds 5

# resolve the PID actually owning the new window (handles single-instance handoff)
function Get-TableauPids {
    @(Get-Process tableau -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object Id)
}

$errorPatterns = @(
    'Errors occurred while trying to load',
    'Unable to complete action',
    'Error Code:',
    'no declaration found for element',
    'is not allowed for content model',
    'internal error'
)
$signinPatterns = @('Sign In', 'Sign in', 'Tableau Server Sign In', 'Connect to Tableau')

function Get-WindowTexts([int[]]$pids) {
    $texts = New-Object System.Collections.Generic.List[string]
    $rootEl = [System.Windows.Automation.AutomationElement]::RootElement
    $cond = [System.Windows.Automation.Condition]::TrueCondition
    foreach ($w in $rootEl.FindAll([System.Windows.Automation.TreeScope]::Children, $cond)) {
        try {
            if ($pids -notcontains $w.Current.ProcessId) { continue }
            $texts.Add("TITLE::" + $w.Current.Name)
            foreach ($d in $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)) {
                try {
                    $n = $d.Current.Name
                    if ($n -and $n.Length -gt 0 -and $n.Length -lt 4000) { $texts.Add($n) }
                } catch {}
            }
        } catch {}
    }
    return $texts
}

$deadline = (Get-Date).AddSeconds($TimeoutSec)
$result = 'TIMEOUT'
$detail = ''
$firstWindowSeen = $null
$lastBlob = ''

while ((Get-Date) -lt $deadline) {
    $pids = Get-TableauPids
    if ($pids.Count -eq 0 -and $proc.HasExited) { Start-Sleep -Seconds 2; $pids = Get-TableauPids }
    if ($pids.Count -gt 0) {
        $texts = Get-WindowTexts $pids
        if ($texts.Count -gt 0 -and -not $firstWindowSeen) { $firstWindowSeen = Get-Date }
        $blob = $texts -join "`n"
        $lastBlob = $blob
        $hitErr = $errorPatterns | Where-Object { $blob -match [regex]::Escape($_) } | Select-Object -First 1
        if ($hitErr) {
            $result = 'FAIL'
            $detail = ($texts | Where-Object { $_ -notmatch '^TITLE::' } |
                Where-Object { $line = $_; ($errorPatterns | Where-Object { $line -match [regex]::Escape($_) }).Count -gt 0 -or $_ -match 'Error' }) -join "`n"
            break
        }
        # strong positive signal: the workbook's own UI text is on screen
        if ($ExpectText -and $blob -match [regex]::Escape($ExpectText)) {
            $result = 'PASS'; $detail = "found expected text '$ExpectText' with no load errors"; break
        }
        $hitSign = $signinPatterns | Where-Object { $blob -match [regex]::Escape($_) } | Select-Object -First 1
        if ($hitSign) { $result = 'PASS'; $detail = "reached connection stage ($hitSign) with no load errors"; break }
        if (-not $ExpectText -and $firstWindowSeen -and ((Get-Date) - $firstWindowSeen).TotalSeconds -ge $SettleSec) {
            $titled = ($texts | Where-Object { $_ -match '^TITLE::' }) -join '; '
            $result = 'PASS'; $detail = "window(s) open, error-free for ${SettleSec}s: $titled"; break
        }
    }
    Start-Sleep -Seconds 3
}
if ($result -eq 'TIMEOUT' -and $ExpectText -and $firstWindowSeen) {
    $detail = "no error dialog, but expected text '$ExpectText' never appeared (inconclusive)"
}
try { $lastBlob | Out-File -FilePath $LogPath -Encoding utf8 } catch {}

# cleanup: kill every tableau process we spawned
foreach ($p in (Get-TableauPids)) {
    try { & taskkill /PID $p /T /F 2>$null | Out-Null } catch {}
}
if (-not $proc.HasExited) { try { & taskkill /PID $proc.Id /T /F 2>$null | Out-Null } catch {} }

Write-Output "RESULT: $result"
if ($detail) { Write-Output "DETAIL: $detail" }
switch ($result) {
    'PASS'    { exit 0 }
    'FAIL'    { exit 1 }
    default   { exit 2 }
}
