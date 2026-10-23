param(
    [switch]$Project
)

#Requires -Version 5.1
$Version = "2.1.0"
Write-Host ""
Write-Host "  MAXILUN $Version Installer" -ForegroundColor Cyan
Write-Host "  18 skills: 1 orchestrator + 17 specialists" -ForegroundColor DarkCyan
Write-Host ""

$ScriptDir = Split-Path -Parent $PSScriptRoot
$SkillsSrc = Join-Path $ScriptDir "skills"
if (-not (Test-Path $SkillsSrc)) {
    $SkillsSrc = Join-Path $ScriptDir ".agents\skills"
}

$InstalledTo = @()
$BackedUp = @()
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmssfff"

# --- Python Dependency Check (Knowledge Graph) ---
$PythonAvailable = $false
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $verOutput = & $cmd --version 2>&1
        if ($verOutput -match '(\d+)\.(\d+)') {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                $PythonAvailable = $true
                Write-Host "  Python ${major}.${minor} detected ($cmd) -- Knowledge Graph visualizer ready." -ForegroundColor Green
                break
            }
        }
    } catch {
        continue
    }
}
if (-not $PythonAvailable) {
    Write-Host "  Python 3.8+ not found. Knowledge Graph visualizer will be unavailable." -ForegroundColor Yellow
    Write-Host "  Install Python from https://www.python.org/downloads/ and re-run this installer." -ForegroundColor Yellow
    Write-Host "  All other Maxilun skills work without Python." -ForegroundColor Gray
}

if ($Project) {
    $CurrentDir = Get-Location
    $Targets = @(
        @{ Name = "Universal / Antigravity / Zed (Project)"; Path = "$CurrentDir\.agents\skills"; LegacyRules = "$CurrentDir\.agents\rules" },
        @{ Name = "[CC] / Termul (Project)";                 Path = "$CurrentDir\.claude\skills"; LegacyRules = "$CurrentDir\.claude\rules" },
        @{ Name = "Trae (Project)";                          Path = "$CurrentDir\.trae\skills"; LegacyRules = $null },
        @{ Name = "Windsurf (Project)";                      Path = "$CurrentDir\.windsurf\skills"; LegacyRules = $null },
        @{ Name = "CodeBuddy (Project)";                     Path = "$CurrentDir\.codebuddy\skills"; LegacyRules = $null }
    )
} else {
    $Targets = @(
        @{ Name = "Antigravity CLI/IDE & Zed"; Path = "$env:USERPROFILE\.agents\skills";          LegacyRules = "$env:USERPROFILE\.agents\rules" },
        @{ Name = "[CC] & Termul";             Path = "$env:USERPROFILE\.claude\skills";          LegacyRules = "$env:USERPROFILE\.claude\rules" },
        @{ Name = "Codex";                     Path = "$env:USERPROFILE\.codex\skills";           LegacyRules = "$env:USERPROFILE\.codex\rules" },
        @{ Name = "OpenCode";                  Path = "$env:USERPROFILE\.config\opencode\skills"; LegacyRules = "$env:USERPROFILE\.config\opencode\rules" },
        @{ Name = "Gemini CLI";                Path = "$env:USERPROFILE\.gemini\config\skills";   LegacyRules = $null },
        @{ Name = "Cursor";                    Path = "$env:USERPROFILE\.cursor\skills";          LegacyRules = $null },
        @{ Name = "Trae";                      Path = "$env:USERPROFILE\.trae\skills";            LegacyRules = $null },
        @{ Name = "CodeBuddy";                 Path = "$env:USERPROFILE\.codebuddy\skills";       LegacyRules = $null }
    )
}

