#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputFolder,
    [Parameter(Mandatory)][string]$OutputFolder,
    [switch]$UseSavedLabs
)

$ErrorActionPreference = 'Stop'
$labsBase = 'https://api.labs.matriklen.dk/CvrEjerskaber?cvr='
$cvrBase = 'https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer='
$jsonOptions = @{}
if ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('DateKind')) {
    $jsonOptions.DateKind = 'String'
}
$roles = @('administrerer', 'ejer')
$relationFields = @(
    'cvr', 'bfe', 'role', 'source_status', 'virkning_fra_original',
    'actual_share_state', 'actual_share_numerator', 'actual_share_denominator',
    'registered_share_state', 'registered_share_numerator', 'registered_share_denominator'
)
$unitFields = @(
    'cvr', 'p_number', 'source_status', 'registered_name', 'registered_address',
    'postal_code_and_city', 'main_industry_code', 'main_industry_name', 'start_date', 'end_date'
)
$companyFields = @('cvr', 'cvr_registered_name', 'current_cvr_status', 'cvr_secondary_names', 'cvr_start_date', 'cvr_end_date')
$lookupFields = @('cvr', 'source', 'url', 'lookup_at', 'outcome', 'active_units', 'closed_units', 'rows', 'raw_file', 'sha256', 'detail')

function Read-JsonFile($Path) {
    $json = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ($json -notmatch '^\s*\{') { throw 'Expected a JSON object.' }
    try {
        ConvertFrom-Json -InputObject $json @jsonOptions
    } catch {
        throw 'The file could not be parsed as JSON.'
    }
}

function Assert-Fields($Record, $Fields, $Context) {
    if ($Record -isnot [pscustomobject]) { throw "Expected an object for $Context." }
    foreach ($field in $Fields) {
        if ($Record.PSObject.Properties.Name -cnotcontains $field) { throw "Missing $field in $Context." }
    }
}

function Write-Table($Path, $Rows, $Fields) {
    $lines = @($Rows | ConvertTo-Csv -NoTypeInformation)
    if ($lines.Count -eq 0) {
        $lines = @(($Fields -join ','))
    }
    [System.IO.File]::WriteAllLines($Path, [string[]]$lines, [System.Text.UTF8Encoding]::new($true))
}

function Read-Share($Observation, $Field) {
    $property = $Observation.PSObject.Properties[$Field]
    if ($null -eq $property) { return @{ State = 'missing' } }
    $value = $property.Value
    if ($null -eq $value) { return @{ State = 'null' } }
    $numerator = $value.tæller
    $denominator = $value.nævner
    if (($numerator -is [int] -or $numerator -is [long]) -and
        ($denominator -is [int] -or $denominator -is [long]) -and
        $numerator -ge 0 -and $denominator -gt 0) {
        return @{ State = 'present'; Numerator = $numerator; Denominator = $denominator }
    }
    return @{ State = 'invalid' }
}

function Read-Labs($Path, $Cvr) {
    $payload = Read-JsonFile $Path
    if ($payload -isnot [pscustomobject] -or @($payload.PSObject.Properties.Name).Count -ne 2 -or
        $payload.administrerer -isnot [array] -or $payload.ejer -isnot [array]) {
        throw 'Expected a Labs object containing administrerer and ejer arrays.'
    }
    foreach ($role in $roles) {
        foreach ($observation in $payload.$role) {
            if ($observation -isnot [pscustomobject]) { throw 'Expected a Labs observation object.' }
            $bfe = $observation.bfe
            if (($bfe -isnot [string] -and $bfe -isnot [int] -and $bfe -isnot [long]) -or
                [string]$bfe -cnotmatch '^[0-9]*[1-9][0-9]*$') { $bfe = '' }
            $status = $observation.status
            if ($status -isnot [string]) { $status = '' }
            $date = $observation.virkningFra
            if ($date -isnot [string]) { $date = '' }
            $actual = Read-Share $observation 'faktiskEjerandel'
            $registered = Read-Share $observation 'tinglystEjerandel'
            [pscustomobject][ordered]@{
                cvr = $Cvr
                bfe = [string]$bfe
                role = $role
                source_status = $status
                virkning_fra_original = $date
                actual_share_state = $actual.State
                actual_share_numerator = $actual.Numerator
                actual_share_denominator = $actual.Denominator
                registered_share_state = $registered.State
                registered_share_numerator = $registered.Numerator
                registered_share_denominator = $registered.Denominator
            }
        }
    }
}

