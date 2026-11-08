#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ScopeCsv,
    [Parameter(Mandatory)][string]$OutputFolder
)

$ErrorActionPreference = 'Stop'
$cvrs = @(Import-Csv -LiteralPath $ScopeCsv -Encoding UTF8 | ForEach-Object { $_.cvr })
if ($cvrs.Count -eq 0 -or @($cvrs | Where-Object { $_ -cnotmatch '^[0-9]{8}$' }).Count -gt 0 -or
    @($cvrs | Sort-Object -Unique).Count -ne $cvrs.Count) {
    throw 'The scope CSV needs one unique eight-digit CVR per row in the cvr column.'
}

$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputFolder)
if (Test-Path -LiteralPath $outputPath) { throw 'Choose a new output folder.' }
$null = New-Item -ItemType Directory -Path $outputPath
$labsPath = Join-Path $outputPath 'labs'
$null = New-Item -ItemType Directory -Path $labsPath
$logPath = Join-Path $outputPath 'lookups.csv'

$failed = $false
foreach ($cvr in $cvrs) {
    $url = "https://api.labs.matriklen.dk/CvrEjerskaber?cvr=$cvr"
    $file = Join-Path $labsPath "$cvr.json"
    $lookup = [ordered]@{
        cvr = $cvr; url = $url; lookup_at = ''; outcome = ''; http_status = ''
        raw_file = ''; sha256 = ''; detail = ''
    }
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 45 -MaximumRedirection 0
        $lookup.http_status = [int]$response.StatusCode
        if ($lookup.http_status -ne 200) { throw "HTTP $($lookup.http_status)" }
        [System.IO.File]::WriteAllBytes("$file.part", $response.RawContentStream.ToArray())
        $hash = (Get-FileHash -LiteralPath "$file.part" -Algorithm SHA256).Hash.ToLowerInvariant()
        [System.IO.File]::Move("$file.part", $file)
        $lookup.raw_file = "labs/$cvr.json"
        $lookup.sha256 = $hash
        $lookup.outcome = 'downloaded'
    } catch {
        $failed = $true
        if ($null -ne $_.Exception.Response) { $lookup.http_status = [int]$_.Exception.Response.StatusCode }
        $lookup.outcome = if ($lookup.http_status -in 401, 403) { 'access_denied' } else { 'error' }
        $lookup.detail = $_.Exception.Message
        if (Test-Path -LiteralPath "$file.part") { Remove-Item -LiteralPath "$file.part" }
        Write-Warning "CVR $cvr failed. $($lookup.detail)"
    }
    $lookup.lookup_at = [datetimeoffset]::UtcNow.ToString('o')
    [pscustomobject]$lookup | Export-Csv -LiteralPath $logPath -Append -Encoding UTF8 -NoTypeInformation
}
if ($failed) { exit 2 }
