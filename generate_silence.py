from pydub import AudioSegment
import imageio_ffmpeg
import os

# Set pydub's ffmpeg path to bundled version
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

def generate_silence_mp3(seconds=5, filename="silence.mp3"):
    # Generate silent audio
    silence = AudioSegment.silent(duration=seconds * 1000)  # milliseconds

    # Export to MP3
    silence.export(filename, format="mp3")
    print(f"✅ Silent MP3 created: {filename} ({seconds} seconds)")