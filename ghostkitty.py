#!/usr/bin/env python3
"""
🐱‍👻 GhostKitty StemSplitter 🐱‍👻
A powerful audio stem separation tool for remixers and producers!

Splits audio files into 4 stems:
- 🎤 Vocals
- 🥁 Drums
- 🎸 Bass
- 🎵 Other (instruments)

Supports: MP3, WAV, FLAC, M4A, and more!
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Tuple

import click

# Audio processing libraries
import librosa
import numpy as np
import soundfile as sf
import torch
import torchaudio
from colorama import Fore, Style, init
from demucs.apply import apply_model
from demucs.pretrained import get_model

# UI and progress libraries
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

# Initialize colorama for cross-platform colored output
init()


class GhostKittyStemSplitter:
    """
    🐱‍👻 The main GhostKitty StemSplitter class
    """

    def __init__(self, model_name: str = "htdemucs", device: Optional[str] = None):
        """
        Initialize the GhostKitty StemSplitter

        Args:
            model_name: The Demucs model to use ('htdemucs', 'htdemucs_ft', 'mdx_extra', etc.)
            device: Device to run on ('cpu', 'cuda', 'mps'). Auto-detected if None.
        """
        self.console = Console()
        self.model_name = model_name
        self.device = device or self._detect_device()
        self.model = None
        self.supported_formats = {
            ".mp3",
            ".wav",
            ".flac",
            ".m4a",
            ".aac",
            ".ogg",
            ".wma",
        }

        # Stem names mapping
        self.stem_names = {0: "drums", 1: "bass", 2: "other", 3: "vocals"}

        self._setup_logging()
        self._print_banner()

    def _detect_device(self) -> str:
        """Auto-detect the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("ghostkitty.log"), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def _print_banner(self):
        """Print the cool GhostKitty banner"""
        banner = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                    🐱‍👻 GHOSTKITTY STEMSPLITTER 🐱‍👻                ║
        ║                                                               ║
        ║              ∩───∩                                            ║
        ║             ( ͡° ͜ʖ ͡°)   Splits your tracks like magic!       ║
        ║            /             Split into 4 stems instantly        ║
        ║           (  @  @  )      • Vocals  • Drums  • Bass  • Other ║
        ║            )     (                                            ║
        ║           (_____)         Supports: MP3, WAV, FLAC & more!   ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """

        self.console.print(
            Panel(
                Text(banner, style="bold cyan"),
                title="🎵 Audio Stem Separation Tool 🎵",
                border_style="bright_magenta",
            )
        )

        device_info = f"🖥️  Device: {self.device.upper()}"
        model_info = f"🤖 Model: {self.model_name}"

        self.console.print(f"\n{device_info} | {model_info}\n", style="bold green")

    def load_model(self):
        """Load the Demucs model"""
        if self.model is None:
            with self.console.status(
                "[bold green]Loading AI model... 🤖", spinner="dots"
            ):
                try:
                    self.model = get_model(self.model_name)
                    self.model.to(self.device)
                    self.model.eval()
                    self.console.print(
                        "✅ Model loaded successfully!", style="bold green"
                    )
                except Exception as e:
                    self.console.print(f"❌ Error loading model: {e}", style="bold red")
                    raise

    def is_supported_format(self, file_path: Path) -> bool:
        """Check if file format is supported"""
        return file_path.suffix.lower() in self.supported_formats

    def load_audio(self, file_path: Path) -> Tuple[torch.Tensor, int]:
        """
        Load audio file and return tensor and sample rate

        Args:
            file_path: Path to audio file

        Returns:
            Tuple of (audio_tensor, sample_rate)
        """
        try:
            # Load audio using torchaudio (handles most formats)
            waveform, sample_rate = torchaudio.load(str(file_path))

            # Convert to float32 and ensure 2 channels
            waveform = waveform.float()
            if waveform.shape[0] == 1:
                waveform = waveform.repeat(2, 1)  # Convert mono to stereo
            elif waveform.shape[0] > 2:
                waveform = waveform[:2]  # Take first 2 channels

            return waveform, sample_rate

        except Exception as e:
            # Fallback to librosa
            self.logger.warning(f"torchaudio failed, trying librosa: {e}")
            try:
                audio, sr = librosa.load(str(file_path), sr=None, mono=False)
                if audio.ndim == 1:
                    audio = np.stack([audio, audio])  # Convert mono to stereo
                waveform = torch.from_numpy(audio).float()
                return waveform, sr
            except Exception as e2:
                raise Exception(
                    f"Failed to load audio with both torchaudio and librosa: {e2}"
                )

    def save_stems(
        self,
        stems: torch.Tensor,
        sample_rate: int,
        output_dir: Path,
        filename_base: str,
    ):
        """
        Save the separated stems to files

        Args:
            stems: Tensor containing the separated stems [4, 2, length]
            sample_rate: Sample rate of audio
            output_dir: Directory to save stems
            filename_base: Base filename without extension
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save each stem
        for i, stem_name in self.stem_names.items():
            stem_audio = stems[i].cpu().numpy()
            output_file = output_dir / f"{filename_base}_{stem_name}.wav"

            try:
                sf.write(str(output_file), stem_audio.T, sample_rate, subtype="PCM_24")
                self.console.print(f"💾 Saved: {stem_name}.wav", style="green")
            except Exception as e:
                self.console.print(f"❌ Error saving {stem_name}: {e}", style="red")

    def split_audio(self, input_path: Path, output_dir: Optional[Path] = None) -> bool:
        """
        Split audio file into stems

        Args:
            input_path: Path to input audio file
            output_dir: Output directory (defaults to input file directory)

        Returns:
            True if successful, False otherwise
        """
        if not self.is_supported_format(input_path):
            self.console.print(
                f"❌ Unsupported format: {input_path.suffix}", style="bold red"
            )
            return False

        if not input_path.exists():
            self.console.print(f"❌ File not found: {input_path}", style="bold red")
            return False

        # Set output directory
        if output_dir is None:
            output_dir = input_path.parent / f"{input_path.stem}_stems"

        filename_base = input_path.stem

        self.console.print(f"\n🎵 Processing: {input_path.name}", style="bold cyan")

        try:
            # Load model if not already loaded
            if self.model is None:
                self.load_model()

            # Load audio
            with self.console.status(
                "[bold blue]Loading audio file... 📁", spinner="dots"
            ):
                waveform, sample_rate = self.load_audio(input_path)
                duration = waveform.shape[1] / sample_rate
                self.console.print(
                    f"📊 Duration: {duration:.2f}s | Sample Rate: {sample_rate}Hz",
                    style="blue",
                )

            # Process with model
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console,
            ) as progress:

                task = progress.add_task(
                    "🐱‍👻 Separating stems with AI magic...", total=100
                )

                # Move audio to device and add batch dimension
                waveform = waveform.to(self.device).unsqueeze(0)

                # Apply the model
                with torch.no_grad():
                    stems = apply_model(
                        self.model, waveform, device=self.device, progress=True
                    )[
                        0
                    ]  # Remove batch dimension

                progress.update(task, completed=100)

            # Save stems
            self.console.print("\n💾 Saving stems...", style="bold yellow")
            self.save_stems(stems, sample_rate, output_dir, filename_base)

            # Success message
            self.console.print(
                f"\n🎉 Success! Stems saved to: {output_dir}", style="bold green"
            )
            self.console.print("🎵 Ready for remixing! 🎧", style="bold magenta")

            return True

        except Exception as e:
            self.console.print(
                f"\n❌ Error processing {input_path.name}: {e}", style="bold red"
            )
            self.logger.error(f"Error processing {input_path}: {e}")
            return False

    def batch_split(self, input_dir: Path, output_dir: Optional[Path] = None) -> int:
        """
        Split multiple audio files in a directory

        Args:
            input_dir: Directory containing audio files
            output_dir: Output directory (defaults to input_dir/stems)

        Returns:
            Number of successfully processed files
        """
        if not input_dir.exists():
            self.console.print(f"❌ Directory not found: {input_dir}", style="bold red")
            return 0

        # Find audio files
        audio_files = []
        for ext in self.supported_formats:
            audio_files.extend(input_dir.glob(f"*{ext}"))
            audio_files.extend(input_dir.glob(f"*{ext.upper()}"))

        if not audio_files:
            self.console.print("❌ No supported audio files found!", style="bold red")
            return 0

        self.console.print(
            f"🔍 Found {len(audio_files)} audio files", style="bold blue"
        )

        if output_dir is None:
            output_dir = input_dir / "stems"

        success_count = 0

        for i, audio_file in enumerate(audio_files, 1):
            self.console.print(
                f"\n📁 [{i}/{len(audio_files)}] Processing batch...", style="bold cyan"
            )

            file_output_dir = output_dir / audio_file.stem
            if self.split_audio(audio_file, file_output_dir):
                success_count += 1

        self.console.print(
            f"\n🎯 Batch complete! {success_count}/{len(audio_files)} files processed successfully.",
            style="bold green",
        )

        return success_count


