param(
    [switch]$Project
)

#Requires -Version 5.1
Write-Host ""
Write-Host "  MAXILUN Specialist Ecosystem Installer" -ForegroundColor Cyan
Write-Host "  ──────────────────────────────────────" -ForegroundColor DarkCyan
Write-Host ""

$ScriptDir = Split-Path -Parent $PSScriptRoot
$SkillsSrc = Join-Path $ScriptDir "skills"
if (-not (Test-Path $SkillsSrc)) {
    $SkillsSrc = Join-Path $ScriptDir ".agents\skills"
}
$RulesSrc  = Join-Path $ScriptDir "rules"

$InstalledTo = @()
$BackedUp = @()
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmssfff"

# --- Python Dependency Check ---
$PythonAvailable = $false
$pythonCandidates = @("python", "python3", "py")
foreach ($cmd in $pythonCandidates) {
    try {
        $verOutput = & $cmd --version 2>&1
        if ($verOutput -match '(\d+)\.(\d+)') {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                $PythonAvailable = $true
                Write-Host "  Python ${major}.${minor} detected ($cmd) — Knowledge Graph visualizer ready." -ForegroundColor Green
                break
            }
        }
    } catch {
        continue
    }
}
if (-not $PythonAvailable) {
    Write-Host "  Python 3.8+ not found. Knowledge Graph visualizer (/graph) will be unavailable." -ForegroundColor Yellow
    Write-Host "  Install Python from https://www.python.org/downloads/ and re-run this installer." -ForegroundColor Yellow
    Write-Host "  Other Maxilun skills work without Python." -ForegroundColor Gray
}

if ($Project) {
    $CurrentDir = Get-Location
    $Targets = @(
        @{ Name = "Universal / Antigravity / Zed (Project)"; Path = "$CurrentDir\.agents\skills"; RulesPath = "$CurrentDir\.agents\rules" },
        @{ Name = "Claude Code / Termul (Project)";         Path = "$CurrentDir\.claude\skills"; RulesPath = "$CurrentDir\.claude\rules" },
        @{ Name = "Trae (Project)";                         Path = "$CurrentDir\.trae\skills"; RulesPath = $null },
        @{ Name = "Windsurf (Project)";                     Path = "$CurrentDir\.windsurf\skills"; RulesPath = $null },
        @{ Name = "CodeBuddy (Project)";                    Path = "$CurrentDir\.codebuddy\skills"; RulesPath = $null }
    )
} else {
    # Target directories for all supported AI agents & platforms
    $Targets = @(
        @{ Name = "Antigravity CLI/IDE & Zed"; Path = "$env:USERPROFILE\.agents\skills";             RulesPath = "$env:USERPROFILE\.agents\rules" },
        @{ Name = "Claude Code & Termul";     Path = "$env:USERPROFILE\.claude\skills";             RulesPath = "$env:USERPROFILE\.claude\rules" },
        @{ Name = "Codex";                    Path = "$env:USERPROFILE\.codex\skills";              RulesPath = "$env:USERPROFILE\.codex\rules" },
        @{ Name = "OpenCode";                 Path = "$env:USERPROFILE\.config\opencode\skills";    RulesPath = "$env:USERPROFILE\.config\opencode\rules" },
        @{ Name = "Gemini CLI";               Path = "$env:USERPROFILE\.gemini\config\skills";       RulesPath = $null },
        @{ Name = "Cursor";                   Path = "$env:USERPROFILE\.cursor\skills";             RulesPath = $null },
        @{ Name = "Trae";                     Path = "$env:USERPROFILE\.trae\skills";               RulesPath = $null },
        @{ Name = "CodeBuddy";                Path = "$env:USERPROFILE\.codebuddy\skills";          RulesPath = $null }
    )
}

