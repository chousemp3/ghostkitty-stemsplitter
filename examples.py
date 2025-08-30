#!/usr/bin/env python3
"""
🐱‍👻 GhostKitty StemSplitter - Example Usage Script
Demonstrates various ways to use the stem splitter
"""

import os
import sys
from pathlib import Path

from ghostkitty import GhostKittyStemSplitter

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def example_basic_usage():
    """Example 1: Basic stem splitting"""
    print("📁 Example 1: Basic Usage")
    print("=" * 50)

    # Create splitter with default settings
    splitter = GhostKittyStemSplitter()

    # Example file (you'll need to provide your own)
    audio_file = Path("example_song.mp3")  # Replace with your audio file

    if audio_file.exists():
        # Split the audio
        success = splitter.split_audio(audio_file)
        if success:
            print("✅ Stems created successfully!")
        else:
            print("❌ Failed to process audio")
    else:
        print(f"⚠️  Audio file not found: {audio_file}")
        print(
            "   Please add an audio file named 'example_song.mp3' to test this example"
        )


def example_custom_settings():
    """Example 2: Custom model and device settings"""
    print("\n🤖 Example 2: Custom Settings")
    print("=" * 50)

    # Create splitter with high-quality model
    splitter = GhostKittyStemSplitter(
        model_name="htdemucs_ft",  # Higher quality model
        device="cpu",  # Force CPU usage
    )

    audio_file = Path("example_song.wav")
    output_dir = Path("custom_output")

    if audio_file.exists():
        success = splitter.split_audio(audio_file, output_dir)
        if success:
            print(f"✅ Custom processing complete! Check: {output_dir}")
    else:
        print(f"⚠️  Audio file not found: {audio_file}")


def example_batch_processing():
    """Example 3: Batch processing multiple files"""
    print("\n📁 Example 3: Batch Processing")
    print("=" * 50)

    # Create a directory with audio files
    music_dir = Path("sample_music")

    if music_dir.exists() and any(music_dir.iterdir()):
        splitter = GhostKittyStemSplitter()

        # Process all audio files in the directory
        success_count = splitter.batch_split(
            input_dir=music_dir, output_dir=Path("batch_output")
        )

        print(f"✅ Processed {success_count} files successfully!")
    else:
        print(f"⚠️  Music directory not found or empty: {music_dir}")
        print(
            "   Create a 'sample_music' folder with audio files to test batch processing"
        )


def example_programmatic_usage():
    """Example 4: Using the splitter programmatically"""
    print("\n💻 Example 4: Programmatic Usage")
    print("=" * 50)

    def process_audio_callback(input_file, success):
        """Callback function for processing results"""
        if success:
            print(f"✅ Successfully processed: {input_file.name}")
        else:
            print(f"❌ Failed to process: {input_file.name}")

    # Find audio files in current directory
    audio_files = []
    for pattern in ["*.mp3", "*.wav", "*.flac"]:
        audio_files.extend(Path(".").glob(pattern))

    if audio_files:
        splitter = GhostKittyStemSplitter()

        for audio_file in audio_files[:3]:  # Process first 3 files
            print(f"🎵 Processing: {audio_file.name}")
            success = splitter.split_audio(audio_file)
            process_audio_callback(audio_file, success)
    else:
        print("⚠️  No audio files found in current directory")


def create_sample_files():
    """Create sample directory structure for testing"""
    print("\n🛠️  Setting up sample files...")

    # Create sample directories
    sample_dir = Path("sample_music")
    sample_dir.mkdir(exist_ok=True)

    # Create a simple README in the sample directory
    readme_content = """
# Sample Music Directory

Add your audio files here to test batch processing:
- MP3 files
- WAV files
- FLAC files
- Any other supported formats

The batch processing example will process all audio files in this directory.
"""

    (sample_dir / "README.md").write_text(readme_content)

    print(f"✅ Created sample directory: {sample_dir}")
    print("   Add your audio files there to test batch processing!")


def main():
    """Run all examples"""
    print("🐱‍👻 GhostKitty StemSplitter - Examples")
    print("=" * 60)

    # Create sample directory structure
    create_sample_files()

    # Run examples
    example_basic_usage()
    example_custom_settings()
    example_batch_processing()
    example_programmatic_usage()

    print("\n🎉 Examples complete!")
    print("\n💡 Tips:")
    print("   • Add audio files to test the examples")
    print("   • Use 'htdemucs_ft' model for best quality")
    print("   • Enable GPU (cuda/mps) for faster processing")
    print("   • Check output directories for separated stems")


if __name__ == "__main__":
    main()
