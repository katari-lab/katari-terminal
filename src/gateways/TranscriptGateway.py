import torch
from faster_whisper import WhisperModel
import logging

LOGGER = logging.getLogger(__name__)


class TranscriptGateway:

    def __init__(self):
        model_size = "small.en"
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        LOGGER.info("using %s", device_type)
        if device_type == "cuda":
            self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
        else:            
            self.model = WhisperModel(model_size, device=device_type)

    def transcript(self, audio_file_path, language="en"):
        transcription_segments, transcription_info = self.model.transcribe(
            audio_file_path, beam_size=5, language=language
        )
        LOGGER.info(
            "Detected language '%s' with probability %f"
            % (transcription_info.language, transcription_info.language_probability)
        )
        transcription_result = []
        for segment in transcription_segments:
            LOGGER.info(
                "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
            )
            transcription_result.append(segment.text)
        transcription_result = " ".join(transcription_result).replace("  ", " ")
        return transcription_result.strip()
