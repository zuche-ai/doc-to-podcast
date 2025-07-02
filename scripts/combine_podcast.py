#!/usr/bin/env python3
"""
Podcast Segment Combiner

This script combines individual podcast segments into a single audio file
with proper pauses between speakers for a natural conversation flow.
"""

import os
import sys
import argparse
import glob
from pathlib import Path


def combine_podcast_segments(segments_dir, output_file, pause_duration=1.0):
    """
    Combine podcast segments into a single audio file.
    
    Args:
        segments_dir (str): Directory containing the audio segments
        output_file (str): Path for the output combined podcast
        pause_duration (float): Duration of pause between segments in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get all MP3 files in the segments directory, sorted by name
        segment_files = sorted(glob.glob(os.path.join(segments_dir, "*.mp3")))
        
        if not segment_files:
            print(f"No MP3 files found in {segments_dir}")
            return False
        
        print(f"Found {len(segment_files)} audio segments")
        print("Combining segments into single podcast...")
        
        # Create the ffmpeg command to concatenate all files
        # First, create a file list for ffmpeg
        file_list_path = "temp_file_list.txt"
        
        with open(file_list_path, 'w') as f:
            for segment_file in segment_files:
                f.write(f"file '{os.path.abspath(segment_file)}'\n")
                # Add a pause after each segment (except the last one)
                if segment_file != segment_files[-1]:
                    # Create a silent audio segment for the pause
                    silence_file = f"temp_silence_{len(segment_files)}.mp3"
                    silence_cmd = f"ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t {pause_duration} -q:a 9 -acodec libmp3lame {silence_file} -y"
                    os.system(silence_cmd)
                    f.write(f"file '{os.path.abspath(silence_file)}'\n")
        
        # Use ffmpeg to concatenate all files
        ffmpeg_cmd = f"ffmpeg -f concat -safe 0 -i {file_list_path} -c copy {output_file} -y"
        
        print("Running ffmpeg to combine segments...")
        result = os.system(ffmpeg_cmd)
        
        # Clean up temporary files
        os.remove(file_list_path)
        for silence_file in glob.glob("temp_silence_*.mp3"):
            os.remove(silence_file)
        
        if result == 0:
            print(f"✓ Podcast successfully combined: {output_file}")
            return True
        else:
            print("✗ Error combining podcast segments")
            return False
            
    except Exception as e:
        print(f"Error combining segments: {e}")
        return False


def main():
    """Main function to handle command line arguments and run podcast combination."""
    parser = argparse.ArgumentParser(
        description="Combine podcast segments into a single audio file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine_podcast.py faith_podcast_segments -o faith_podcast.mp3
  python combine_podcast.py segments_dir -o podcast.mp3 --pause 1.5
        """
    )
    
    parser.add_argument(
        "segments_dir",
        help="Directory containing the audio segments"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="combined_podcast.mp3",
        help="Output audio file path (default: combined_podcast.mp3)"
    )
    
    parser.add_argument(
        "--pause",
        type=float,
        default=1.0,
        help="Duration of pause between segments in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        if not os.path.exists(args.segments_dir):
            print(f"Error: Segments directory not found: {args.segments_dir}")
            sys.exit(1)
        
        success = combine_podcast_segments(
            segments_dir=args.segments_dir,
            output_file=args.output,
            pause_duration=args.pause
        )
        
        if success:
            print(f"\n✓ Podcast combination completed successfully!")
            print(f"Output: {args.output}")
            print(f"Pause duration: {args.pause} seconds")
        else:
            print("Failed to combine podcast segments.", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error during podcast combination: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 