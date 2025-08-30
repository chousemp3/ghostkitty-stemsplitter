# GhostKitty StemSplitter

**AI-powered audio stem separation tool with a clean, dark interface**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange?style=flat-square&logo=pytorch)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20|%20Linux%20|%20Windows-lightgrey?style=flat-square)](https://github.com/chousemp3/ghostkitty-stemsplitter)

## Features

- **Audio stem separation** using Meta's Demucs models
- **Dark-themed GUI** with visual effects
- **Command-line interface** for batch processing
- **GPU acceleration** (CUDA, MPS, CPU)
- **Multiple audio formats** - MP3, WAV, FLAC, M4A, AAC, OGG
- **High-quality output** - 24-bit WAV files
- **Cross-platform** support  

Split any song into 4 stems:
- **Vocals** - Lead and backing vocals
- **Drums** - Drum kit and percussion
- **Bass** - Bass guitar and low-frequency elements
- **Other** - All remaining instruments

## Installation

```bash
git clone https://github.com/chousemp3/ghostkitty-stemsplitter.git
cd ghostkitty-stemsplitter
pip install -r requirements.txt
```

## Usage

### GUI Version
```bash
python ghostkitty_stemsplitter.py
```

### Command Line
```bash
# Single file
python ghostkitty.py song.mp3

# Batch processing
python ghostkitty.py music_folder/ --batch

# High-quality model with GPU
python ghostkitty.py song.wav -m htdemucs_ft -d cuda
```

## 🎯 Use Cases

| Use Case | Description |
|----------|-------------|
| 🎧 **Remixing** | Extract individual stems for creative remixes |
| 🎤 **Karaoke** | Remove vocals for sing-along tracks |
| 🎹 **Production** | Isolate instruments for sampling and analysis |
| 📚 **Education** | Study music arrangement and composition |
| 🔧 **Audio Repair** | Remove specific elements from recordings |

## 🛠️ Technical Details

### AI Models
- **htdemucs** (default) - Best balance of speed and quality
- **htdemucs_ft** - Fine-tuned for maximum quality  
- **mdx_extra** - Alternative separation algorithm

### Performance
- **GPU Acceleration** - 5-10x faster on CUDA/MPS
- **Memory Efficient** - Handles large files without issues
- **Batch Processing** - Process entire albums overnight

### Output Quality
- **24-bit WAV** - Professional studio quality
- **Original Sample Rate** - Preserves source quality
- **Stereo Separation** - Full stereo imaging maintained

## 📊 Supported Formats

| Input | Output |
|-------|--------|
| MP3, WAV, FLAC | 24-bit WAV |
| M4A, AAC, OGG | High-quality stems |
| Any sample rate | Original rate preserved |

## 🖥️ System Requirements

- **Python 3.8+**
- **4GB+ RAM** (8GB+ recommended)
- **GPU** (optional but recommended)
  - NVIDIA CUDA 11.0+
  - Apple Silicon (M1/M2)
- **Storage** - ~2GB for AI models

## 🎨 Screenshots

### Cyberpunk GUI
*Dark theme with animated visual effects and professional controls*

### Command Line Interface  
*Beautiful terminal output with progress bars and status updates*

## 🔧 Advanced Usage

### Batch Processing
```bash
# Process entire music library
python ghostkitty.py "/path/to/music/" --batch -o "/path/to/stems/"
```

### Quality vs Speed
```bash
# Maximum quality (slower)
python ghostkitty.py song.wav -m htdemucs_ft

# Balanced (default)
python ghostkitty.py song.wav -m htdemucs

# Alternative algorithm
python ghostkitty.py song.wav -m mdx_extra
```

### GPU Optimization
```bash
# Force CUDA
python ghostkitty.py song.wav -d cuda

# Apple Silicon
python ghostkitty.py song.wav -d mps

# CPU only
python ghostkitty.py song.wav -d cpu
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/chousemp3/ghostkitty-stemsplitter.git
cd ghostkitty-stemsplitter
pip install -r requirements.txt
python test_system.py  # Verify installation
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta Research** - For the incredible Demucs models
- **PyTorch Team** - For the deep learning framework
- **Music Community** - For inspiration and feedback

## 🐛 Issues & Support

Found a bug or need help? 
- 🐛 [Report Issues](https://github.com/chousemp3/ghostkitty-stemsplitter/issues)
- 💬 [Discussions](https://github.com/chousemp3/ghostkitty-stemsplitter/discussions)
- 📧 Contact: [your-email@domain.com]

## ⭐ Star History

If you find GhostKitty StemSplitter useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ and 🐱‍👻 magic**

[⭐ Star this repo](https://github.com/chousemp3/ghostkitty-stemsplitter) • [🐛 Report Bug](https://github.com/chousemp3/ghostkitty-stemsplitter/issues) • [💡 Request Feature](https://github.com/chousemp3/ghostkitty-stemsplitter/issues)

</div>
