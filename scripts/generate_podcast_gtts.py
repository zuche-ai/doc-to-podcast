#!/usr/bin/env python3
"""
Podcast Generation Script using Google Text-to-Speech

This script converts a JSON podcast script into an engaging audio podcast
with distinct Latin American Spanish voices for different speakers using gTTS.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
import time


class PodcastGenerator:
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
            # Create gTTS object with specific language and TLD for accent variation
            tts = gTTS(text=text, lang=voice_info["lang"], tld=voice_info["tld"], slow=False)
            
            # Generate speech
            tts.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return False
    
    def add_pause(self, audio_segment, duration_ms=800):
        """
        Add a pause between dialogue segments.
        
        Args:
            audio_segment (AudioSegment): Audio to add pause to
            duration_ms (int): Duration of pause in milliseconds
            
        Returns:
            AudioSegment: Audio with pause added
        """
        silence = AudioSegment.silent(duration=duration_ms)
        return audio_segment + silence
    
    def generate_podcast(self, script_path, output_path, add_intro=True, add_outro=True):
        """
        Generate the complete podcast from the script.
        
        Args:
            script_path (str): Path to the JSON script file
            output_path (str): Path to save the final podcast
            add_intro (bool): Whether to add podcast intro music
            add_outro (bool): Whether to add podcast outro music
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("Loading podcast script...")
        script = self.load_script(script_path)
        
        print("Generating podcast audio...")
        podcast_audio = AudioSegment.empty()
        
        # Add intro music if requested
        if add_intro:
            print("Adding intro music...")
            intro_duration = 3000  # 3 seconds
            intro = AudioSegment.silent(duration=intro_duration)
            podcast_audio += intro
        
        # Process each dialogue segment
        for i, entry in enumerate(script):
            speaker = entry["speaker"]
            line = entry["line"]
            
            if speaker not in self.voices:
                print(f"Warning: Unknown speaker '{speaker}', skipping...")
                continue
            
            voice_info = self.voices[speaker]
            print(f"Generating audio for {voice_info['name']}: {line[:50]}...")
            
            # Generate temporary audio file
            temp_audio_path = f"temp_{speaker}_{i}.mp3"
            
            if self.text_to_speech(line, voice_info, temp_audio_path):
                # Load and add to podcast
                segment_audio = AudioSegment.from_mp3(temp_audio_path)
                podcast_audio += segment_audio
                
                # Add pause between speakers
                if i < len(script) - 1:
                    podcast_audio = self.add_pause(podcast_audio, 800)
                
                # Clean up temporary file
                os.remove(temp_audio_path)
            else:
                print(f"Failed to generate audio for {speaker}")
                return False
        
        # Add outro music if requested
        if add_outro:
            print("Adding outro music...")
            outro_duration = 2000  # 2 seconds
            outro = AudioSegment.silent(duration=outro_duration)
            podcast_audio += outro
        
        # Export final podcast
        print(f"Exporting podcast to: {output_path}")
        podcast_audio.export(output_path, format="mp3", bitrate="192k")
        
        print("Podcast generation completed successfully!")
        return True


def main():
    """Main function to handle command line arguments and run podcast generation."""
    parser = argparse.ArgumentParser(
        description="Generate an engaging podcast from a JSON script using Google TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_podcast_gtts.py script.json -o podcast.mp3
  python generate_podcast_gtts.py script.json --no-intro --no-outro -o podcast.mp3
        """
    )
    
    parser.add_argument(
        "script_file",
        help="Path to the JSON podcast script file"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="podcast.mp3",
        help="Output audio file path (default: podcast.mp3)"
    )
    
    parser.add_argument(
        "--no-intro",
        action="store_true",
        help="Skip intro music"
    )
    
    parser.add_argument(
        "--no-outro", 
        action="store_true",
        help="Skip outro music"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        generator = PodcastGenerator()
        
        success = generator.generate_podcast(
            script_path=args.script_file,
            output_path=args.output,
            add_intro=not args.no_intro,
            add_outro=not args.no_outro
        )
        
        if success:
            print(f"\nPodcast generated successfully!")
            print(f"Output: {args.output}")
            print("Note: Using Google Text-to-Speech with Latin American Spanish accents.")
        else:
            print("Failed to generate podcast.", file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during podcast generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 