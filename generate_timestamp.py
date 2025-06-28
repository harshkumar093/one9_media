import os
import tempfile
from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel

def generate_timestamps_from_audio(video_path, model_size, device, compute_type):
    print('Generating timestamps from audio...')
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None
    print("Extracting audio from video...")
    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(temp_audio_file, codec="pcm_s16le")
        video.close()
        print("Transcribing audio with timestamps...")
        print(f"Using Whisper model: {model_size} on device: {device}")        
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, info = model.transcribe(temp_audio_file, word_timestamps=True)
        all_words = []
        for segment in segments:
            if segment.words:
                for word in segment.words:
                    all_words.append({'text': word.word, 'start': word.start, 'end': word.end})
        print(f"Transcription complete. Detected language: {info.language}")
    except Exception as e:
        print(f"Error during audio extraction or transcription: {e}")
        return None
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
    return all_words