#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateSet('companies', 'production_units', 'relations', 'company_ownership')][string]$Table,
    [Parameter(Mandatory)][string]$CompanyCsv,
    [Parameter(Mandatory)][string]$ComparisonCsv,
    [Parameter(Mandatory)][string]$OutputCsv,
    [char]$CompanyDelimiter = ',',
    [char]$ComparisonDelimiter = ','
)

$ErrorActionPreference = 'Stop'
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputCsv)
if (Test-Path -LiteralPath $outputPath) { throw 'Choose a new output CSV.' }
$columns = @{
    companies = @('cvr', 'cvr_registered_name', 'current_cvr_status', 'cvr_secondary_names', 'cvr_start_date', 'cvr_end_date')
    production_units = @(
        'cvr', 'p_number', 'source_status', 'registered_name', 'registered_address',
        'postal_code_and_city', 'main_industry_code', 'main_industry_name', 'start_date', 'end_date'
    )
    relations = @(
        'cvr', 'bfe', 'role', 'source_status', 'virkning_fra_original',
        'actual_share_state', 'actual_share_numerator', 'actual_share_denominator',
        'registered_share_state', 'registered_share_numerator', 'registered_share_denominator'
    )
    company_ownership = @(
        'company_cvr', 'registered_company_name', 'owner_cvr', 'registered_owner_name',
        'capital_share_display', 'vote_share_display', 'effective_from', 'effective_to',
        'displayed_owner_change_date', 'disposal_date'
    )
}
$fields = $columns[$Table]
$counts = [System.Collections.Generic.Dictionary[string,object]]::new([System.StringComparer]::Ordinal)

foreach ($file in @(
    @{ Path = $CompanyCsv; CountField = 'company_count'; Delimiter = $CompanyDelimiter },
    @{ Path = $ComparisonCsv; CountField = 'comparison_count'; Delimiter = $ComparisonDelimiter }
)) {
    $header = Get-Content -LiteralPath $file.Path -TotalCount 1 -Encoding UTF8
    $names = @($header -split [regex]::Escape($file.Delimiter) | ForEach-Object { $_.Trim('"') })
    foreach ($field in $fields) {
        if ($names -cnotcontains $field) { throw "Missing field $field in $($file.Path)." }
    }
    foreach ($row in (Import-Csv -LiteralPath $file.Path -Encoding UTF8 -Delimiter $file.Delimiter)) {
        $values = [string[]]@($fields | ForEach-Object { [string]$row.$_ })
        $key = ConvertTo-Json -InputObject $values -Compress
        if (-not $counts.ContainsKey($key)) {
            $record = [ordered]@{ company_count = 0; comparison_count = 0 }
            foreach ($field in $fields) { $record[$field] = $row.$field }
            $counts[$key] = $record
        }
        $counts[$key][$file.CountField]++
    }
}

$different = @(
    foreach ($key in ($counts.Keys | Sort-Object -CaseSensitive)) {
        $record = $counts[$key]
        if ($record.company_count -ne $record.comparison_count) { [pscustomobject]$record }
    }
)
$lines = @($different | ConvertTo-Csv -NoTypeInformation)
if ($lines.Count -eq 0) { $lines = @(('company_count', 'comparison_count' + $fields) -join ',') }
[System.IO.File]::WriteAllLines($outputPath, [string[]]$lines, [System.Text.UTF8Encoding]::new($true))
Write-Host "$($different.Count) distinct rows have different occurrence counts."
