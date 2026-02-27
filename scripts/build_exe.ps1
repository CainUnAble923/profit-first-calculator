$ErrorActionPreference = "Stop"

Write-Host "Cleaning old builds..."
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Remove-Item *.spec -ErrorAction SilentlyContinue

Write-Host "Building Profit First Calculator..."

python -m PyInstaller `
    --noconsole `
    --onefile `
    --name "Profit First Calculator" `
    --icon assets/app.ico `
    src/main.py

Write-Host ""
Write-Host "Build Complete!"
Write-Host "Your EXE is located in: dist\Profit First Calculator.exe"