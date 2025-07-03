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

### Option 1: Human-Sounding Voices (ElevenLabs) - RECOMMENDED

For the most natural, human-sounding voices with distinct personalities:

#### Setup ElevenLabs
```bash
python setup_elevenlabs.py
```

#### Generate Podcast Segments
```bash
python generate_podcast_elevenlabs.py script.json --api-key YOUR_KEY -o podcast_segments
```

### Option 2: Basic Voices (Google TTS)

For basic text-to-speech (more robotic but free):

```bash
python generate_podcast_simple.py script.json -o podcast_segments
```

### Combine Podcast Segments

Combine individual segments into a single podcast file:

```bash
python combine_podcast.py podcast_segments -o final_podcast.mp3
```

### Complete Workflow Example

#### With ElevenLabs (Human Voices)
```bash
# 1. Setup (one-time)
python setup_elevenlabs.py

# 2. Generate segments with human voices
python generate_podcast_elevenlabs.py podcast_script.json --api-key YOUR_KEY -o segments

# 3. Combine into final podcast
python combine_podcast.py segments -o podcast.mp3 --pause 0.8
```

#### With Google TTS (Basic Voices)
```bash
# 1. Generate segments from JSON script
python generate_podcast_simple.py podcast_script.json -o segments

# 2. Combine into final podcast
python combine_podcast.py segments -o podcast.mp3 --pause 0.8
```

### Voice Profiles

#### ElevenLabs (Human-Sounding)
- **Miguel (Host)**: Deep, manly, authoritative Latin American male voice
- **Sam (Guest)**: Higher-pitched, faster-talking, clear Latin American male voice

#### Google TTS (Basic)
- **Miguel (Host)**: Mexican Spanish accent (warm, engaging)
- **Sam (Guest)**: Argentine Spanish accent (thoughtful, articulate)

### Features

- **Multiple voice options** (ElevenLabs for human voices, Google TTS for basic)
- **Distinct personalities** for each speaker
- **Natural conversation flow** with appropriate pauses
- **High-quality audio output** in MP3 format
- **Easy setup and testing** with included tools 