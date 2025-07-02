# Audio Processing Scripts

This folder contains scripts for audio processing, transcription, and podcast generation.

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

## Podcast Generation from JSON Scripts

### Generate Podcast Segments

Convert a JSON podcast script into individual audio segments with distinct voices:

```bash
python generate_podcast_simple.py script.json -o podcast_segments
```

### Combine Podcast Segments

Combine individual segments into a single podcast file:

```bash
python combine_podcast.py podcast_segments -o final_podcast.mp3
```

### Complete Workflow Example

```bash
# 1. Generate segments from JSON script
python generate_podcast_simple.py podcast_script.json -o segments

# 2. Combine into final podcast
python combine_podcast.py segments -o podcast.mp3 --pause 0.8
```

### Features

- **Distinct Latin American Spanish voices** for different speakers
- **Miguel (Host)**: Mexican Spanish accent (warm, engaging)
- **Sam (Guest)**: Argentine Spanish accent (thoughtful, articulate)
- **Natural conversation flow** with appropriate pauses
- **High-quality audio output** in MP3 format 