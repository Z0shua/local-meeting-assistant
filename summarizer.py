import ollama

class MeetingSummarizer:
    def __init__(self, model="llama3"):
        self.model = model

    def summarize(self, text):
        """Generates a summary of the provided text using Ollama."""
        if not text:
            return "No text to summarize."

        prompt = f"""
        You are a helpful assistant that summarizes meeting transcripts.
        
        Please provide a structured summary of the following meeting transcript.
        Include:
        1. **Key Topics Discussed**
        2. **Action Items** (if any)
        3. **Brief Summary**

        Transcript:
        {text}
        """

        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Test block
    s = MeetingSummarizer()
    print(s.summarize("This is a test meeting. execution was good. We need to buy milk."))
