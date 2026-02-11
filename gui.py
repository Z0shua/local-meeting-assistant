import customtkinter as ctk
import threading
import os
import time
from recorder import AudioRecorder
from transcriber import Transcriber
from summarizer import MeetingSummarizer

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

OUTPUT_DIR = "output"

class MeetingAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Local Meeting Assistant")
        self.geometry("900x700")

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Transcript area grows

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.label_title = ctk.CTkLabel(self.header_frame, text="Local Meeting Assistant", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(padx=10, pady=10)

        # --- Controls ---
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_record = ctk.CTkButton(self.controls_frame, text="Start Recording", command=self.toggle_recording, fg_color="green", hover_color="darkgreen")
        self.btn_record.pack(side="left", padx=10, pady=10)

        self.lbl_status = ctk.CTkLabel(self.controls_frame, text="Status: Idle", text_color="gray")
        self.lbl_status.pack(side="left", padx=10, pady=10)

        # Options
        self.option_model = ctk.CTkOptionMenu(self.controls_frame, values=["base", "small", "medium", "large"])
        self.option_model.pack(side="right", padx=10, pady=10)
        self.lbl_model = ctk.CTkLabel(self.controls_frame, text="Whisper Model:")
        self.lbl_model.pack(side="right", padx=5, pady=10)

        # --- Content Areas ---
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1) # Titles row
        self.content_frame.grid_rowconfigure(1, weight=10) # Text areas row

        # Transcript Section
        self.lbl_transcript = ctk.CTkLabel(self.content_frame, text="Transcript", font=ctk.CTkFont(weight="bold"))
        self.lbl_transcript.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.txt_transcript = ctk.CTkTextbox(self.content_frame)
        self.txt_transcript.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Summary Section
        self.lbl_summary = ctk.CTkLabel(self.content_frame, text="Meeting Notes & Summary", font=ctk.CTkFont(weight="bold"))
        self.lbl_summary.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.txt_summary = ctk.CTkTextbox(self.content_frame)
        self.txt_summary.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew")

        # --- State ---
        self.is_recording = False
        self.recorder = None
        self.current_audio_file = None

        # Ensure output dir
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.btn_record.configure(text="Stop Recording", fg_color="red", hover_color="darkred")
        self.update_status("Recording in progress...")
        
        self.recorder = AudioRecorder()
        self.recorder.start()

    def stop_recording(self):
        self.is_recording = False
        self.btn_record.configure(text="Start Recording", fg_color="green", hover_color="darkgreen")
        self.update_status("Stopping recording...")
        
        # Stop in thread to avoid UI freeze?
        # AudioRecorder.stop() joins the thread, so it might block briefly.
        # Ideally we'd do this async, but for simplicity let's do it here or simple thread.
        threading.Thread(target=self._finish_recording_process).start()

    def _finish_recording_process(self):
        if self.recorder:
            self.recorder.stop()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_{timestamp}.wav"
            filepath = os.path.join(OUTPUT_DIR, filename)
            self.recorder.save(filepath)
            self.current_audio_file = filepath
            
            self.update_status(f"Recording saved: {filename}")
            
            # Start Processing
            self.process_audio(filepath)

    def process_audio(self, filepath):
        self.update_status("Transcribing audio...")
        self.txt_transcript.delete("0.0", "end")
        self.txt_transcript.insert("0.0", "Processing transcription...\n")
        
        def run_pipeline():
            try:
                # Transcribe
                model_name = self.option_model.get()
                transcriber = Transcriber(model_name=model_name)
                text = transcriber.transcribe(filepath)
                
                # Update Transcript UI
                self.txt_transcript.delete("0.0", "end")
                self.txt_transcript.insert("0.0", text)
                
                # Save Transcript
                base_name = os.path.splitext(os.path.basename(filepath))[0]
                text_path = os.path.join(OUTPUT_DIR, f"{base_name}_transcript.txt")
                with open(text_path, "w") as f:
                    f.write(text)

                # Summarize
                self.update_status("Generating summary...")
                self.txt_summary.delete("0.0", "end")
                self.txt_summary.insert("0.0", "Generating summary with Ollama...\n")
                
                summarizer = MeetingSummarizer(model="llama3")
                summary = summarizer.summarize(text)
                
                # Update Summary UI
                self.txt_summary.delete("0.0", "end")
                self.txt_summary.insert("0.0", summary)
                
                # Save Summary
                summary_path = os.path.join(OUTPUT_DIR, f"{base_name}_summary.md")
                with open(summary_path, "w") as f:
                    f.write(summary)
                    
                self.update_status("Done! Files saved in output/ folder.")
                
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
                print(e)

        threading.Thread(target=run_pipeline).start()

    def update_status(self, text):
        self.lbl_status.configure(text=f"Status: {text}")

if __name__ == "__main__":
    app = MeetingAssistantGUI()
    app.mainloop()
