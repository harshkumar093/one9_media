import wave
import struct

def generate_silence_wav(seconds=5, filename="silence.wav", sample_rate=44100):
    num_samples = seconds * sample_rate
    amplitude = 0  # silence
    nchannels = 1
    sampwidth = 2  # bytes per sample
    framerate = sample_rate

    with wave.open(filename, 'w') as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        for _ in range(num_samples):
            wf.writeframes(struct.pack('<h', amplitude))

    print(f"✅ Created silent WAV file: {filename} ({seconds} seconds)")

generate_silence_wav(seconds=5, filename="silence.wav")