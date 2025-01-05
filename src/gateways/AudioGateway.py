import pyaudio
import logging
import numpy as np
import tempfile
from pydub import AudioSegment

LOGGER = logging.getLogger(__name__)


class AudioGateway:

    @staticmethod
    def get_audio_devices() -> dict:
        audio = pyaudio.PyAudio()
        devices = {}
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            device_info = {
                "ID": info["index"],
                "Name": info["name"],
                "Input Channels": info["maxInputChannels"],
                "Output Channels": info["maxOutputChannels"],
            }
            devices[info["index"]] = device_info
        return devices

    @staticmethod
    def get_input_devices():
        devices = AudioGateway.get_audio_devices()
        temp = {
            device["ID"]: device
            for device in devices.values()
            if device["Input Channels"] > 0
        }
        return temp

    @staticmethod
    def get_ouput_devices():
        devices = AudioGateway.get_audio_devices()
        return {
            device["ID"]: device
            for device in devices.values()
            if device["Output Channels"] > 0
        }

    def _is_silent(self, data, threshold=100):
        if len(data) == 0:
            return True
        # Convert raw audio chunk to NumPy array (assuming 16-bit audio)
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Check the maximum amplitude in the chunk
        max_amplitude = np.max(np.abs(audio_data))
        return max_amplitude < threshold

    def _listen_audio(self, input_stream, chunk_size):
        count = 0
        buffer = []
        while True:
            input_data = input_stream.read(chunk_size)
            if self._is_silent(input_data):
                if count > 100:  # how many chunks
                    LOGGER.info("Voice silent more than 100 times, stop listening")
                    break
                else:
                    count += 1
            else:
                buffer.append(input_data)

        return b"".join(buffer)

    def is_mp3_silent(self, file_path, threshold=100):
        audio_segment = AudioSegment.from_mp3(file_path)
        audio_data = np.array(audio_segment.get_array_of_samples())
        duration_in_seconds = len(audio_segment) / 1000.0
        if duration_in_seconds < 1:
            return True
        max_amplitude = np.max(np.abs(audio_data))        
        return max_amplitude < threshold

    def capture_until_silence(self, input_device, format, channels, rate, chunk):
        input_device_id = input_device.get("ID")
        input_device_name = input_device.get("Name")
        LOGGER.info(f"Starting audio component..{input_device_name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_name = temp_file.name
            audio_segment = AudioSegment.silent(duration=0)
            audio = pyaudio.PyAudio()
            input_stream = None
            try:
                input_stream = audio.open(
                    format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=input_device_id,
                )

                input_data = self._listen_audio(input_stream, chunk_size=chunk)
                if self._is_silent(input_data):
                    LOGGER.info("Voice returned but silent")
                    return None

                chunk_segment = AudioSegment(
                    data=input_data,
                    sample_width=audio.get_sample_size(format),
                    frame_rate=rate,
                    channels=channels,
                )
                audio_segment += chunk_segment
                # Save the complete audio segment to an MP3 file
                audio_segment.export(temp_file, format="mp3")
                LOGGER.info(f"Audio saved to {temp_file_name}")
                if self.is_mp3_silent(temp_file_name):
                    LOGGER.info("Audio is silent")
                    return None
                return temp_file_name
            except Exception as ex:
                LOGGER.exception(ex)
            finally:
                if input_stream:
                    input_stream.close()
