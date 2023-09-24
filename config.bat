@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    pause
    exit 1
)

for /f "tokens=2" %%V in ('python --version 2^>^&1') do (
    set python_version=%%V
)

for /f "tokens=1,2 delims=." %%A in ("%python_version%") do (
    set major=%%A
    set minor=%%B
)

if %major% LSS 3 (
    echo Python version is less than 3.10.
    pause
    exit 1
) else if %major% EQU 3 (
    if %minor% LSS 10 (
        echo Python version is less than 3.10.
        pause
        exit 1
    )
)

python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    if %errorlevel% neq 0 (
        echo Pip installation failed.
        pause
        exit 1
    )
)
ffmpeg.exe -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg is not installed.
    pause
    exit 1
)

pip install discord
pip install yt-dlp
pip install youtube-search-python
pip install ffmpeg
pip install flask
pip install PyNaCl
pip install waitress

touch CONFIG.json
(
  echo {
  echo     "owners": [],
  echo     "token": "",
  echo     "prefix": ""
  echo }
) > CONFIG.json

exit 0