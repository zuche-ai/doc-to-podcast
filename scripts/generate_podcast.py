#!/usr/bin/env python3
"""
Podcast Generation Script

This script converts a JSON podcast script into an engaging audio podcast
with distinct Latin American Spanish voices for different speakers.
"""

import json
import os
import sys
import argparse
from pathlib import Path
import requests
from pydub import AudioSegment
from pydub.playback import play
import time


class PodcastGenerator:
    def __init__(self, api_key=None):
        """
        Initialize the podcast generator.
        
        Args:
            api_key (str): API key for text-to-speech service (optional)
        """
        self.api_key = api_key
        self.voices = {
            "MIGUEL": {
                "name": "Miguel",
                "description": "Warm, engaging Latin American male voice with a natural conversational tone",
                "voice_id": "pNInz6obpgDQGcFmaJgB"  # Adam voice for Miguel
            },
            "SAM": {
                "name": "Sam", 
                "description": "Thoughtful, articulate Latin American male voice with depth and wisdom",
                "voice_id": "VR6AewLTigWG4xSOukaG"  # Arnold voice for Sam
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
    
    def text_to_speech(self, text, voice_id, output_path):
        """
        Convert text to speech using ElevenLabs API.
        
        Args:
            text (str): Text to convert to speech
            voice_id (str): Voice ID to use
            output_path (str): Path to save the audio file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.api_key:
            print("Warning: No API key provided. Using placeholder audio generation.")
            return self._generate_placeholder_audio(text, output_path)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating speech: {e}")
            return False
    
    def _generate_placeholder_audio(self, text, output_path):
        """
        Generate placeholder audio for testing without API key.
        
        Args:
            text (str): Text to convert
            output_path (str): Path to save audio
            
        Returns:
            bool: True if successful
        """
        # Create a simple beep sound as placeholder
        sample_rate = 44100
        duration = len(text.split()) * 0.3  # Rough estimate: 0.3 seconds per word
        
        # Generate a simple tone
        import numpy as np
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * 440 * t) * 0.3  # 440 Hz tone
        
        # Convert to 16-bit PCM
        audio_data = (tone * 32767).astype(np.int16)
        
        # Save as WAV
        import wave
        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        return True
    
    def add_pause(self, audio_segment, duration_ms=500):
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
            
            if self.text_to_speech(line, voice_info["voice_id"], temp_audio_path):
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
        description="Generate an engaging podcast from a JSON script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_podcast.py script.json -o podcast.mp3
  python generate_podcast.py script.json --api-key YOUR_KEY -o podcast.mp3
  python generate_podcast.py script.json --no-intro --no-outro -o podcast.mp3
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
        "--api-key",
        help="ElevenLabs API key for high-quality text-to-speech"
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
        generator = PodcastGenerator(api_key=args.api_key)
        
        success = generator.generate_podcast(
            script_path=args.script_file,
            output_path=args.output,
            add_intro=not args.no_intro,
            add_outro=not args.no_outro
        )
        
        if success:
            print(f"\nPodcast generated successfully!")
            print(f"Output: {args.output}")
            if not args.api_key:
                print("Note: Used placeholder audio. For high-quality speech, provide an ElevenLabs API key.")
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