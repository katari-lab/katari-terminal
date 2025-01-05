import pyaudio
from ..gateways.AudioGateway import AudioGateway
from ..gateways.TranscriptGateway import TranscriptGateway
from ..gateways.TermCacheGateway import TermCacheGateway
from ..gateways.OpenIAGateway import OpenAIGateway
from ..gateways.TerminalGateway import TerminalGateway
from pprint import pprint
import logging

LOGGER = logging.getLogger(__name__)


class TerminalComponent:
    def __init__(
        self,
        audio_format=pyaudio.paInt16,
        num_channels=1,
        sample_rate=44100,
        buffer_size=1024,
    ):
        self.audio_gateway = AudioGateway()
        self.transcript_gateway = TranscriptGateway()
        self.term_cache_gateway = TermCacheGateway()
        self.terminals_gateway = TerminalGateway()
        self.openai_gateway = OpenAIGateway()
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.audio_format = audio_format

    def capture_action(self, selected_device):
        audio_data = self.audio_gateway.capture_until_silence(
            selected_device,
            self.audio_format,
            self.num_channels,
            self.sample_rate,
            self.buffer_size,
        )
        if audio_data is None:
            LOGGER.info("No audio data captured, skipping transcription")
            return None, None
        LOGGER.info(f"Transcripting the audio {audio_data}")
        transcript = self.transcript_gateway.transcript(audio_data)
        LOGGER.info(f"Transcript: {transcript}")        
        command = self.term_cache_gateway.get_term(transcript)
        if not command:                       
            command = self.openai_gateway.transcription_to_action(transcript)
            self.term_cache_gateway.set_term(transcript, command)                        
        else:
            LOGGER.info(f"Response from cache: {command}")
        LOGGER.info(f"Response from run: {command}")            
        return transcript, command

    def run(self):
        input_devices = self.audio_gateway.get_input_devices()
        pprint(input_devices)
        input_device_id = int(input("Select the input device you want to use for transcription \n"))
        selected_device = input_devices[input_device_id]
        LOGGER.info(f"Transcript using input device: {selected_device}")        
        try:

            while True:
                input("Press Enter to start recording or Ctrl+C to cancel...")
                transcript , command = self.capture_action(selected_device)
                if command:
                    try:
                        self.terminals_gateway.execute_command(command)
                    except Exception as ex:
                        self.term_cache_gateway.delete_term(transcript)
        except KeyboardInterrupt:
            LOGGER.info("Recording cancelled by user.")
            return        
