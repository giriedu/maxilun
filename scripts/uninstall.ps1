param(
    [switch]$Project
)

#Requires -Version 5.1
Write-Host ""
Write-Host "  MAXILUN Uninstaller" -ForegroundColor Cyan
Write-Host "  --------------------------------------" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  This will remove all Maxilun skills, plus legacy rule files left by v1 installs." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "  Are you sure you want to continue? [y/N]"
if ($confirm -notmatch '^[Yy]$') {
    Write-Host "  Cancelled." -ForegroundColor Gray
    exit 0
}

$Removed = @()
if ($Project) {
    $CurrentDir = Get-Location
    $Targets = @(
        @{ Name = "Universal / Antigravity / Zed (Project)"; SkillsPath = "$CurrentDir\.agents\skills"; AgentsPath = "$CurrentDir\.agents\agents"; RulesPath = "$CurrentDir\.agents\rules" },
        @{ Name = "Claude Code (Project)";                 SkillsPath = "$CurrentDir\.claude\skills"; AgentsPath = "$CurrentDir\.claude\agents"; RulesPath = "$CurrentDir\.claude\rules" },
        @{ Name = "Trae (Project)";                          SkillsPath = "$CurrentDir\.trae\skills";   AgentsPath = $null; RulesPath = $null },
        @{ Name = "Windsurf (Project)";                      SkillsPath = "$CurrentDir\.windsurf\skills"; AgentsPath = $null; RulesPath = $null },
        @{ Name = "CodeBuddy (Project)";                     SkillsPath = "$CurrentDir\.codebuddy\skills"; AgentsPath = $null; RulesPath = $null }
    )
} else {
    $Targets = @(
        @{ Name = "Antigravity CLI/IDE"; SkillsPath = "$env:USERPROFILE\.agents\skills";          AgentsPath = "$env:USERPROFILE\.agents\agents";          RulesPath = "$env:USERPROFILE\.agents\rules" },
        @{ Name = "Claude Code";         SkillsPath = "$env:USERPROFILE\.claude\skills";          AgentsPath = "$env:USERPROFILE\.claude\agents";          RulesPath = "$env:USERPROFILE\.claude\rules" },
        @{ Name = "Codex";               SkillsPath = "$env:USERPROFILE\.codex\skills";           AgentsPath = $null;                                      RulesPath = "$env:USERPROFILE\.codex\rules" },
        @{ Name = "OpenCode (.config)"; SkillsPath = "$env:USERPROFILE\.config\opencode\skills"; AgentsPath = "$env:USERPROFILE\.config\opencode\agents"; RulesPath = "$env:USERPROFILE\.config\opencode\rules" },
        @{ Name = "OpenCode";            SkillsPath = "$env:USERPROFILE\.opencode\skills";        AgentsPath = "$env:USERPROFILE\.opencode\agents";        RulesPath = "$env:USERPROFILE\.opencode\rules" },
        @{ Name = "Gemini CLI";          SkillsPath = "$env:USERPROFILE\.gemini\config\skills";   AgentsPath = $null;                                      RulesPath = $null },
        @{ Name = "Cursor";              SkillsPath = "$env:USERPROFILE\.cursor\skills";          AgentsPath = $null;                                      RulesPath = $null },
        @{ Name = "Trae";                SkillsPath = "$env:USERPROFILE\.trae\skills";            AgentsPath = $null;                                      RulesPath = $null },
        @{ Name = "Windsurf";            SkillsPath = "$env:USERPROFILE\.windsurf\skills";        AgentsPath = $null;                                      RulesPath = $null },
        @{ Name = "CodeBuddy";           SkillsPath = "$env:USERPROFILE\.codebuddy\skills";       AgentsPath = $null;                                      RulesPath = $null }
    )
}

foreach ($target in $Targets) {
    if (Test-Path $target.SkillsPath) {
        $skillsDirs = Get-ChildItem -Path $target.SkillsPath -Directory -ErrorAction SilentlyContinue | Where-Object {
            ($_.Name -eq "maxilun" -or $_.Name -like "maxilun-*" -or $_.Name -like "msal-*") -and
            (Test-Path (Join-Path $_.FullName "SKILL.md")) -and
            ((Get-Content (Join-Path $_.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue) -match '(?m)^  ecosystem:\s*maxilun\s*$')
        }
        if ($skillsDirs) {
            foreach ($dir in $skillsDirs) {
                Remove-Item -Path $dir.FullName -Recurse -Force
            }
            $Removed += "$($target.Name) (skills): $($target.SkillsPath)"
            Write-Host "  Removed Maxilun/MSAL skills from: $($target.SkillsPath)" -ForegroundColor Green
        }
    }

    if ($target.AgentsPath -and (Test-Path $target.AgentsPath)) {
        $agentFiles = Get-ChildItem -Path $target.AgentsPath -File -Filter "maxilun-*.md" -ErrorAction SilentlyContinue
        if ($agentFiles) {
            foreach ($af in $agentFiles) {
                Remove-Item -Path $af.FullName -Force
            }
            $Removed += "$($target.Name) (agents): $($target.AgentsPath)"
            Write-Host "  Removed Maxilun agent definitions from: $($target.AgentsPath)" -ForegroundColor Green
        }
    }

    if ($target.RulesPath -and (Test-Path $target.RulesPath)) {
        $ruleFiles = Get-ChildItem -Path $target.RulesPath -File -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -in @("always-on.md", "maxilun-global.md", "code-hygiene.md", "purity-catalog.md")
        }
        if ($ruleFiles) {
            foreach ($file in $ruleFiles) {
                $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
                $ownedRule = switch ($file.Name) {
                    "maxilun-global.md" { $content -match '(?m)^# Aturan Global Maxilun' }
                    "always-on.md" { $content -match '(?m)^# (Tujuh Mesin Wajib Maxilun|Four Always-On Engines and Three Operating Protocols|Maxilun Always-On)' }
                    "code-hygiene.md" { $content -match '(?m)^# Maxilun Code Hygiene Rules' }
                    "purity-catalog.md" { $content -match '(?m)^# Maxilun Purity Catalog' }
                    default { $false }
                }
                if ($ownedRule) {
                    Remove-Item -Path $file.FullName -Force
                }
            }
            $Removed += "$($target.Name) (legacy rules): $($target.RulesPath)"
            Write-Host "  Removed legacy Maxilun rule files from: $($target.RulesPath)" -ForegroundColor Green
        }
    }
}

Write-Host ""
if ($Removed.Count -eq 0) {
    Write-Host "  No Maxilun installation found." -ForegroundColor Yellow
} else {
    Write-Host "  Maxilun removed from $($Removed.Count) location(s)." -ForegroundColor Green
}
Write-Host ""
