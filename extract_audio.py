import sys
import io
import os
from moviepy import VideoFileClip

# Force standard output to use utf-8 to avoid console cp950 encoding errors on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def extract_audio(video_path, output_path):
    print("Loading video...")
    try:
        video = VideoFileClip(video_path)
        print("Extracting audio...")
        video.audio.write_audiofile(output_path)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_audio.py <input_video> <output_audio>")
        sys.exit(1)
    extract_audio(sys.argv[1], sys.argv[2])
