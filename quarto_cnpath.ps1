param(
    [ValidateSet('render','preview')]
    [string]$Mode = 'render',
    [string]$Chapter = 'chapters/01-introduction-hypotheses.qmd',
    [int]$Port = 4321
)

$ProjectPath = (Get-Location).Path
$LinkRoot = 'C:\qtmp'
$LinkPath = 'C:\qtmp\exP03'

if (!(Test-Path -LiteralPath $LinkRoot)) {
    New-Item -ItemType Directory -Path $LinkRoot | Out-Null
}

if (Test-Path -LiteralPath $LinkPath) {
    cmd /c rmdir $LinkPath | Out-Null
}

New-Item -ItemType Junction -Path $LinkPath -Target $ProjectPath | Out-Null

Push-Location $LinkPath
try {
    if ($Mode -eq 'render') {
        Write-Host "[INFO] Rendering via: $LinkPath"
        quarto render
    }
    else {
        Write-Host "[INFO] Preview via: $LinkPath/$Chapter"
        quarto preview "C:/qtmp/exP03/$Chapter" --no-browser --no-watch-inputs --port $Port
    }
}
finally {
    Pop-Location
}