foreach ($target in $Targets) {
    $parentDir = Split-Path -Parent $target.Path
    $shouldInstall = $Project -or $target.Name -like "*Antigravity*" -or $target.Name -like "*Claude*" -or (Test-Path $parentDir)
    if (-not $shouldInstall) { continue }

    if (Test-Path $target.Path -PathType Container) {
        $backupRoot = Join-Path $parentDir "_maxilun_backup_$Timestamp"
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        Copy-Item -Path $target.Path -Destination (Join-Path $backupRoot "skills") -Recurse -Force
        $BackedUp += "  $($target.Name): $backupRoot"
    }

    if (-not (Test-Path $target.Path)) {
        New-Item -ItemType Directory -Path $target.Path -Force | Out-Null
    }

    Get-ChildItem -Path $target.Path -Directory -ErrorAction SilentlyContinue | Where-Object {
        ($_.Name -eq "maxilun" -or $_.Name -like "maxilun-*" -or $_.Name -like "msal-*") -and
        (Test-Path (Join-Path $_.FullName "SKILL.md")) -and
        ((Get-Content (Join-Path $_.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue) -match '(?m)^  ecosystem:\s*maxilun\s*$')
    } | Remove-Item -Recurse -Force

    Copy-Item -Path "$SkillsSrc\*" -Destination $target.Path -Recurse -Force

    Get-ChildItem -Path $target.Path -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $target.Path -File -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue

    # Remove v1 rule files that lived outside the skill folder (marked Maxilun only)
    if ($target.LegacyRules -and (Test-Path $target.LegacyRules)) {
        foreach ($ruleName in @("always-on.md", "maxilun-global.md", "code-hygiene.md", "purity-catalog.md")) {
            $rulePath = Join-Path $target.LegacyRules $ruleName
            if (Test-Path $rulePath) {
                $head = Get-Content $rulePath -TotalCount 3 -ErrorAction SilentlyContinue
                if ($head -match 'Maxilun|Four Always-On Engines') {
                    Remove-Item -LiteralPath $rulePath -Force
                }
            }
        }
    }

    $InstalledTo += "  $($target.Name): $($target.Path)"
}

Write-Host ""
if ($BackedUp.Count -gt 0) {
    Write-Host "  Previous versions backed up to:" -ForegroundColor Yellow
    foreach ($b in $BackedUp) { Write-Host $b -ForegroundColor White }
}
Write-Host ""
if ($InstalledTo.Count -eq 0) {
    Write-Host "  No supported AI CLI/IDE detected automatically." -ForegroundColor Yellow
    Write-Host "  Tip: use 'npx skills add giriedu/maxilun' for interactive installation." -ForegroundColor Yellow
} else {
    Write-Host "  Installed successfully to:" -ForegroundColor Green
    foreach ($loc in $InstalledTo) { Write-Host $loc -ForegroundColor White }
}

Write-Host ""
Write-Host "  --------------------------------------" -ForegroundColor DarkCyan
Write-Host "  Post-Install Verification" -ForegroundColor Cyan
Write-Host "  --------------------------------------" -ForegroundColor DarkCyan
$VerifyOk = $true
foreach ($loc in $InstalledTo) {
    $parts = $loc.Split(":", 2)
    $platformLabel = $parts[0].Trim()
    $targetDir = $parts[1].Trim()
    $skillFiles = Get-ChildItem -Path $targetDir -Filter "SKILL.md" -Recurse -Depth 2 -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '[\\/](maxilun|maxilun-[^\\/]+|msal-[^\\/]+)[\\/]SKILL\.md$' }
    $count = if ($skillFiles) { @($skillFiles).Count } else { 0 }
    if ($count -ge 18) {
        Write-Host "    $platformLabel : ${count}/18 skills" -ForegroundColor Green
    } else {
        Write-Host "    $platformLabel : only ${count}/18 skills -- reinstall recommended" -ForegroundColor Red
        $VerifyOk = $false
    }
    $engines = Join-Path $targetDir "maxilun\references\engines.md"
    if (Test-Path $engines) {
        Write-Host "      rules bundled inside skill (references/)" -ForegroundColor Green
    } else {
        Write-Host "      references/engines.md missing -- skill would run without core rules" -ForegroundColor Red
        $VerifyOk = $false
    }
}
if ($PythonAvailable) {
    $kgCli = $null
    foreach ($loc in $InstalledTo) {
        $candidate = Join-Path ($loc.Split(":", 2)[1].Trim()) "maxilun-knowledge-graph\cli.py"
        if (Test-Path $candidate) { $kgCli = $candidate; break }
    }
    if ($kgCli) {
        Write-Host "    Knowledge Graph CLI: $kgCli" -ForegroundColor Green
    } else {
        Write-Host "    Knowledge Graph CLI: cli.py not found" -ForegroundColor Yellow
        $VerifyOk = $false
    }
} else {
    Write-Host "    Knowledge Graph CLI: skipped (Python not available)" -ForegroundColor Gray
}
Write-Host ""
if ($VerifyOk) {
    Write-Host "  All checks passed. Maxilun $Version is operational." -ForegroundColor Green
} else {
    Write-Host "  Some checks failed. Review output above and re-run the installer." -ForegroundColor Yellow
    exit 1
}
Write-Host ""
