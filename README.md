# Local Meeting Assistant

A lightweight, privacy-focused meeting assistant that records audio, transcribes it using OpenAI's Whisper, and generates intelligent summaries using Ollama. All processing happens locally—no data is sent to external servers.

## Features

- 🎤 **Audio Recording**: Record meetings directly from your microphone
- 📝 **Transcription**: Convert audio to text using OpenAI Whisper (multiple model sizes available)
- 🤖 **Smart Summarization**: Generate structured summaries with key topics and action items using Ollama
- 🖥️ **GUI Application**: User-friendly interface built with CustomTkinter
- 💻 **CLI Support**: Command-line interface for scripting and automation
- 🔒 **Privacy First**: Everything runs locally—no cloud dependencies

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed and running (for summarization features)
- Microphone access

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running (required for summarization):
   ```bash
   ollama serve
   ```

### Usage

#### GUI Application (Recommended)

Start the graphical interface:
```bash
python gui.py
```

The GUI provides:
- One-click recording with visual feedback
- Model selection for transcription quality
- Live transcript display
- Summary generation
- Output management

#### CLI Application

Run the command-line interface:
```bash
python main.py
```

Follow the interactive prompts to:
1. Record a meeting
2. Transcribe the audio
3. Generate a summary

#### Using as a Module

```python
from recorder import AudioRecorder
from transcriber import Transcriber
from summarizer import MeetingSummarizer

# Record audio
recorder = AudioRecorder()
recorder.start()
# ... recording ...
recorder.stop()
recorder.save("my_meeting.wav")

# Transcribe
transcriber = Transcriber(model_name="base")
text = transcriber.transcribe("my_meeting.wav")

# Summarize
summarizer = MeetingSummarizer(model="llama3")
summary = summarizer.summarize(text)
print(summary)
```

## Project Structure

```
local_meeting_assistant/
├── gui.py                 # CustomTkinter GUI application
├── main.py               # CLI interface and orchestration
├── recorder.py           # Audio recording functionality
├── transcriber.py        # Whisper-based transcription
├── summarizer.py         # Ollama-based summarization
├── requirements.txt      # Python dependencies
├── output/               # Generated transcripts and summaries
└── README.md            # This file
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `sounddevice` | Audio input/output handling |
| `numpy` | Numerical operations for audio processing |
| `scipy` | Scientific computing for audio I/O |
| `openai-whisper` | Speech-to-text transcription |
| `ollama` | Local LLM integration for summarization |
| `customtkinter` | Modern GUI framework |
| `packaging` | Version compatibility utilities |

## Configuration

### Transcription Models

Whisper offers different model sizes. Choose based on accuracy vs. speed:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 39M | ⚡⚡⚡ | ⭐ |
| `base` | 140M | ⚡⚡ | ⭐⭐⭐ |
| `small` | 244M | ⚡ | ⭐⭐⭐⭐ |
| `medium` | 769M | 🐢 | ⭐⭐⭐⭐ |
| `large` | 1550M | 🐢🐢 | ⭐⭐⭐⭐⭐ |

Select via GUI dropdown or pass to `Transcriber(model_name="base")`

### Summarization Models

Requires Ollama with installed models. Popular options:

- `llama3` - Balanced quality and speed
- `llama2` - Smaller, faster
- `neural-chat` - Optimized for conversations

Pull a model with: `ollama pull llama3`

## Output

All outputs are saved to the `output/` directory:

- `meeting_YYYYMMDD_HHMMSS.wav` - Raw audio recording
- `meeting_YYYYMMDD_HHMMSS_transcript.txt` - Full transcription
- `meeting_YYYYMMDD_HHMMSS_summary.md` - Structured summary

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check that port 11434 is accessible
- Verify the model exists: `ollama list`

### No Audio Input
- Check microphone permissions
- Verify audio device is selected/connected
- Test with system audio settings

### Transcription is Slow
- Use a smaller Whisper model (`tiny` or `base`)
- Ensure your system has sufficient disk space for models
- GPU acceleration can help (if available)

### Out of Memory
- Use smaller models for both Whisper and Ollama
- Close other applications
- Process shorter audio segments

## Customization

### Change Default Sample Rate

Edit `recorder.py`:
```python
recorder = AudioRecorder(sample_rate=48000)  # Default is 44100
```

### Adjust Summarization Prompt

Edit `summarizer.py` to customize the summary structure and output format.

### Add Custom Transcription Post-Processing

Extend `Transcriber` class to clean up transcription output:
```python
class CustomTranscriber(Transcriber):
    def transcribe(self, audio_path):
        text = super().transcribe(audio_path)
        # Custom post-processing
        return text.upper()  # Example
```

## Tips & Best Practices

1. **Recording Quality**: Use a high-quality microphone for better transcription accuracy
2. **Model Selection**: Start with `base` model; upgrade if accuracy isn't sufficient
3. **Batch Processing**: Process multiple meetings by running the CLI in sequence
4. **Storage**: Regularly archive old meetings; raw WAV files consume significant space
5. **Ollama Models**: Download models during off-peak hours; larger models need time

## Known Limitations

- Single-speaker focus; performance degrades with multiple speakers
- English language optimized (Whisper supports other languages)
- Summary quality depends on Ollama model choice and transcript clarity
- Real-time transcription not supported (batch processing only)

## Future Enhancements

- [ ] Multi-speaker diarization
- [ ] Real-time transcription streaming
- [ ] Speaker identification
- [ ] Export formats (PDF, DOCX, JSON)
- [ ] Meeting scheduling integration
- [ ] Conversation history tracking

## License

[Add your license here]

## Support

For issues, questions, or contributions, please [specify your support channel].

---

**Made with ❤️ for privacy-conscious teams**
