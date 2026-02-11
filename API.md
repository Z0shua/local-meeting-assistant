# API Documentation

## Overview

This document provides detailed API reference for the Local Meeting Assistant modules.

---

## AudioRecorder

Class for recording audio from the microphone.

### Class: `AudioRecorder`

```python
from recorder import AudioRecorder

recorder = AudioRecorder(sample_rate=44100, channels=1)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sample_rate` | int | 44100 | Audio sample rate in Hz |
| `channels` | int | 1 | Number of audio channels (1=mono, 2=stereo) |

#### Methods

##### `start()`
Begins recording audio in a background thread.

**Returns:** None

**Example:**
```python
recorder.start()
print("Recording started...")
```

##### `stop()`
Stops the active recording.

**Returns:** None

**Example:**
```python
recorder.stop()
print("Recording stopped.")
```

##### `save(filename: str)`
Saves the recorded audio to a WAV file.

**Parameters:**
- `filename` (str): Path where the WAV file will be saved

**Returns:** None

**Raises:** 
- `IOError`: If the file cannot be written

**Example:**
```python
recorder.save("meeting_2026_02_11.wav")
```

#### Complete Example

```python
from recorder import AudioRecorder
import time

recorder = AudioRecorder(sample_rate=44100)
recorder.start()

# Record for 10 seconds
time.sleep(10)

recorder.stop()
recorder.save("output/my_recording.wav")
```

---

## Transcriber

Speech-to-text transcription using OpenAI Whisper.

### Class: `Transcriber`

```python
from transcriber import Transcriber

transcriber = Transcriber(model_name="base")
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | str | "base" | Whisper model size: "tiny", "base", "small", "medium", "large" |

#### Methods

##### `transcribe(audio_path: str) -> str`
Transcribes an audio file to text.

**Parameters:**
- `audio_path` (str): Path to the audio file (WAV, MP3, FLAC, etc.)

**Returns:** 
- str: The transcribed text

**Raises:**
- `FileNotFoundError`: If audio file doesn't exist
- `RuntimeError`: If transcription fails

**Example:**
```python
transcriber = Transcriber(model_name="base")
text = transcriber.transcribe("meeting.wav")
print(text)
```

#### Model Selection

| Model | Size | Use Case |
|-------|------|----------|
| tiny | 39MB | Quick testing, limited accuracy |
| base | 140MB | Good balance (recommended) |
| small | 244MB | Higher accuracy for important meetings |
| medium | 769MB | Production quality |
| large | 1550MB | Maximum accuracy (requires GPU for speed) |

#### Performance Notes

- First run downloads the model (~100MB-1.5GB depending on size)
- Subsequent runs use cached models
- Execution time varies with audio length and model size
- GPU acceleration available if CUDA is detected

#### Example: Transcribe Multiple Files

```python
from transcriber import Transcriber
from pathlib import Path

transcriber = Transcriber(model_name="small")

audio_files = Path("recordings").glob("*.wav")
for audio_file in audio_files:
    text = transcriber.transcribe(str(audio_file))
    output_file = audio_file.with_suffix(".txt")
    with open(output_file, "w") as f:
        f.write(text)
    print(f"Transcribed: {audio_file}")
```

---

## MeetingSummarizer

Intelligent meeting summary generation using Ollama.

### Class: `MeetingSummarizer`

```python
from summarizer import MeetingSummarizer

summarizer = MeetingSummarizer(model="llama3")
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | "llama3" | Ollama model name for summarization |

#### Methods

##### `summarize(text: str) -> str`
Generates a structured summary of meeting text.

**Parameters:**
- `text` (str): The meeting transcript or conversation text

**Returns:**
- str: The generated summary with key topics, action items, and brief summary

**Example:**
```python
summarizer = MeetingSummarizer(model="llama3")
transcript = "..."  # Long meeting transcript
summary = summarizer.summarize(transcript)
print(summary)
```

#### Output Format

The summarizer returns structured output:

```
1. **Key Topics Discussed**
   - Topic 1
   - Topic 2
   - ...

2. **Action Items** (if any)
   - [ ] Action item 1 - Owner
   - [ ] Action item 2 - Owner

3. **Brief Summary**
   A concise overview of the meeting...
```

#### Available Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama2 | 3.8B | Fast ⚡ | Good ⭐⭐⭐ | Quick summaries |
| llama3 | 7B | Medium ⚡⚡ | Excellent ⭐⭐⭐⭐⭐ | Recommended |
| neural-chat | 13B | Slow 🐢 | Excellent ⭐⭐⭐⭐⭐ | Conversation-optimized |
| mistral | 7B | Fast ⚡ | Good ⭐⭐⭐⭐ | Alternative |