foreach ($target in $Targets) {
    $parentDir = Split-Path -Parent $target.Path
    # Always install to Universal/Antigravity and Claude Code, or if parent exists for others
    if ($Project -or $target.Name -like "*Antigravity*" -or $target.Name -like "*Claude*" -or (Test-Path $parentDir)) {
        # Backup existing skills/rules before overwrite
        if (Test-Path $target.Path -PathType Container) {
            $backupRoot = Join-Path (Split-Path -Parent $target.Path) "_maxilun_backup_$Timestamp"
            New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
            Copy-Item -Path $target.Path -Destination (Join-Path $backupRoot "skills") -Recurse -Force
            if ($target.RulesPath -and (Test-Path $target.RulesPath -PathType Container)) {
                Copy-Item -Path $target.RulesPath -Destination (Join-Path $backupRoot "rules") -Recurse -Force
            }
            $BackedUp += "  $($target.Name): $backupRoot"
        }

        if (-not (Test-Path $target.Path)) {
            New-Item -ItemType Directory -Path $target.Path -Force | Out-Null
        }
        # Clean previously installed Maxilun-owned folders before copying
        Get-ChildItem -Path $target.Path -Directory -ErrorAction SilentlyContinue | Where-Object {
            ($_.Name -eq "maxilun" -or $_.Name -like "maxilun-*" -or $_.Name -like "msal-*") -and
            (Test-Path (Join-Path $_.FullName "SKILL.md")) -and
            ((Get-Content (Join-Path $_.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue) -match '(?m)^  ecosystem:\s*maxilun\s*$')
        } | Remove-Item -Recurse -Force
        Copy-Item -Path "$SkillsSrc\*" -Destination $target.Path -Recurse -Force
        $InstalledTo += "  $($target.Name): $($target.Path)"

        # Copy rules if target supports rules directory
        if ($target.RulesPath -and (Test-Path $RulesSrc)) {
            if (-not (Test-Path $target.RulesPath)) {
                New-Item -ItemType Directory -Path $target.RulesPath -Force | Out-Null
            }
            Copy-Item -Path "$RulesSrc\*" -Destination $target.RulesPath -Recurse -Force
        }
    }
}

Write-Host ""
if ($BackedUp.Count -gt 0) {
    Write-Host "  Previous versions backed up to:" -ForegroundColor Yellow
    foreach ($b in $BackedUp) {
        Write-Host $b -ForegroundColor White
    }
}
Write-Host ""
if ($InstalledTo.Count -eq 0) {
    Write-Host "  No supported AI CLI/IDE detected automatically." -ForegroundColor Yellow
    Write-Host "  Tip: Use 'npx skills add giriedu/maxilun' for interactive skill & agent installation." -ForegroundColor Yellow
} else {
    Write-Host "  Installed successfully to:" -ForegroundColor Green
    foreach ($loc in $InstalledTo) {
        Write-Host $loc -ForegroundColor White
    }
}

Write-Host ""
Write-Host "  18 Specialist Skills (/maxilun, /msal-*):" -ForegroundColor Cyan
$skills = @(
    "1.  maxilun              | Master Orchestrator (/maxilun, /msal)",
    "2.  msal-knowledge-graph | Dependency & Repo Graph (AST/Lens)",
    "3.  msal-scaffold        | Project Context Scaffolder (docs/)",
    "4.  msal-architect       | Architecture & API Design (/msal-think)",
    "5.  msal-sentinel        | Security, Auth, & Privacy",
    "6.  msal-engineer        | Code, Bugfix, & Refactor",
    "7.  msal-data            | Database & Data Layer",
    "8.  msal-frontend        | RSC, App Router, & Server Actions",
    "9.  msal-verify          | QA, E2E, & Regression",
    "10. msal-insight         | Diagnostics & Root Cause",
    "11. msal-deploy          | CI/CD, Docker, & Monitoring",
    "12. msal-docsmith        | Technical Docs & API Contracts",
    "13. msal-craft           | UI/UX & Design Systems",
    "14. msal-motion          | Motion Design & Animation",
    "15. msal-cinecode        | Programmatic Video & Render Pipeline",
    "16. msal-diagrams        | Diagrams & Flow Mapping",
    "17. msal-content         | Copywriting & Brand Voice",
    "18. msal-seo-audit       | Technical SEO & Web Vitals"
)
foreach ($s in $skills) {
    Write-Host "    $s" -ForegroundColor White
}

Write-Host ""
Write-Host "  4 Always-On Engines Active:" -ForegroundColor DarkCyan
Write-Host "    [*] Focus Engine (Executive HUD & Working-Memory Scaffold)" -ForegroundColor Gray
Write-Host "    [*] Purity Engine (Purpose Gate & Zero AI Fluff)" -ForegroundColor Gray
Write-Host "    [*] Minimalist Engineering Engine (The Simplicity Ladder)" -ForegroundColor Gray
Write-Host "    [*] Clarity Engine (High-Density Technical Synthesis)" -ForegroundColor Gray

Write-Host ""
Write-Host "  Type /msal to verify installation." -ForegroundColor Green

# --- Post-Install Verification ---
Write-Host ""
Write-Host "  ──────────────────────────────────────" -ForegroundColor DarkCyan
Write-Host "  Post-Install Verification" -ForegroundColor Cyan
Write-Host "  ──────────────────────────────────────" -ForegroundColor DarkCyan
$VerifyOk = $true
foreach ($loc in $InstalledTo) {
    $parts = $loc.Split(":", 2)
    $platformLabel = $parts[0].Trim()
    $targetDir = $parts[1].Trim()
    $skillFiles = Get-ChildItem -Path $targetDir -Filter "SKILL.md" -Recurse -Depth 2 -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match '[\\/](maxilun|msal-[^\\/]+)[\\/]SKILL\.md$' }
    $count = if ($skillFiles) { @($skillFiles).Count } else { 0 }
    if ($count -ge 18) {
        Write-Host "    $platformLabel : ${count}/18 skills verified" -ForegroundColor Green
    } else {
        Write-Host "    $platformLabel : Only ${count}/18 skills found — reinstall recommended" -ForegroundColor Red
        $VerifyOk = $false
    }
}
if ($PythonAvailable) {
    $kgCli = $null
    foreach ($loc in $InstalledTo) {
        $candidate = Join-Path ($loc.Split(":", 2)[1].Trim()) "msal-knowledge-graph\cli.py"
        if (Test-Path $candidate) {
            $kgCli = $candidate
            break
        }
    }
    if ($kgCli) {
        Write-Host "    Knowledge Graph CLI: Found at $kgCli" -ForegroundColor Green
    } else {
        Write-Host "    Knowledge Graph CLI: cli.py not found in installed skills" -ForegroundColor Yellow
        $VerifyOk = $false
    }
} else {
    Write-Host "    Knowledge Graph CLI: Skipped (Python not available)" -ForegroundColor Gray
}
Write-Host ""
if ($VerifyOk) {
    Write-Host "  All checks passed. Maxilun is fully operational." -ForegroundColor Green
} else {
    Write-Host "  Some checks failed. Review output above and re-run installer if needed." -ForegroundColor Yellow
    exit 1
}
Write-Host ""
