param (
    [Parameter(Mandatory=$true)]
    [string]$Language
)

Write-Host "Scanning repository for $Language tests..." -ForegroundColor Cyan

$directories = Get-ChildItem -Path . -Recurse -Directory -Filter $Language

foreach ($dir in $directories) {
    Write-Host "`n========================================" -ForegroundColor DarkGray
    Write-Host "Running tests in $($dir.FullName)" -ForegroundColor Yellow
    Push-Location $dir.FullName
    
    switch ($Language) {
        "python"     { pytest }
        "typescript" { npm install; npm test }
        "go"         { go test -v ./... }
        "rust"       { cargo test }
        "java"       { mvn clean test }
        "csharp"     { dotnet test }
        "cpp"        { 

            g++ -std=c++17 test.cpp -o test_bin.exe
            if ($?) { .\test_bin.exe }
        }
    }
    
    Pop-Location
}
Write-Host "`nAll $Language tests completed!" -ForegroundColor Green
