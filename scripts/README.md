# Audio Transcription Scripts

This folder contains scripts for audio processing and transcription.

## Audio Transcription with Whisper

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Usage

```bash
python transcribe_audio.py audio.mp3
```

For more options:
```bash
python transcribe_audio.py --help
```

### Examples

```bash
# Basic transcription
python transcribe_audio.py audio.mp3

# High-quality transcription
python transcribe_audio.py audio.mp3 -m large -o output.txt

# Quick transcription
python transcribe_audio.py audio.mp3 -m tiny -v
``` 