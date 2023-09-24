#!/bin/bash

if ! command -v python &> /dev/null; then
    echo "Python is not installed."
    read -p "Press Enter to continue..."
    exit 1
fi

installed_python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')

if [[ "$(python3 -c "import sys; print(sys.version_info >= (3, 10))")" != "True" ]]; then
    echo "Python version $installed_python_version is not compatible. Python $required_python_version or higher is required."
    read -p "Press Enter to continue..."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    if [ $? -ne 0 ]; then
        echo "Pip installation failed."
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed."
    read -p "Press Enter to continue..."
    exit 1
fi

pip install discord yt-dlp youtube-search-python ffmpeg flask PyNaCl waitress

echo '{
    "owners": [],
    "token": "",
    "prefix": ""
}' > CONFIG.json

exit 0