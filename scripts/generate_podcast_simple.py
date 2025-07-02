#!/usr/bin/env python3
"""
Simple Podcast Generation Script using Google Text-to-Speech

This script converts a JSON podcast script into individual audio files
with distinct Latin American Spanish voices for different speakers.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from gtts import gTTS
import time


class SimplePodcastGenerator:
    def __init__(self):
        """Initialize the podcast generator."""
        self.voices = {
            "MIGUEL": {
                "name": "Miguel",
                "description": "Warm, engaging Latin American male voice",
                "lang": "es",
                "tld": "com.mx"  # Mexican Spanish for Miguel
            },
            "SAM": {
                "name": "Sam", 
                "description": "Thoughtful, articulate Latin American male voice",
                "lang": "es",
                "tld": "com.ar"  # Argentine Spanish for Sam (different accent)
            }
        }
        
    def load_script(self, script_path):
        """
        Load the podcast script from JSON file.
        
        Args:
            script_path (str): Path to the JSON script file
            
        Returns:
            list: List of dialogue entries
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script = json.load(f)
            return script
        except FileNotFoundError:
            raise FileNotFoundError(f"Script file not found: {script_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in script file: {script_path}")
    
    def text_to_speech(self, text, voice_info, output_path):
        """
        Convert text to speech using Google Text-to-Speech.
        
        Args:
            text (str): Text to convert to speech
            voice_info (dict): Voice configuration
            output_path (str): Path to save the audio file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"  Generating speech for {voice_info['name']}...")
            
            # Create gTTS object with specific language and TLD for accent variation
            tts = gTTS(text=text, lang=voice_info["lang"], tld=voice_info["tld"], slow=False)
            
            # Generate speech
            tts.save(output_path)
            
            print(f"  ✓ Saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"  ✗ Error generating speech: {e}")
            return False
    
    def generate_podcast_segments(self, script_path, output_dir="podcast_segments"):
        """
        Generate individual audio segments for each dialogue entry.
        
        Args:
            script_path (str): Path to the JSON script file
            output_dir (str): Directory to save audio segments
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("Loading podcast script...")
        script = self.load_script(script_path)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Generating podcast segments in: {output_dir}")
        print("=" * 50)
        
        # Process each dialogue segment
        for i, entry in enumerate(script):
            speaker = entry["speaker"]
            line = entry["line"]
            
            if speaker not in self.voices:
                print(f"Warning: Unknown speaker '{speaker}', skipping...")
                continue
            
            voice_info = self.voices[speaker]
            print(f"\nSegment {i+1}/{len(script)} - {voice_info['name']}:")
            print(f"  Text: {line[:80]}{'...' if len(line) > 80 else ''}")
            
            # Generate audio file
            output_path = os.path.join(output_dir, f"{i+1:03d}_{speaker}_{voice_info['name']}.mp3")
            
            if not self.text_to_speech(line, voice_info, output_path):
                print(f"Failed to generate audio for {speaker}")
                return False
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print("Podcast generation completed successfully!")
        print(f"All segments saved in: {output_dir}")
        print("\nTo combine the segments into a single podcast, you can:")
        print("1. Use audio editing software like Audacity")
        print("2. Use command line tools like ffmpeg")
        print("3. Use online audio merging tools")
        
        return True


def main():
    """Main function to handle command line arguments and run podcast generation."""
    parser = argparse.ArgumentParser(
        description="Generate podcast segments from a JSON script using Google TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_podcast_simple.py script.json
  python generate_podcast_simple.py script.json -o my_podcast_segments
        """
    )
    
    parser.add_argument(
        "script_file",
        help="Path to the JSON podcast script file"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="podcast_segments",
        help="Output directory for audio segments (default: podcast_segments)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        generator = SimplePodcastGenerator()
        
        success = generator.generate_podcast_segments(
            script_path=args.script_file,
            output_dir=args.output_dir
        )
        
        if success:
            print(f"\n✓ Podcast segments generated successfully!")
            print(f"Output directory: {args.output_dir}")
            print("Note: Using Google Text-to-Speech with Latin American Spanish accents.")
        else:
            print("Failed to generate podcast segments.", file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during podcast generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 