#!/usr/bin/env python3
"""
Combine Podcast Segments Script using ffmpeg (WAV version)

This script combines individual WAV audio segments into a single podcast file
using ffmpeg directly, specifically for Coqui TTS output.
"""

import os
import sys
import argparse
import glob
import subprocess
import tempfile


def combine_audio_segments(input_dir, output_file):
    """
    Combine audio segments into a single podcast file using ffmpeg.
    
    Args:
        input_dir (str): Directory containing audio segments
        output_file (str): Output file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get all WAV files in the directory, sorted by name
        audio_files = glob.glob(os.path.join(input_dir, "*.wav"))
        audio_files.sort()
        
        if not audio_files:
            print("No WAV files found in", input_dir)
            return False
        
        print(f"Found {len(audio_files)} audio segments")
        print("Combining segments...")
        
        # Create a temporary file with the list of audio files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            for audio_file in audio_files:
                f.write(f"file '{os.path.abspath(audio_file)}'\n")
            file_list_path = f.name
        
        try:
            # Use ffmpeg to concatenate the audio files
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', file_list_path,
                '-c:a', 'libmp3lame',
                '-b:a', '192k',
                output_file,
                '-y'  # Overwrite output file if it exists
            ]
            
            print("Running ffmpeg command...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Successfully created: {output_file}")
                
                # Get duration using ffprobe
                duration_cmd = [
                    'ffprobe',
                    '-v', 'quiet',
                    '-show_entries', 'format=duration',
                    '-of', 'csv=p=0',
                    output_file
                ]
                
                duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
                if duration_result.returncode == 0:
                    duration = float(duration_result.stdout.strip())
                    print(f"Total duration: {duration:.2f} seconds")
                
                return True
            else:
                print(f"Error running ffmpeg: {result.stderr}")
                return False
                
        finally:
            # Clean up temporary file
            os.unlink(file_list_path)
        
    except Exception as e:
        print(f"Error combining audio segments: {e}")
        return False


def check_ffmpeg():
    """Check if ffmpeg is available on the system."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main():
    """Main function to handle command line arguments and run audio combination."""
    parser = argparse.ArgumentParser(
        description="Combine WAV audio segments into a single podcast file using ffmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine_podcast_wav.py coqui_podcast_segments -o coqui_podcast.mp3
  python combine_podcast_wav.py podcast_segments -o final_podcast.mp3
        """
    )
    
    parser.add_argument(
        "input_dir",
        help="Directory containing WAV audio segments"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="combined_podcast.mp3",
        help="Output file path (default: combined_podcast.mp3)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Check if ffmpeg is available
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not available in PATH", file=sys.stderr)
        print("Please install ffmpeg: https://ffmpeg.org/download.html", file=sys.stderr)
        sys.exit(1)
    
    # Check if input directory exists
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Check if there are any WAV files
    audio_files = glob.glob(os.path.join(args.input_dir, "*.wav"))
    if not audio_files:
        print(f"No WAV files found in '{args.input_dir}'", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(audio_files)} WAV files in {args.input_dir}")
    
    # Combine the audio segments
    success = combine_audio_segments(args.input_dir, args.output)
    
    if success:
        print(f"\n✓ Podcast successfully combined!")
        print(f"Output file: {args.output}")
    else:
        print("Failed to combine podcast segments.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 