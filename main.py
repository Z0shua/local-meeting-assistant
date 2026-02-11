import os
import time
import argparse
from recorder import AudioRecorder
from transcriber import Transcriber
from summarizer import MeetingSummarizer

OUTPUT_DIR = "output"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def record_workflow():
    print("\n--- Audio Recording ---")
    filename = input("Enter filename for recording (default: meeting): ").strip()
    if not filename:
        filename = "meeting"
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"{filename}_{timestamp}.wav")
    
    recorder = AudioRecorder()
    recorder.start()
    input("Press Enter to stop recording...")
    recorder.stop()
    recorder.save(filepath)
    return filepath

def transcribe_workflow(audio_path, model="base"):
    print(f"\n--- Transcribing {audio_path} ---")
    transcriber = Transcriber(model_name=model)
    text = transcriber.transcribe(audio_path)
    
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    text_path = os.path.join(OUTPUT_DIR, f"{base_name}_transcript.txt")
    
    with open(text_path, "w") as f:
        f.write(text)
    
    print(f"Transcript saved to: {text_path}")
    return text, text_path

def summarize_workflow(text, model="llama3"):
    print("\n--- Generating Summary ---")
    summarizer = MeetingSummarizer(model=model)
    summary = summarizer.summarize(text)
    
    return summary

def main():
    ensure_output_dir()
    parser = argparse.ArgumentParser(description="Local Meeting Assistant")
    parser.add_argument("--record", action="store_true", help="Start a new recording")
    parser.add_argument("--transcribe", type=str, help="Transcribe an existing audio file")
    parser.add_argument("--summarize", type=str, help="Summarize an existing text file")
    parser.add_argument("--model", type=str, default="base", help="Whisper model to use (base, small, medium, large)")
    parser.add_argument("--llm", type=str, default="llama3", help="Ollama model to use")
    
    args = parser.parse_args()

    if args.record:
        audio_path = record_workflow()
        
        # Auto proceeding to transcribe and summarize?
        # Let's ask user or just do it. Detailed plan implied pipeline.
        do_process = input("Propcess this recording (transcribe + summarize)? [Y/n]: ").strip().lower()
        if do_process != 'n':
            transcript, text_path = transcribe_workflow(audio_path, args.model)
            summary = summarize_workflow(transcript, args.llm)
            
            summary_path = text_path.replace("_transcript.txt", "_summary.md")
            with open(summary_path, "w") as f:
                f.write(summary)
            print(f"\nSummary saved to: {summary_path}")
            print("\n" + "="*40)
            print(summary)
            print("="*40)

    elif args.transcribe:
        transcript, text_path = transcribe_workflow(args.transcribe, args.model)
        
        do_summ = input("Summarize this transcript? [Y/n]: ").strip().lower()
        if do_summ != 'n':
            summary = summarize_workflow(transcript, args.llm)
            summary_path = text_path.replace("_transcript.txt", "_summary.md")
            with open(summary_path, "w") as f:
                f.write(summary)
            print(f"\nSummary saved to: {summary_path}")

    elif args.summarize:
        with open(args.summarize, "r") as f:
            text = f.read()
        summary = summarize_workflow(text, args.llm)
        print("\n" + "="*40)
        print(summary)
        print("="*40)
        
        base_name = os.path.splitext(os.path.basename(args.summarize))[0]
        if base_name.endswith("_transcript"):
            base_name = base_name.replace("_transcript", "")
        
        summary_path = os.path.join(OUTPUT_DIR, f"{base_name}_summary.md")
        with open(summary_path, "w") as f:
            f.write(summary)
            print(f"Summary saved to: {summary_path}")

    else:
        # Default interactive mode
        print("Welcome to Local Meeting Assistant")
        print("1. Record new meeting")
        print("2. Transcribe file")
        print("3. Summarize text")
        choice = input("Select option: ").strip()
        
        if choice == "1":
            audio_path = record_workflow()
            transcript, text_path = transcribe_workflow(audio_path)
            summary = summarize_workflow(transcript, "llama3")
            summary_path = text_path.replace("_transcript.txt", "_summary.md")
            with open(summary_path, "w") as f:
                f.write(summary)
            print(f"Summary saved to {summary_path}")
            
        elif choice == "2":
            path = input("Enter audio file path: ").strip()
            transcribe_workflow(path)
        elif choice == "3":
            path = input("Enter text file path: ").strip()
            with open(path, "r") as f:
                text = f.read()
            summary = summarize_workflow(text, "llama3")
            print(summary)

if __name__ == "__main__":
    main()
