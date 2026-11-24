param(
    [switch]$Project
)

#Requires -Version 5.1
$Version = "1.3.0"
Write-Host ""
Write-Host "  MAXILUN $Version Installer" -ForegroundColor Cyan
Write-Host "  27 skills + 21 autonomous agents" -ForegroundColor DarkCyan
Write-Host ""

$ScriptDir = Split-Path -Parent $PSScriptRoot
$SkillsSrc = Join-Path $ScriptDir "skills"
if (-not (Test-Path $SkillsSrc)) {
    $SkillsSrc = Join-Path $ScriptDir ".agents\skills"
}
$AgentsSrc = Join-Path $ScriptDir "agents"
$ExpectedSkillCount = @(Get-ChildItem -Path $SkillsSrc -Directory -ErrorAction SilentlyContinue | Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }).Count
if ($ExpectedSkillCount -eq 0) { $ExpectedSkillCount = 25 }

$InstalledTo = @()
$BackedUp = @()
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmssfff"

# --- Python Dependency Check (Knowledge Graph) ---
$PythonAvailable = $false
$PyExe = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $verOutput = & $cmd --version 2>&1
        if ($verOutput -match '(\d+)\.(\d+)') {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 8)) {
                $PythonAvailable = $true
                # Absolute interpreter path: `python` may be the Store stub or absent (only `py`).
                $PyExe = ((& $cmd -c "import sys; print(sys.executable)") | Select-Object -First 1) -replace '\\','/'
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

$AgentsInstalled = @()

# Copy agent definitions (*.md only). Owned maxilun-*.md files are removed first so
# renamed/removed agents never linger. Format "omp" rewrites frontmatter for OMP:
# drops the `model:` line (OMP model selector) and lowercases tool names.
function Install-Agents([string]$Name, [string]$AgentsPath, [string]$Format = "claude") {
    if (-not (Test-Path $AgentsSrc)) { return }
    New-Item -ItemType Directory -Path $AgentsPath -Force -ErrorAction Stop | Out-Null
    Get-ChildItem -LiteralPath $AgentsPath -File -Filter "maxilun-*.md" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction Stop
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    foreach ($agent in Get-ChildItem -LiteralPath $AgentsSrc -File -Filter "*.md") {
        $dest = Join-Path $AgentsPath $agent.Name
        if ($Format -eq "omp") {
            $out = New-Object System.Collections.Generic.List[string]
            $inFrontmatter = $false
            $lineNo = 0
            foreach ($line in [System.IO.File]::ReadAllLines($agent.FullName)) {
                $lineNo++
                if ($lineNo -eq 1 -and $line -match '^---') { $inFrontmatter = $true; $out.Add($line); continue }
                if ($inFrontmatter) {
                    if ($line -match '^---') { $inFrontmatter = $false }
                    elseif ($line -match '^model:') { continue }
                    elseif ($line -cmatch '^  - (Read|Grep|Glob|Bash|Write|Edit)\s*$') { $line = "  - " + $Matches[1].ToLowerInvariant() }
                }
                $out.Add($line)
            }
            [System.IO.File]::WriteAllText($dest, (($out -join "`n") + "`n"), $utf8NoBom)
        } else {
            Copy-Item -LiteralPath $agent.FullName -Destination $dest -Force -ErrorAction Stop
        }
    }
    $script:AgentsInstalled += "  ${Name}: $AgentsPath"
}

$U = $env:USERPROFILE
$AgentsOnlyTargets = @()
if ($Project) {
    $CurrentDir = Get-Location
    $Targets = @(
        @{ Name = "Universal / Antigravity / Zed (Project)"; Path = "$CurrentDir\.agents\skills"; AgentsPath = "$CurrentDir\.agents\agents"; LegacyRules = "$CurrentDir\.agents\rules" },
        @{ Name = "OpenCode (Project)";                      Path = "$CurrentDir\.opencode\skills"; AgentsPath = "$CurrentDir\.opencode\agents"; LegacyRules = "$CurrentDir\.opencode\rules" },
        @{ Name = "[CC] / Termul (Project)";                 Path = "$CurrentDir\.claude\skills"; AgentsPath = "$CurrentDir\.claude\agents"; LegacyRules = "$CurrentDir\.claude\rules" },
        @{ Name = "Trae (Project)";                          Path = "$CurrentDir\.trae\skills";   AgentsPath = $null; LegacyRules = $null },
        @{ Name = "Windsurf (Project)";                      Path = "$CurrentDir\.windsurf\skills"; AgentsPath = $null; LegacyRules = $null },
        @{ Name = "CodeBuddy (Project)";                     Path = "$CurrentDir\.codebuddy\skills"; AgentsPath = $null; LegacyRules = $null }
    )
    $AgentsOnlyTargets += @{ Name = "OMP (Project)"; AgentsPath = "$CurrentDir\.omp\agents" }
} else {
    $Targets = @(
        @{ Name = "Antigravity CLI/IDE & Zed"; Path = "$U\.agents\skills"; AgentsPath = "$U\.agents\agents"; LegacyRules = "$U\.agents\rules" },
        @{ Name = "[CC] & Termul";             Path = "$U\.claude\skills"; AgentsPath = "$U\.claude\agents"; LegacyRules = "$U\.claude\rules" }
    )
    if (Test-Path "$U\.omp") { $AgentsOnlyTargets += @{ Name = "OMP"; AgentsPath = "$U\.omp\agent\agents" } }
    if (Test-Path "$U\.codex") { $Targets += @{ Name = "Codex"; Path = "$U\.codex\skills"; AgentsPath = "$U\.codex\agents"; LegacyRules = "$U\.codex\rules" } }
    if (Test-Path "$U\.config\opencode") {
        $Targets += @{ Name = "OpenCode"; Path = "$U\.config\opencode\skills"; AgentsPath = "$U\.config\opencode\agents"; LegacyRules = "$U\.config\opencode\rules" }
    } elseif (Test-Path "$U\.opencode") {
        $Targets += @{ Name = "OpenCode"; Path = "$U\.opencode\skills"; AgentsPath = "$U\.opencode\agents"; LegacyRules = "$U\.opencode\rules" }
    }
    if (Test-Path "$U\.gemini\config\skills") {
        $Targets += @{ Name = "Gemini CLI / Antigravity Config"; Path = "$U\.gemini\config\skills"; AgentsPath = $null; LegacyRules = $null }
    }
    if (Test-Path "$U\.gemini")    { $Targets += @{ Name = "Gemini CLI"; Path = "$U\.gemini\skills";    AgentsPath = $null; LegacyRules = "$U\.gemini\rules" } }
    if (Test-Path "$U\.cursor")    { $Targets += @{ Name = "Cursor";     Path = "$U\.cursor\skills";    AgentsPath = $null; LegacyRules = $null } }
    if (Test-Path "$U\.trae")      { $Targets += @{ Name = "Trae";       Path = "$U\.trae\skills";      AgentsPath = $null; LegacyRules = $null } }
    if (Test-Path "$U\.windsurf")  { $Targets += @{ Name = "Windsurf";   Path = "$U\.windsurf\skills";  AgentsPath = $null; LegacyRules = $null } }
    if (Test-Path "$U\.codebuddy") { $Targets += @{ Name = "CodeBuddy";  Path = "$U\.codebuddy\skills"; AgentsPath = $null; LegacyRules = $null } }
}

foreach ($target in $Targets) {
    $parentDir = Split-Path -Parent $target.Path

    $existingMaxilun = @()
    if (Test-Path $target.Path -PathType Container) {
        $existingMaxilun = @(Get-ChildItem -Path $target.Path -Directory -ErrorAction SilentlyContinue | Where-Object {
            ($_.Name -eq "maxilun" -or $_.Name -like "maxilun-*" -or $_.Name -like "msal-*") -and
            (Test-Path (Join-Path $_.FullName "SKILL.md")) -and
            ((Get-Content (Join-Path $_.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue) -match '(?m)^  ecosystem:\s*maxilun\s*$')
        })
    }

    if ($existingMaxilun.Count -gt 0) {
        $backupRoot = Join-Path $parentDir "_maxilun_backup_$Timestamp"
        $backupSkills = Join-Path $backupRoot "skills"
        New-Item -ItemType Directory -Path $backupSkills -Force -ErrorAction Stop | Out-Null
        foreach ($dir in $existingMaxilun) {
            Copy-Item -Path $dir.FullName -Destination (Join-Path $backupSkills $dir.Name) -Recurse -Force -ErrorAction Stop
        }
        $BackedUp += "  $($target.Name): $backupRoot"
        $existingMaxilun | Remove-Item -Recurse -Force

        # Keep at most 2 most recent backups to prevent disk bloat
        $oldBackups = @(Get-ChildItem -Path $parentDir -Directory -Filter "_maxilun_backup_*" -ErrorAction SilentlyContinue | Sort-Object Name -Descending)
        if ($oldBackups.Count -gt 2) {
            $oldBackups | Select-Object -Skip 2 | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    New-Item -ItemType Directory -Path $target.Path -Force -ErrorAction Stop | Out-Null

    foreach ($skillDir in Get-ChildItem -LiteralPath $SkillsSrc -Directory) {
        $dest = Join-Path $target.Path $skillDir.Name
        if (Test-Path -LiteralPath $dest) {
            Copy-Item -Path (Join-Path $skillDir.FullName "*") -Destination $dest -Recurse -Force -ErrorAction Stop
        } else {
            Copy-Item -LiteralPath $skillDir.FullName -Destination $dest -Recurse -Force -ErrorAction Stop
        }
        # Never ship bytecode or local scan caches (scoped to the skill just copied)
        foreach ($cacheDir in @("__pycache__", ".maxilun", "maxilun-out")) {
            Get-ChildItem -LiteralPath $dest -Directory -Recurse -Force -Filter $cacheDir -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        }
        Get-ChildItem -LiteralPath $dest -File -Recurse -Force -Filter "*.pyc" -ErrorAction SilentlyContinue |
            Remove-Item -Force -ErrorAction SilentlyContinue
    }

    if ($target.AgentsPath) {
        Install-Agents -Name $target.Name -AgentsPath $target.AgentsPath
    }
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

foreach ($target in $AgentsOnlyTargets) {
    Install-Agents -Name $target.Name -AgentsPath $target.AgentsPath -Format "omp"
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
if ($AgentsInstalled.Count -gt 0) {
    Write-Host "  Agents installed to:" -ForegroundColor Green
    foreach ($loc in $AgentsInstalled) { Write-Host $loc -ForegroundColor White }
}

# Register the knowledge graph as a native MCP tool in Claude Code (idempotent),
# so agents call kg_locate instead of falling back to grep.
if ((Get-Command claude -ErrorAction SilentlyContinue) -and $PyExe) {
    & claude mcp get maxilun-kg *> $null
    if ($LASTEXITCODE -ne 0) {
        $kgCandidates = @(
            @{ Path = "$CurrentDir\.claude\skills\maxilun-knowledge-graph\mcp_server.py"; Scope = "project" },
            @{ Path = "$env:USERPROFILE\.claude\skills\maxilun-knowledge-graph\mcp_server.py"; Scope = "user" }
        )
        foreach ($kg in $kgCandidates) {
            if (Test-Path $kg.Path) {
                & claude mcp add --scope $kg.Scope maxilun-kg -- $PyExe ($kg.Path -replace '\\','/') *> $null
                if ($LASTEXITCODE -eq 0) { Write-Host "  maxilun-kg MCP server registered in Claude Code ($($kg.Scope) scope)" -ForegroundColor Green }
                break
            }
        }
    }
}

# Codex: register maxilun-kg in ~/.codex/config.toml when absent.
$codexCfg = "$env:USERPROFILE\.codex\config.toml"
$codexKg = "$env:USERPROFILE/.codex/skills/maxilun-knowledge-graph/mcp_server.py" -replace '\\','/'
if ($PyExe -and (Test-Path $codexCfg) -and (Test-Path $codexKg) -and -not (Select-String -Path $codexCfg -Pattern '^\[mcp_servers\.maxilun-kg\]' -Quiet)) {
    Add-Content -Path $codexCfg -Encoding utf8 -Value "`n[mcp_servers.maxilun-kg]`ncommand = `"$PyExe`"`nargs = [`"$codexKg`"]"
    Write-Host "  maxilun-kg MCP server registered in Codex" -ForegroundColor Green
}

# Council mode survives compaction via a UserPromptSubmit hook (idempotent).
$councilHook = "$env:USERPROFILE\.claude\skills\maxilun\scripts\council_hook.py"
# No `claude` CLI check: the desktop app reads ~/.claude/settings.json without it on PATH.
if ($PyExe -and (Test-Path $councilHook)) {
    & $PyExe $councilHook --install
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
    if ($count -ge $ExpectedSkillCount) {
        Write-Host "    $platformLabel : ${count}/${ExpectedSkillCount} skills" -ForegroundColor Green
    } else {
        Write-Host "    $platformLabel : only ${count}/${ExpectedSkillCount} skills -- reinstall recommended" -ForegroundColor Red
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
