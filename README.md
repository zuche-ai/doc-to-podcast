# Audio Transcription with Whisper

A Python script that uses OpenAI's Whisper model to transcribe audio files and save the transcription to a text file.

## Features

- Transcribe audio files in various formats (MP3, WAV, M4A, etc.)
- Choose from different Whisper models (tiny, base, small, medium, large)
- Automatic output file naming
- Command-line interface with helpful options
- Error handling and validation

## Installation

1. Clone or download this repository
2. Navigate to the scripts directory and install the required dependencies:

```bash
cd scripts
pip install -r requirements.txt
```

## Usage

### Basic Usage

Transcribe an audio file with the default settings:

```bash
cd scripts
python transcribe_audio.py audio.mp3
```

This will create a text file with the same name as your audio file (e.g., `audio.txt`).

### Advanced Usage

Specify an output file:

```bash
cd scripts
python transcribe_audio.py audio.mp3 -o my_transcription.txt
```

Use a different Whisper model:

```bash
cd scripts
python transcribe_audio.py audio.mp3 -m large
```

Enable verbose output:

```bash
cd scripts
python transcribe_audio.py audio.mp3 -v
```

### Available Models

- `tiny`: Fastest, least accurate
- `base`: Good balance of speed and accuracy (default)
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

### Command Line Options

```
positional arguments:
  audio_file            Path to the audio file to transcribe

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output text file path (default: same name as audio file with .txt extension)
  -m {tiny,base,small,medium,large}, --model {tiny,base,small,medium,large}
                        Whisper model to use (default: base)
  -v, --verbose         Enable verbose output
```

## Examples

```bash
# Basic transcription
cd scripts
python transcribe_audio.py podcast.mp3

# High-quality transcription with custom output
cd scripts
python transcribe_audio.py interview.wav -m large -o interview_transcript.txt

# Quick transcription for short audio
cd scripts
python transcribe_audio.py voicemail.m4a -m tiny -v
```

## Supported Audio Formats

Whisper supports most common audio formats including:
- MP3
- WAV
- M4A
- FLAC
- OGG
- And many others

## Notes

- The first time you run the script, it will download the selected Whisper model (this may take a few minutes depending on your internet connection)
- Larger models provide better accuracy but take longer to process
- The script automatically handles different audio formats and sample rates
- Transcriptions are saved in UTF-8 encoding

## Requirements

- Python 3.7 or higher
- Internet connection (for downloading models)
- Sufficient disk space for model storage 