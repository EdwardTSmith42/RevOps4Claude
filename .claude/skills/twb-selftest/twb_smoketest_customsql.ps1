param(
    [string]$Path = "C:\Users\esmith\temp\program_taxonomy_launch\HFD Program Code Lookup.twb",
    [string]$Answer = "No"
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes

$exe = Get-ChildItem "C:\Program Files\Tableau" -Recurse -Filter "tableau.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
if (-not $exe) { Write-Output "FAIL: tableau.exe not found"; exit 2 }
$before = @(Get-Process tableau -ErrorAction SilentlyContinue | ForEach-Object Id)
$proc = Start-Process -FilePath $exe.FullName -ArgumentList "`"$Path`"" -PassThru
Write-Output ("spawned pid " + $proc.Id)

function Get-Windows([int[]]$pids) {
    $rootEl = [System.Windows.Automation.AutomationElement]::RootElement
    $cond = [System.Windows.Automation.Condition]::TrueCondition
    $out = @()
    foreach ($w in $rootEl.FindAll([System.Windows.Automation.TreeScope]::Children, $cond)) {
        try { if ($pids -contains $w.Current.ProcessId) { $out += $w } } catch {}
    }
    return $out
}

function Dump-Text($el) {
    $sb = New-Object System.Text.StringBuilder
    $cond = [System.Windows.Automation.Condition]::TrueCondition
    foreach ($d in $el.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)) {
        try { $n = $d.Current.Name; if ($n -and $n.Trim()) { [void]$sb.AppendLine($n) } } catch {}
    }
    return $sb.ToString()
}

# Phase 1: wait for the Custom SQL Warning dialog and answer it
$answered = $false
$deadline = (Get-Date).AddSeconds(120)
while ((Get-Date) -lt $deadline -and -not $answered) {
    Start-Sleep -Seconds 3
    $allPids = @(Get-Process tableau -ErrorAction SilentlyContinue | ForEach-Object Id) | Where-Object { $before -notcontains $_ }
    foreach ($w in (Get-Windows $allPids)) {
        $txt = Dump-Text $w
        if ($txt -match 'Custom SQL Warning') {
            $btnCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Answer)
            $btn = $w.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $btnCond)
            if ($btn) {
                $inv = $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
                $inv.Invoke()
                Write-Output ("answered '" + $Answer + "' on Custom SQL Warning")
                $answered = $true
                break
            }
        }
        if ($txt -match 'D2E8DA72|2805CF18|can.t open|unable to open|error code') {
            Write-Output "FAIL: load error dialog"
            Write-Output $txt
            Get-Process tableau -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force
            exit 1
        }
    }
}
if (-not $answered) { Write-Output "WARN: Custom SQL Warning never appeared" }

# Phase 2: dismiss any sign-in dialog and wait for the workbook UI (tab strip) to render
$found = $false
$deadline2 = (Get-Date).AddSeconds(150)
$lastText = ''
while ((Get-Date) -lt $deadline2 -and -not $found) {
    Start-Sleep -Seconds 5
    $allPids = @(Get-Process tableau -ErrorAction SilentlyContinue | ForEach-Object Id) | Where-Object { $before -notcontains $_ }
    foreach ($w in (Get-Windows $allPids)) {
        $txt = Dump-Text $w
        $lastText = $txt
        if ($txt -match 'D2E8DA72|2805CF18') {
            Write-Output "FAIL: load error dialog"; Write-Output $txt
            Get-Process tableau -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force
            exit 1
        }
        # cancel a SQL Server sign-in dialog if it appears
        if ($txt -match 'Sign In|Server Sign In|Microsoft SQL Server') {
            foreach ($bn in @('Cancel','Close')) {
                $cbCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $bn)
                $cb = $w.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cbCond)
                if ($cb) {
                    try { $cb.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke(); Write-Output ("dismissed dialog via " + $bn) } catch {}
                    break
                }
            }
        }
        # dismiss connection-failure boxes so the shell can render
        if ($txt -match 'could not connect|connection error|Unable to connect') {
            foreach ($bn in @('OK','Close','Cancel')) {
                $cbCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $bn)
                $cb = $w.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cbCond)
                if ($cb) {
                    try { $cb.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke(); Write-Output ("dismissed connect-failure via " + $bn) } catch {}
                    break
                }
            }
        }
        if ($txt -match 'Code Lookup' -and $txt -match 'Codes by Vertical') {
            Write-Output "PASS: workbook UI rendered (sheet tabs found)"
            $found = $true; break
        }
    }
}
$lastText | Out-File "$env:TEMP\twb_interactive_last.txt" -Encoding utf8
if ($found) {
    # capture the window for visual proof
    $tpid = (Get-Process tableau -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Select-Object -First 1).Id
    try { & "C:\Users\esmith\.claude\skills\twb-selftest\twb_window_capture.ps1" -ProcId $tpid | Out-Null; Write-Output "captured window" } catch { Write-Output "capture failed: $_" }
}
Get-Process tableau -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | Stop-Process -Force
if ($found) { exit 0 } else { Write-Output "INCONCLUSIVE: workbook UI text not seen; see %TEMP%\twb_interactive_last.txt"; exit 2 }
