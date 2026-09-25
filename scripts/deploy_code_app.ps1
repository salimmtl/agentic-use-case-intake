param(
    [string]$SolutionName = "AgenticUseCaseIntake"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$AppRoot = Join-Path $RepoRoot "code-app"
$ConfigPath = Join-Path $AppRoot "src\config.generated.ts"

function ConvertTo-TypeScriptString([string]$Value) {
    return ($Value | ConvertTo-Json -Compress)
}

Push-Location $RepoRoot
try {
    $envJson = python .\scripts\read_env_vars.py
    if ($LASTEXITCODE -ne 0) { throw "read_env_vars.py failed with exit code $LASTEXITCODE" }
    $envVars = $envJson | ConvertFrom-Json

    $config = @"
import type { AppConfig } from './domain';

export const APP_CONFIG: AppConfig = {
  intakeAgentUrl: $(ConvertTo-TypeScriptString $envVars.sams_IntakeAgentUrl),
  toolGuideUrl: $(ConvertTo-TypeScriptString $envVars.sams_ToolGuideUrl),
  creditsGuideUrl: $(ConvertTo-TypeScriptString $envVars.sams_CreditsGuideUrl),
};
"@
    Set-Content -Path $ConfigPath -Value $config -Encoding utf8
}
finally {
    Pop-Location
}

Push-Location $AppRoot
try {
    npx prettier --write src/config.generated.ts --print-width 110 --single-quote
    if ($LASTEXITCODE -ne 0) { throw "prettier failed with exit code $LASTEXITCODE" }

    npm run build
    if ($LASTEXITCODE -ne 0) { throw "npm run build failed with exit code $LASTEXITCODE" }

    $env:TERM = "dumb"
    pac code push -s $SolutionName
    if ($LASTEXITCODE -ne 0) { throw "pac code push failed with exit code $LASTEXITCODE" }

    # PAC can upload the draft but time out on the publish POST while returning success.
    # Publish explicitly with the same active PAC auth token so the live app matches the pushed draft.
    $powerConfig = Get-Content .\power.config.json -Raw | ConvertFrom-Json
    if ($powerConfig.appId) {
        $tokenLine = pac auth token | Where-Object { $_ -like "Token:*" } | Select-Object -First 1
        $token = ($tokenLine -replace "^Token:\s*", "").Trim()
        if (-not $token) { throw "Could not get PAC auth token for publish verification" }

        $compactEnvironmentId = ($powerConfig.environmentId -replace "-", "")
        $environmentHost = "{0}.{1}" -f $compactEnvironmentId.Substring(0, 30), $compactEnvironmentId.Substring(30)
        $publishUrl = "https://$environmentHost.environment.api.powerplatform.com/powerapps/apps/$($powerConfig.appId)/publish?api-version=1"
        Invoke-RestMethod -Method Post -Uri $publishUrl -Headers @{ Authorization = "Bearer $token" } -TimeoutSec 300 | Out-Null
        Write-Host "Published app via Power Apps API."
    }
}
finally {
    Pop-Location
}
