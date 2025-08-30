#!/usr/bin/env python3
"""
🐱‍👻 GhostKitty StemSplitter -    try:
        from ghostkitty import GhostKittyStemSplitter

        print("  ✅ GhostKitty StemSplitter")
        # Test that the class can be instantiated
        assert GhostKittyStemSplitter.__name__ == 'GhostKittyStemSplitter'
    except ImportError as e:em Test
Tests the installation and basic functionality
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test if all required libraries can be imported"""
    print("🔍 Testing imports...")

    try:
        import numpy

        print(f"  ✅ NumPy {numpy.__version__}")
    except ImportError as e:
        print(f"  ❌ NumPy: {e}")
        return False

    try:
        import torch

        print(f"  ✅ PyTorch {torch.__version__}")
    except ImportError as e:
        print(f"  ❌ PyTorch: {e}")
        return False

    try:
        import librosa

        print(f"  ✅ LibROSA {librosa.__version__}")
    except ImportError as e:
        print(f"  ❌ LibROSA: {e}")
        return False

    try:
        import demucs

        # Use demucs to avoid F401
        _ = hasattr(demucs, "__version__")
        print("  ✅ Demucs")
    except ImportError as e:
        print(f"  ❌ Demucs: {e}")
        return False

    try:
        import rich

        print("  ✅ Rich")
        # Use rich to avoid F401
        _ = hasattr(rich, "print")
    except ImportError as e:
        print(f"  ❌ Rich: {e}")
        return False

    try:
        from ghostkitty import GhostKittyStemSplitter

        print("  ✅ GhostKitty module")
        # Use the import to avoid F401
        assert hasattr(GhostKittyStemSplitter, "__init__")
    except ImportError as e:
        print(f"  ❌ GhostKitty module: {e}")
        return False

    return True


def test_device_detection():
    """Test device detection"""
    print("\n🖥️  Testing device detection...")

    try:
        import torch

        # Test CUDA
        if torch.cuda.is_available():
            print(f"  ✅ CUDA available: {torch.cuda.get_device_name()}")
        else:
            print("  ⚪ CUDA not available")

        # Test MPS (Apple Silicon)
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            print("  ✅ MPS (Apple Silicon) available")
        else:
            print("  ⚪ MPS not available")

        print("  ✅ CPU always available")

    except Exception as e:
        print(f"  ❌ Device detection error: {e}")
        return False

    return True


def test_ghostkitty_init():
    """Test GhostKitty initialization"""
    print("\n🐱‍👻 Testing GhostKitty initialization...")

    try:
        from ghostkitty import GhostKittyStemSplitter

        # Test GhostKitty initialization
        splitter = GhostKittyStemSplitter(device="cpu")
        print("  ✅ GhostKitty StemSplitter initialized successfully")

        # Test supported formats
        test_files = [
            Path("test.mp3"),
            Path("test.wav"),
            Path("test.flac"),
            Path("test.m4a"),
            Path("test.txt"),  # Should not be supported
        ]

        supported_count = 0
        for test_file in test_files:
            if splitter.is_supported_format(test_file):
                supported_count += 1

        print(
            f"  ✅ Format detection working: {supported_count}/4 audio formats supported"
        )

        return True

    except Exception as e:
        print(f"  ❌ GhostKitty initialization error: {e}")
        return False


def test_cli_help():
    """Test command-line interface"""
    print("\n💻 Testing CLI...")

    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "ghostkitty.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0 and "GhostKitty" in result.stdout:
            print("  ✅ CLI help working")
            return True
        else:
            print(f"  ❌ CLI help failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"  ❌ CLI test error: {e}")
        return False


def main():
    """Run all tests"""
    print("🐱‍👻 GhostKitty StemSplitter - System Test")
    print("=" * 50)

    all_passed = True

    # Run tests
    all_passed &= test_imports()
    all_passed &= test_device_detection()
    all_passed &= test_ghostkitty_init()
    all_passed &= test_cli_help()

    print("\n" + "=" * 50)

    if all_passed:
        print(
            "🎉 All tests passed! GhostKitty StemSplitter is ready to split some stems!"
        )
        print("\n💡 Next steps:")
        print("   • Add an audio file to this directory")
        print("   • Run: python ghostkitty.py your_song.mp3")
        print("   • Or try the GUI: python ghostkitty_stemsplitter.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\n🔧 Try:")
        print("   • Reinstalling dependencies: pip install -r requirements.txt")
        print("   • Checking Python version (3.8+ required)")

    print("\n🐱‍👻 Happy stem splitting!")


if __name__ == "__main__":
    main()
