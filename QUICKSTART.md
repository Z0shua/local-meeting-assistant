# Quick Start Guide

Get up and running with Local Meeting Assistant in 5 minutes.

## Installation

### 1. Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Verify pip is installed
pip --version
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected installation time: 2-5 minutes (depending on internet speed)

### 3. Install & Start Ollama

Ollama is required for summarization features.

**Option A: Download from ollama.ai**
```bash
# Visit https://ollama.ai and download installer for macOS
# After installation, start Ollama
ollama serve
```

**Option B: Using Homebrew (macOS)**
```bash
brew install ollama
ollama serve
```

### 4. Pull a Summarization Model (Required)

Open a new terminal while Ollama is running:

```bash
ollama pull llama3
```

This downloads the model (~5 GB, one-time only). Time varies with internet speed.

---

## First Meeting Recording

### Option 1: GUI (Easiest)

```bash
python gui.py
```

1. Click **"Start Recording"** (button turns red)
2. Speak your meeting content
3. Click **"Stop Recording"** (button turns green)
4. Select transcription model (default: "base" is fine)
5. Click **"Transcribe"** - wait for processing
6. Click **"Summarize"** - view results

### Option 2: Command Line

```bash
python main.py
```

Follow interactive prompts:
1. Enter meeting name or press Enter for default
2. Press Enter to start recording
3. Press Enter again to stop recording
4. Select Whisper model (choose "base" if unsure)
5. Transcription begins automatically
6. View transcript and summary in the terminal

---

## Understanding Model Selection

### Transcription Model (Whisper)

Choose based on your computer:

| Your Computer | Recommended Model | Speed |
|---|---|---|
| Older/Limited RAM | `tiny` | 30 sec / 1 min audio |
| Typical laptop | `base` | 60 sec / 1 min audio |
| Powerful machine | `small` or `medium` | 120+ sec / 1 min audio |

**Pro tip:** Start with "base"—it's a great balance of speed and accuracy.

### Summary Model (Ollama)

Models already required for summarization:
- **llama3** (default): Best quality and speed balance ✅ Recommended
- **llama2**: Faster, slightly lower quality
- **neural-chat**: Best for conversations

To use a different model:

```python
# In GUI: Select from dropdown in main window
# In CLI: Select when prompted
# In code:
from summarizer import MeetingSummarizer
summarizer = MeetingSummarizer(model="llama2")
```

---

## Common First-Time Tasks

### I want to test without recording

```bash
# Create a test transcript file
echo "Today we discussed project roadmap. Alice will handle Q1 planning. Bob will update documentation." > test_transcript.txt

# Summarize it
python -c "
from summarizer import MeetingSummarizer
with open('test_transcript.txt', 'r') as f:
    text = f.read()
summarizer = MeetingSummarizer()
print(summarizer.summarize(text))
"
```

### I want to process an existing audio file

```python
from transcriber import Transcriber

transcriber = Transcriber(model_name="base")
text = transcriber.transcribe("path/to/your/audio.wav")
print(text)
```

### I want to just transcribe (no summary)

```python
from transcriber import Transcriber

transcriber = Transcriber()
text = transcriber.transcribe("meeting.wav")

with open("transcript.txt", "w") as f:
    f.write(text)
```

### I want to test summarization without recording

```python
from summarizer import MeetingSummarizer

sample_transcript = """
The team met to discuss Q1 objectives. Key points:
- New product launch scheduled for March 15
- Marketing needs 3 weeks for campaign prep
- Engineering estimates 4 weeks for implementation
- Finance will finalize budget by end of week

Action items:
- Sarah: Prepare detailed project timeline by Friday
- Mike: Review implementation feasibility
- Lisa: Coordinate with external partners

Next meeting: February 18, 2026
"""

summarizer = MeetingSummarizer(model="llama3")
summary = summarizer.summarize(sample_transcript)
print(summary)
```

---

## Finding Output Files

All recordings, transcripts, and summaries are saved to the `output/` folder:

```bash
# View all generated files
ls -lah output/

# Open the output folder in Finder (macOS)
open output/

# View latest transcript
cat output/meeting_*_transcript.txt | tail -1

# View latest summary
cat output/meeting_*_summary.md | tail -1
```

---

## Troubleshooting First Run

### Problem: "Ollama connection refused"

**Solution:**
```bash
# Make sure Ollama is running in another terminal
ollama serve

# Verify connection
curl http://localhost:11434/api/tags
```

### Problem: "Model not found" (Whisper)

**Solution:**
Don't worry! Whisper auto-downloads on first use. It needs:
- Internet connection (first run only)
- ~1.5GB disk space
- Time (30 seconds to 2 minutes depending on model)

### Problem: No microphone input

**Solution:**
```bash
# Check if microphone is detected
python -c "
import sounddevice as sd
print('Default device:', sd.default_device())
print('Available devices:')
print(sd.query_devices())
"

# Check macOS permissions:
# System Preferences > Security & Privacy > Microphone
# Ensure Python/Terminal has access
```

### Problem: "Running out of memory" or "Slow"

**Solution:**
1. Use smaller models:
   ```python
   transcriber = Transcriber(model_name="tiny")  # Faster
   summarizer = MeetingSummarizer(model="llama2")  # Faster
   ```

2. Close other applications to free RAM

3. Restart Ollama:
   ```bash
   pkill ollama
   sleep 2
   ollama serve
   ```

---

## Next Steps

After your first successful recording:

1. **Customize output:** Edit `main.py` or `gui.py` to save in different locations
2. **Integrate with workflows:** Import modules in your own scripts
3. **Improve accuracy:** Experiment with larger Whisper models for important meetings
4. **Batch processing:** Process multiple audio files programmatically
5. **Share summaries:** Export to PDF or send directly to team

---

## Useful Commands Reference

```bash
# Start GUI
python gui.py

# Run CLI
python main.py

# Start Ollama service
ollama serve

# Pull a model for Ollama
ollama pull llama3

# List available Ollama models
ollama list

# Test microphone
python -c "import sounddevice; sd.rec(48000).play()"

# Clean old recordings (CAUTION!)
rm output/*.wav

# View recent summary
cat output/*_summary.md | head -50
```

---

## Need Help?

- Check [README.md](README.md) for full documentation
- Review [API.md](API.md) for detailed module reference
- See TROUBLESHOOTING section in [README.md](README.md)

---

**Enjoy your first meeting recording! 🎉**
