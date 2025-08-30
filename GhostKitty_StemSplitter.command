#!/bin/bash
# 🐱‍👻 GhostKitty StemSplitter - Double-click to launch!

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the project directory
cd "$DIR"

# Activate virtual environment and launch GUI
echo "🐱‍👻 Starting GhostKitty StemSplitter..."
source .venv/bin/activate
python ghostkitty_stemsplitter.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo "Press any key to exit..."
    read -n 1
fi
