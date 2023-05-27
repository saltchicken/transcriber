from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np

class Transcriber():
    
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-base")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
        self.model.config.forced_decoder_ids = None

    def transcribe(self, audio_data):
        numpy_array = np.frombuffer(audio_data, dtype=np.int16) / 32767.0
        input_features = self.processor(numpy_array, sampling_rate=16000, return_tensors="pt").input_features
        predicted_ids = self.model.generate(input_features, max_length= 448)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcription[0].strip()