function Read-Cvr($Path, $Cvr) {
    $payload = Read-JsonFile $Path
    $company = $payload.stamdata
    Assert-Fields $company @('cvrnummer', 'navn', 'status', 'startdato', 'ophoersdato') 'company'
    if ([string]$company.cvrnummer -cne $Cvr -or -not $company.navn -or -not $company.status) {
        throw 'CVR identity or company fields do not match the requested CVR.'
    }
    if ($payload.udvidedeOplysninger.binavne -isnot [array]) { throw 'Expected the secondary names array.' }
    $lists = $payload.produktionsenheder
    if ($lists.aktiveProduktionsenheder -isnot [array] -or $lists.ophoerteProduktionsenheder -isnot [array]) {
        throw 'Expected both the active and closed P-enhed arrays.'
    }
    $status = switch -CaseSensitive ($company.status) {
        'NORMAL' { 'Normal' }
        'OPLØSTEFTERFUSION' { 'Opløst efter fusion' }
        default { $company.status }
    }
    $companyRow = [pscustomobject][ordered]@{
        cvr = $Cvr
        cvr_registered_name = $company.navn
        current_cvr_status = $status
        cvr_secondary_names = $payload.udvidedeOplysninger.binavne -join '|'
        cvr_start_date = $company.startdato
        cvr_end_date = $company.ophoersdato
    }
    $unitRows = @(
        foreach ($group in @('aktiveProduktionsenheder', 'ophoerteProduktionsenheder')) {
            $unitStatus = if ($group -eq 'aktiveProduktionsenheder') { 'active' } else { 'closed' }
            foreach ($item in $lists.$group) {
                $unit = $item.stamdata
                Assert-Fields $unit @(
                    'cvrnummer', 'pnummer', 'navn', 'adresse', 'postnummerOgBy', 'hovedbranche', 'startdato', 'ophoersdato'
                ) 'P-enhed'
                if ([string]$unit.cvrnummer -cne $Cvr -or [string]$unit.pnummer -cnotmatch '^[0-9]{10}$') {
                    throw 'A P-enhed has an unexpected CVR or P-number.'
                }
                if ($null -ne $unit.hovedbranche) {
                    Assert-Fields $unit.hovedbranche @('branchekode', 'titel') 'P-enhed industry'
                }
                [pscustomobject][ordered]@{
                    cvr = $Cvr
                    p_number = [string]$unit.pnummer
                    source_status = $unitStatus
                    registered_name = $unit.navn
                    registered_address = $unit.adresse
                    postal_code_and_city = $unit.postnummerOgBy
                    main_industry_code = [string]$unit.hovedbranche.branchekode
                    main_industry_name = $unit.hovedbranche.titel
                    start_date = $unit.startdato
                    end_date = $unit.ophoersdato
                }
            }
        }
    )
    if ($unitRows.Count -ne @($unitRows | Select-Object -ExpandProperty p_number -Unique).Count) {
        throw 'A P-number occurs more than once for the CVR.'
    }
    return @{
        Company = $companyRow; Units = $unitRows
        Active = $lists.aktiveProduktionsenheder.Count
        Closed = $lists.ophoerteProduktionsenheder.Count
    }
}

$inputPath = (Resolve-Path -LiteralPath $InputFolder).ProviderPath
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputFolder)
if (Test-Path -LiteralPath $outputPath) { throw 'Choose a new output folder for each run.' }
$scope = @(Import-Csv -LiteralPath (Join-Path $inputPath 'scope.csv') -Encoding UTF8)
$cvrs = @($scope | ForEach-Object { $_.cvr })
if ($scope.Count -eq 0 -or $cvrs.Count -ne $scope.Count -or
    @($cvrs | Where-Object { $_ -cnotmatch '^[0-9]{8}$' }).Count -gt 0 -or
    @($cvrs | Sort-Object -Unique).Count -ne $scope.Count) {
    throw 'scope.csv needs one unique eight-digit CVR per row in the cvr column.'
}

$captures = @{}
$captureFile = Join-Path $inputPath 'captures.csv'
if (Test-Path -LiteralPath $captureFile -PathType Leaf) {
    foreach ($capture in (Import-Csv -LiteralPath $captureFile -Encoding UTF8)) {
        $key = "$($capture.cvr)/$($capture.source)"
        $expectedUrl = if ($capture.source -ceq 'labs') {
            "$labsBase$($capture.cvr)"
        } else {
            "$cvrBase$($capture.cvr)&locale=da"
        }
        $parsedTime = [datetimeoffset]::MinValue
        if ($cvrs -cnotcontains $capture.cvr -or @('labs', 'cvr') -cnotcontains $capture.source -or
            $capture.url -cne $expectedUrl -or $captures.ContainsKey($key) -or
            @('saved', 'access_denied', 'technical_error', 'partial', 'invalid_response') -cnotcontains $capture.outcome -or
            $capture.lookup_at -cnotmatch '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$' -or
            -not [datetimeoffset]::TryParse($capture.lookup_at, [ref]$parsedTime)) {
            throw "Invalid or repeated capture for $key. Check captures.csv."
        }
        $captures[$key] = $capture
    }
}

