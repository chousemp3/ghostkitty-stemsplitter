#!/bin/bash
"""
🐱‍👻 GhostKitty StemSplitter - Quick Start Script
Run this to quickly test the stem splitter with a sample file
"""

echo "🐱‍👻 GhostKitty StemSplitter - Quick Start"
echo "=============================================="

# Check if Python virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating Python virtual environment..."
    source .venv/bin/activate
fi

# Check if we have any audio files to test with
AUDIO_FILES=(*.mp3 *.wav *.flac *.m4a)
FOUND_FILES=()

for file in "${AUDIO_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        FOUND_FILES+=("$file")
    fi
done

if [[ ${#FOUND_FILES[@]} -eq 0 ]]; then
    echo "⚠️  No audio files found in current directory"
    echo ""
    echo "To test GhostKitty, please:"
    echo "1. Add an audio file (MP3, WAV, FLAC, etc.) to this directory"
    echo "2. Run this script again"
    echo ""
    echo "Or use the commands directly:"
    echo "  python ghostkitty.py your_song.mp3"
    echo "  python ghostkitty_stemsplitter.py"
    echo ""
    exit 1
fi

echo "🎵 Found audio files:"
for file in "${FOUND_FILES[@]}"; do
    echo "   • $file"
done

echo ""
echo "🤖 Testing GhostKitty StemSplitter with: ${FOUND_FILES[0]}"

# Test the command-line version
echo ""
echo "🔄 Running stem separation..."
python ghostkitty.py "${FOUND_FILES[0]}"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "🎉 Success! Check the output directory for your stems:"
    echo "   • vocals.wav"
    echo "   • drums.wav"  
    echo "   • bass.wav"
    echo "   • other.wav"
    echo ""
    echo ""
    echo "💡 You can also try:"
    echo "   • python ghostkitty_stemsplitter.py (enhanced graphical interface)"
    echo "   • python examples.py (more examples)"
else
    echo "❌ Something went wrong. Check the error messages above."
fi
