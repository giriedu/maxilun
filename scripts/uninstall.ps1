#Requires -Version 5.1
Write-Host ""
Write-Host "  MAXILUN Uninstaller" -ForegroundColor Cyan
Write-Host "  --------------------------------------" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  This will remove all Maxilun skills and rules from your system." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "  Are you sure you want to continue? [y/N]"
if ($confirm -notmatch '^[Yy]$') {
    Write-Host "  Cancelled." -ForegroundColor Gray
    exit 0
}

$Removed = @()
$Targets = @(
    @{ Name = "Antigravity CLI/IDE"; SkillsPath = "$env:USERPROFILE\.agents\skills"; RulesPath = "$env:USERPROFILE\.agents\rules" },
    @{ Name = "Claude Code";         SkillsPath = "$env:USERPROFILE\.claude\skills"; RulesPath = "$env:USERPROFILE\.claude\rules" },
    @{ Name = "Codex";               SkillsPath = "$env:USERPROFILE\.codex\skills"; RulesPath = "$env:USERPROFILE\.codex\rules" },
    @{ Name = "OpenCode";            SkillsPath = "$env:USERPROFILE\.config\opencode\skills"; RulesPath = "$env:USERPROFILE\.config\opencode\rules" },
    @{ Name = "Gemini CLI";          SkillsPath = "$env:USERPROFILE\.gemini\config\skills"; RulesPath = $null },
    @{ Name = "Cursor";              SkillsPath = "$env:USERPROFILE\.cursor\skills"; RulesPath = $null },
    @{ Name = "Trae";                SkillsPath = "$env:USERPROFILE\.trae\skills"; RulesPath = $null },
    @{ Name = "CodeBuddy";           SkillsPath = "$env:USERPROFILE\.codebuddy\skills"; RulesPath = $null }
)

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

    if ($target.RulesPath -and (Test-Path $target.RulesPath)) {
        $ruleFiles = Get-ChildItem -Path $target.RulesPath -File -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -in @("always-on.md", "code-hygiene.md", "purity-catalog.md")
        }
        if ($ruleFiles) {
            foreach ($file in $ruleFiles) {
                $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
                $ownedRule = switch ($file.Name) {
                    "always-on.md" { $content -match '(?m)^# (Tujuh Mesin Wajib Maxilun|Four Always-On Engines and Three Operating Protocols|Maxilun Always-On)' }
                    "code-hygiene.md" { $content -match '(?m)^# Maxilun Code Hygiene Rules' }
                    "purity-catalog.md" { $content -match '(?m)^# Maxilun Purity Catalog' }
                    default { $false }
                }
                if ($ownedRule) {
                    Remove-Item -Path $file.FullName -Force
                }
            }
            $Removed += "$($target.Name) (rules): $($target.RulesPath)"
            Write-Host "  Removed Maxilun rules from: $($target.RulesPath)" -ForegroundColor Green
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
