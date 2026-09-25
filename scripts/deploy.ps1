<#
.SYNOPSIS
  Imports the Agentic Use Case Intake solution into a Power Platform environment.

.DESCRIPTION
  Imports the managed (default) or unmanaged package from packages/, optionally with a deployment
  settings file that binds the two connection references and sets environment variables, then
  publishes all customizations. The code app ships inside the solution, so there is nothing to build.

  Prerequisite: PAC CLI signed in to the target environment (pac auth create / pac auth select)
  as a System Administrator.

.EXAMPLE
  .\scripts\deploy.ps1 -EnvironmentUrl https://contoso.crm.dynamics.com -SettingsFile .\packages\deploymentSettings.json
#>
param(
    [Parameter(Mandatory = $true)][string]$EnvironmentUrl,
    [string]$SettingsFile = "",
    [switch]$Unmanaged
)

$ErrorActionPreference = "Stop"
$env:TERM = "dumb"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Solution = "AgenticUseCaseIntake"
$EnvironmentUrl = $EnvironmentUrl.TrimEnd('/')

function Invoke-Pac {
    & pac @args
    if ($LASTEXITCODE -ne 0) { throw "pac $($args -join ' ') failed with exit code $LASTEXITCODE" }
}

$zipName = if ($Unmanaged) { "$Solution.zip" } else { "${Solution}_managed.zip" }
$zip = Join-Path $RepoRoot "packages\$zipName"
Write-Host "Importing $zip into $EnvironmentUrl ..." -ForegroundColor Cyan
$importArgs = @("solution", "import", "--path", $zip, "--environment", $EnvironmentUrl, "--activate-plugins", "--async")
if ($SettingsFile) { $importArgs += @("--settings-file", (Resolve-Path $SettingsFile)) }
Invoke-Pac @importArgs
Invoke-Pac solution publish --environment $EnvironmentUrl

Write-Host ""
Write-Host "Imported. Remaining steps (README 'After importing'):" -ForegroundColor Green
Write-Host "  1. Assign the Agentic Use Case Submitter / Reviewer / Admin roles."
Write-Host "  2. In Copilot Studio, check the agent's tool connections, publish it, and add it to Teams / Microsoft 365 Copilot."
Write-Host "  3. Share the Agentic Use Case Studio and Agentic Use Case Hub apps."
Write-Host "  4. Set a Copilot Credit cap for the agent in the Power Platform admin center."
