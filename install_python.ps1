$installer = "C:\Users\antik\.gemini\antigravity\scratch\python_installer.exe"
Write-Host "Downloading Python 3.12..."
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile $installer
Write-Host "Installing Python silently..."
Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0" -Wait
Write-Host "Python Installation complete."
Remove-Item $installer