#### Setup

Before using, ensure Ollama is running with desired models:

```bash
# Start Ollama service
ollama serve

# In another terminal, pull your desired model
ollama pull llama3
```

#### Error Handling

```python
from summarizer import MeetingSummarizer

summarizer = MeetingSummarizer(model="llama3")
summary = summarizer.summarize(transcript)

if "Error" in summary:
    print("Summary generation failed:", summary)
else:
    print("Summary:", summary)
```

#### Example: Batch Summarization

```python
from summarizer import MeetingSummarizer
from pathlib import Path

summarizer = MeetingSummarizer(model="llama3")

transcripts = Path("transcripts").glob("*.txt")
for transcript_file in transcripts:
    with open(transcript_file, "r") as f:
        text = f.read()
    
    summary = summarizer.summarize(text)
    
    output_file = transcript_file.with_name(
        transcript_file.stem + "_summary.md"
    )
    with open(output_file, "w") as f:
        f.write(summary)
    
    print(f"Summarized: {transcript_file}")
```

---

## GUI Application

### Starting the GUI

```bash
python gui.py
```

### Features

1. **Recording Controls**
   - Start/Stop button toggles recording
   - Visual status indicator
   - Timestamp-based file naming

2. **Transcription Options**
   - Dropdown to select Whisper model size
   - Real-time transcription progress
   - Transcript display in scrollable text area

3. **Summary Generation**
   - Generate summary button
   - Summary preview in dedicated area
   - Copy and export options

4. **Output Management**
   - View generated files
   - Open file location
   - Delete old recordings

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Cmd+Q | Quit application |
| Cmd+S | Save transcript |
| Cmd+C | Copy summary to clipboard |

---

## CLI Application

### Running Main Script

```bash
python main.py
```

### Interactive Workflow

The CLI guides you through:
1. Enter filename for recording (default: "meeting")
2. Press Enter to start recording
3. Press Enter again to stop recording
4. Select Whisper model for transcription
5. View generated transcript
6. Select Ollama model for summarization
7. View generated summary

### Example Session

```
--- Audio Recording ---
Enter filename for recording (default: meeting): project_standup
Recording started... Press Enter to stop.
[Enter pressed]
Recording stopped.

--- Transcribing output/project_standup_20260211_152531.wav ---
Transcript saved to: output/project_standup_20260211_152531_transcript.txt

--- Generating Summary ---
[Summary output...]
Summary saved to: output/project_standup_20260211_152531_summary.md
```

---

## Output Files

### Directory Structure

```
output/
├── meeting_YYYYMMDD_HHMMSS.wav              # Raw audio (WAV format)
├── meeting_YYYYMMDD_HHMMSS_transcript.txt   # Full text transcript
└── meeting_YYYYMMDD_HHMMSS_summary.md       # Structured summary
```

### File Details

**Audio File (`.wav`)**
- Format: Uncompressed WAV
- Sample Rate: 44.1 kHz
- Channels: Mono
- Size: ~10 MB per minute of audio

**Transcript File (`.txt`)**
- Plain text format
- Full transcription of audio
- One statement per line (roughly)
- Suitable for further processing

**Summary File (`.md`)**
- Markdown format
- Structured with headers and bullet points
- Contains: Key Topics, Action Items, Brief Summary
- Ready to share or integrate into documents

---

## Error Handling

### Common Errors and Solutions

**"Model not found" (Whisper)**
```
Solution: The model will auto-download on first use.
Ensure sufficient disk space (~1.5GB for large model)
```

**"Connection refused" (Ollama)**
```
Solution: Start Ollama with: ollama serve
Ensure it's running before attempting summarization
```

**"No microphone detected"**
```
Solution: Check system audio settings
Grant microphone permissions to Python
Test with: python -c "import sounddevice; print(sounddevice.default_device())"
```

**"Out of memory" (Summarization)**
```
Solution: Use a smaller Ollama model
Close other applications
Reduce transcript size (process in chunks)
```

---

## Performance Optimization

### Tips for Faster Processing

1. **Transcription**
   - Use `tiny` or `base` models for speed
   - Enable GPU if available (automatic detection)
   - Process during off-peak hours

2. **Summarization**
   - Use `llama2` for faster summaries
   - Process shorter transcripts
   - Run on machine with sufficient RAM

3. **Recording**
   - Use mono (default) instead of stereo
   - Lower sample rate (22050 Hz) if quality permits
   - Ensure minimal background noise

---

## Version Information

- Python: 3.8+
- Whisper: Latest from OpenAI
- Ollama: 0.1.0+
- CustomTkinter: Latest

---

## Additional Resources

- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [Ollama Documentation](https://ollama.ai)
- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)

