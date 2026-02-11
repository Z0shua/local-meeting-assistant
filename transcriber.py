import whisper
import os

class Transcriber:
    def __init__(self, model_name="base"):
        self.model_name = model_name
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
        print("Model loaded.")

    def transcribe(self, audio_path):
        """Transcribes the audio file and returns text."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing {audio_path}...")
        result = self.model.transcribe(audio_path)
        return result["text"].strip()

if __name__ == "__main__":
    # Test block
    t = Transcriber()
    # Assume test_recording.wav exists from recorder test
    if os.path.exists("test_recording.wav"):
        print(t.transcribe("test_recording.wav"))
