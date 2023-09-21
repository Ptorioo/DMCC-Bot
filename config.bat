@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    pause
    exit 1
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
pip install ffmpeg
pip install PyNaCl

touch CONFIG.json
(
  echo {
  echo     "owners": [],
  echo     "token": "",
  echo     "prefix": ""
  echo }
) > CONFIG.json

exit 0