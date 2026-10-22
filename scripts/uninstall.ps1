#Requires -Version 5.1
Write-Host ""
Write-Host "  MAXILUN Uninstaller" -ForegroundColor Cyan
Write-Host "  ──────────────────────────────────────" -ForegroundColor DarkCyan
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
            $_.Name -like "maxilun*" -or $_.Name -like "msal*"
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
            $_.Name -match "maxilun|always-on|code-hygiene|purity-catalog"
        }
        if ($ruleFiles) {
            foreach ($file in $ruleFiles) {
                $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
                if ($content -match "(?i)(maxilun|msal)") {
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
