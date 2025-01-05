import sounddevice as sd
import numpy as np
import wave

import pyaudio
import wave
import pyaudio
import wave
import numpy as np


def pyaudiotest():
    # Audio settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    SILENCE_THRESHOLD = (
        500  # Adjust this value based on your microphone and environment
    )
    SILENCE_DURATION = 2  # Stop after 2 seconds of silence

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Recording... (Will stop after silence)")

    frames = []
    silence_counter = 0

    # Record audio
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert audio chunks to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Calculate RMS of the audio chunk
        rms = np.sqrt(np.mean(np.square(audio_data)))

        # Check if RMS is below the silence threshold
        if rms < SILENCE_THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0

        # Stop recording if silence duration is reached
        if silence_counter > SILENCE_DURATION * (RATE / CHUNK):
            break

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    WAVE_OUTPUT_FILENAME = "output.wav"
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    pyaudiotest()
