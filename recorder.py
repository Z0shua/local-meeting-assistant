import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import time
import sys

class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames = []
        self.thread = None

    def _record_loop(self):
        """Internal loop to read from the stream."""
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._callback):
            while self.recording:
                sd.sleep(100)

    def _callback(self, indata, frames, time, status):
        """Callback for sounddevice."""
        if status:
            print(f"Status: {status}", file=sys.stderr)
        self.frames.append(indata.copy())

    def start(self):
        """Starts the recording in a separate thread."""
        if self.recording:
            print("Already recording...")
            return

        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record_loop)
        self.thread.start()
        print("Recording started... Press Enter to stop.")

    def stop(self):
        """Stops the recording and returns the filename."""
        if not self.recording:
            return

        self.recording = False
        self.thread.join()
        print("Recording stopped.")

    def save(self, filename):
        """Saves the recorded audio to a WAV file."""
        if not self.frames:
            print("No audio recorded.")
            return

        # Concatenate all blocks
        audio_data = np.concatenate(self.frames, axis=0)
        
        # Save as WAV
        wav.write(filename, self.sample_rate, (audio_data * 32767).astype(np.int16))
        print(f"Saved recording to {filename}")
        return filename

if __name__ == "__main__":
    # Test block
    recorder = AudioRecorder()
    recorder.start()
    input("Press Enter to stop...")
    recorder.stop()
    recorder.save("test_recording.wav")