def create_cli():
    """Create the command-line interface"""

    @click.command()
    @click.argument("input_path", type=click.Path(exists=True, path_type=Path))
    @click.option(
        "--output", "-o", type=click.Path(path_type=Path), help="Output directory"
    )
    @click.option(
        "--model",
        "-m",
        default="htdemucs",
        help="Demucs model to use (htdemucs, htdemucs_ft, mdx_extra)",
    )
    @click.option("--device", "-d", help="Device to use (cpu, cuda, mps)")
    @click.option(
        "--batch", "-b", is_flag=True, help="Process all audio files in directory"
    )
    def cli(
        input_path: Path,
        output: Optional[Path],
        model: str,
        device: Optional[str],
        batch: bool,
    ):
        """
        🐱‍👻 GhostKitty StemSplitter - Split audio into 4 stems for remixing!

        INPUT_PATH: Audio file or directory to process
        """

        try:
            # Initialize splitter
            splitter = GhostKittyStemSplitter(model_name=model, device=device)

            if batch or input_path.is_dir():
                # Batch processing
                splitter.batch_split(input_path, output)
            else:
                # Single file processing
                splitter.split_audio(input_path, output)

        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}👋 Goodbye! Thanks for using GhostKitty StemSplitter!{Style.RESET_ALL}"
            )
        except Exception as e:
            print(f"\n{Fore.RED}💥 Fatal error: {e}{Style.RESET_ALL}")
            sys.exit(1)

    return cli


if __name__ == "__main__":
    # Create and run CLI
    cli = create_cli()
    cli()
