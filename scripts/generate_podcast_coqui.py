#!/usr/bin/env python3
"""
Coqui TTS Podcast Generation Script

This script converts a JSON podcast script into an engaging audio podcast
using Coqui TTS with high-quality, human-sounding voices.
Supports both default voices and voice cloning from audio samples.
"""

import json
import os
import sys
import argparse
from pathlib import Path
import torch
from TTS.api import TTS
import time


class CoquiPodcastGenerator:
    def __init__(self, use_gpu=False, use_voice_cloning=False):
        """
        Initialize the Coqui TTS podcast generator.
        
        Args:
            use_gpu (bool): Whether to use GPU acceleration if available
            use_voice_cloning (bool): Whether to use voice cloning (requires sample files)
        """
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.use_voice_cloning = use_voice_cloning
        print(f"Using device: {self.device}")
        
        # Initialize TTS with multilingual model
        print("Loading TTS model...")
        if use_voice_cloning:
            # Use XTTS v2 for voice cloning
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        else:
            # Use a simpler multilingual model for default voices
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1.1").to(self.device)
        
        # Voice configurations
        self.voices = {
            "MIGUEL": {
                "name": "Miguel",
                "description": "Deep, manly, authoritative Latin American male voice",
                "voice_file": "voice_samples/miguel_sample.wav",  # For voice cloning
                "language": "es",
                "speed": 0.9  # Slightly slower for authority
            },
            "SAM": {
                "name": "Sam", 
                "description": "Higher-pitched, faster-talking, clear Latin American male voice",
                "voice_file": "voice_samples/sam_sample.wav",  # For voice cloning
                "language": "es",
                "speed": 1.2  # Faster talking
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
    
    def create_default_voice_samples(self):
        """Create default voice samples for testing."""
        samples_dir = "voice_samples"
        os.makedirs(samples_dir, exist_ok=True)
        
        print("Creating default voice samples...")
        
        # Create sample audio files for each voice
        sample_texts = {
            "miguel_sample": "Hola, soy Miguel. Tengo una voz profunda y masculina para nuestro podcast.",
            "sam_sample": "¡Hola! Soy Sam. Hablo rápido y con energía, perfecto para conversaciones dinámicas."
        }
        
        for voice_name, text in sample_texts.items():
            sample_path = f"{samples_dir}/{voice_name}.wav"
            
            if not os.path.exists(sample_path):
                print(f"  Creating {voice_name} sample...")
                self.tts.tts_to_file(
                    text=text,
                    file_path=sample_path,
                    language="es"
                )
        
        print("✓ Default voice samples created")
    
    def text_to_speech(self, text, voice_info, output_path):
        """
        Convert text to speech using Coqui TTS.
        
        Args:
            text (str): Text to convert to speech
            voice_info (dict): Voice configuration
            output_path (str): Path to save the audio file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"  Generating speech for {voice_info['name']}...")
            
            if self.use_voice_cloning and os.path.exists(voice_info['voice_file']):
                # Use voice cloning
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=voice_info['voice_file'],
                    language=voice_info["language"],
                    speed=voice_info["speed"]
                )
            else:
                # Use default voice
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=voice_info["language"],
                    speed=voice_info["speed"]
                )
            
            print(f"  ✓ Saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"  ✗ Error generating speech: {e}")
            return False
    
    def generate_podcast_segments(self, script_path, output_dir="coqui_podcast_segments"):
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
        
        # Create voice samples if using voice cloning
        if self.use_voice_cloning:
            self.create_default_voice_samples()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Generating podcast segments in: {output_dir}")
        print("=" * 60)
        print("Voice Profiles:")
        print(f"  Miguel: {self.voices['MIGUEL']['description']}")
        print(f"  Sam: {self.voices['SAM']['description']}")
        print(f"  Voice Cloning: {'Enabled' if self.use_voice_cloning else 'Disabled'}")
        print("=" * 60)
        
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
            output_path = os.path.join(output_dir, f"{i+1:03d}_{speaker}_{voice_info['name']}.wav")
            
            if not self.text_to_speech(line, voice_info, output_path):
                print(f"Failed to generate audio for {speaker}")
                return False
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("Podcast generation completed successfully!")
        print(f"All segments saved in: {output_dir}")
        print("\nTo combine the segments into a single podcast, run:")
        print(f"python combine_podcast_ffmpeg.py {output_dir} -o coqui_podcast.mp3")
        print("\nNote: Using Coqui TTS for high-quality, human-sounding voices!")
        
        return True


def main():
    """Main function to handle command line arguments and run podcast generation."""
    parser = argparse.ArgumentParser(
        description="Generate podcast segments with Coqui TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_podcast_coqui.py script.json -o coqui_podcast_segments
  python generate_podcast_coqui.py script.json --voice-cloning --gpu
        """
    )
    
    parser.add_argument(
        "script_file",
        help="Path to the JSON podcast script file"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="coqui_podcast_segments",
        help="Output directory for audio segments (default: coqui_podcast_segments)"
    )
    
    parser.add_argument(
        "--voice-cloning",
        action="store_true",
        help="Enable voice cloning (requires voice sample files)"
    )
    
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use GPU acceleration if available"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        generator = CoquiPodcastGenerator(
            use_gpu=args.gpu,
            use_voice_cloning=args.voice_cloning
        )
        
        success = generator.generate_podcast_segments(
            script_path=args.script_file,
            output_dir=args.output_dir
        )
        
        if success:
            print(f"\n✓ Podcast segments generated successfully!")
            print(f"Output directory: {args.output_dir}")
            print("Note: Using Coqui TTS for high-quality, human-sounding voices!")
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