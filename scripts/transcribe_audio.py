#!/usr/bin/env python3
"""
Audio Transcription Script using OpenAI Whisper

This script transcribes audio files using the Whisper model and saves the
transcription to a text file.
"""

import argparse
import os
import sys
from pathlib import Path
import whisper


def transcribe_audio(audio_path, output_path=None, model_name="base"):
    """
    Transcribe an audio file using Whisper and save to text file.
    
    Args:
        audio_path (str): Path to the audio file
        output_path (str): Path for the output text file (optional)
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
    
    Returns:
        str: Path to the output text file
    """
    # Validate input file
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Set output path if not provided
    if output_path is None:
        audio_file = Path(audio_path)
        output_path = audio_file.with_suffix('.txt')
    
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)
    
    print(f"Transcribing audio file: {audio_path}")
    result = model.transcribe(audio_path)
    
    # Save transcription to text file
    transcription_text = result["text"]
    if isinstance(transcription_text, list):
        transcription_text = " ".join(transcription_text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcription_text)
    
    print(f"Transcription saved to: {output_path}")
    return output_path


def main():
    """Main function to handle command line arguments and run transcription."""
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe_audio.py audio.mp3
  python transcribe_audio.py audio.wav -o transcription.txt
  python transcribe_audio.py audio.m4a -m large
        """
    )
    
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to transcribe"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output text file path (default: same name as audio file with .txt extension)"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: base)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        output_file = transcribe_audio(
            audio_path=args.audio_file,
            output_path=args.output,
            model_name=args.model
        )
        
        if args.verbose:
            print(f"\nTranscription completed successfully!")
            print(f"Input: {args.audio_file}")
            print(f"Output: {output_file}")
            print(f"Model used: {args.model}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 