$stage = Join-Path (Split-Path -Parent $outputPath) ('.backbone-' + [guid]::NewGuid().ToString('N'))
$rawPath = Join-Path $stage 'raw/matriklen-labs'
$null = New-Item -ItemType Directory -Path $rawPath -Force
$relations = [System.Collections.Generic.List[object]]::new()
$companies = [System.Collections.Generic.List[object]]::new()
$units = [System.Collections.Generic.List[object]]::new()
$lookups = [System.Collections.Generic.List[object]]::new()

try {
    foreach ($cvr in ($cvrs | Sort-Object)) {
        foreach ($source in @('labs', 'cvr')) {
            $live = $source -eq 'labs' -and -not $UseSavedLabs
            $capture = $captures["$cvr/$source"]
            $lookup = [ordered]@{
                cvr = $cvr; source = $source; url = ''; lookup_at = ''; outcome = 'not_checked'
                active_units = ''; closed_units = ''; rows = ''; raw_file = ''; sha256 = ''; detail = ''
            }
            $lookup.url = if ($source -eq 'labs') { "$labsBase$cvr" } else { "$cvrBase$cvr&locale=da" }
            $lookups.Add([pscustomobject]$lookup)
            $record = $lookups[$lookups.Count - 1]
            if (-not $live) {
                if ($null -eq $capture) { continue }
                $record.lookup_at = $capture.lookup_at
                $record.outcome = $capture.outcome
                if ($capture.outcome -ne 'saved') { continue }
            }
            $rawFile = Join-Path $rawPath "$cvr.json"
            $inputFile = Join-Path $inputPath "$source/$cvr.json"
            if ($live) {
                try {
                    $response = Invoke-WebRequest -Uri $record.url -UseBasicParsing -TimeoutSec 45 -MaximumRedirection 0
                    if ($response.StatusCode -ne 200) { throw "HTTP $($response.StatusCode)" }
                    [System.IO.File]::WriteAllBytes($rawFile, $response.RawContentStream.ToArray())
                } catch {
                    $record.lookup_at = [datetimeoffset]::UtcNow.ToString('o')
                    $status = $_.Exception.Response.StatusCode
                    $record.outcome = if ($status -in 401, 403) { 'access_denied' } else { 'technical_error' }
                    $record.detail = $_.Exception.Message
                    if (Test-Path -LiteralPath $rawFile) { Remove-Item -LiteralPath $rawFile }
                    continue
                }
                $record.lookup_at = [datetimeoffset]::UtcNow.ToString('o')
                $inputFile = $rawFile
            }
            try {
                if ($source -eq 'labs') {
                    $rows = @(Read-Labs $inputFile $cvr)
                    if (-not $live) { Copy-Item -LiteralPath $inputFile -Destination $rawFile }
                    $record.sha256 = (Get-FileHash -LiteralPath $rawFile -Algorithm SHA256).Hash.ToLowerInvariant()
                    $record.raw_file = "raw/matriklen-labs/$cvr.json"
                    $record.rows = $rows.Count
                    $record.outcome = if ($rows.Count -eq 0) { 'no_result' } else { 'found' }
                    $relations.AddRange($rows)
                } else {
                    $result = Read-Cvr $inputFile $cvr
                    $record.sha256 = (Get-FileHash -LiteralPath $inputFile -Algorithm SHA256).Hash.ToLowerInvariant()
                    $record.active_units = $result.Active
                    $record.closed_units = $result.Closed
                    $record.outcome = 'found'
                    $companies.Add($result.Company)
                    $units.AddRange($result.Units)
                }
            } catch {
                $record.outcome = 'invalid_response'
                $record.detail = $_.Exception.Message
                if ($source -eq 'labs' -and (Test-Path -LiteralPath $rawFile)) {
                    Remove-Item -LiteralPath $rawFile
                }
            }
        }
    }
    Write-Table (Join-Path $stage 'relations.csv') $relations $relationFields
    Write-Table (Join-Path $stage 'companies.csv') $companies $companyFields
    Write-Table (Join-Path $stage 'production_units.csv') $units $unitFields
    Write-Table (Join-Path $stage 'lookups.csv') $lookups $lookupFields
    [System.IO.Directory]::Move($stage, $outputPath)
} finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}

$incomplete = @($lookups | Where-Object { $_.outcome -notin 'found', 'no_result' })
$repeatedUnits = @($units | Group-Object -Property p_number | Where-Object { $_.Count -gt 1 })
Write-Host "$($cvrs.Count) CVRs, $($relations.Count) Labs observations, $($companies.Count) companies, $($units.Count) P-enheder."
if ($incomplete.Count -gt 0) {
    Write-Warning "$($incomplete.Count) lookups are incomplete. See lookups.csv in $outputPath."
}
if ($repeatedUnits.Count -gt 0) {
    Write-Warning "P-numbers recorded under multiple CVRs: $($repeatedUnits.Name -join ', '). Check both sources."
}
if ($incomplete.Count -gt 0 -or $repeatedUnits.Count -gt 0) {
    exit 2
}
