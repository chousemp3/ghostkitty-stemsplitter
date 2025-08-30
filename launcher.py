#!/usr/bin/env python3
"""
🐱‍👻 GhostKitty StemSplitter - Main Launcher
Simple launcher for the GhostKitty StemSplitter GUI
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the GhostKitty StemSplitter GUI"""

    print("🐱‍👻 GhostKitty StemSplitter")
    print("=" * 40)
    print("Launching GUI application...")

    # Get the path to the virtual environment Python
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"

    # Path to the GUI application
    gui_app = Path(__file__).parent / "ghostkitty_stemsplitter.py"

    try:
        # Launch the GUI
        subprocess.run([str(venv_python), str(gui_app)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
