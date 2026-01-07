"""
Create Formatted Notes using GPT
Takes transcript and creates structured notes
"""

import os
from openai import OpenAI
from apiKeyCycler import get_next_api_key


class NotesCreator:
    """Use GPT to create structured notes from transcripts"""
    
    def __init__(self, api_key=None):
        """
        Initialize with OpenAI API key
        Args:
            api_key: OpenAI API key (or uses cycler if not provided)
        """
        # Use provided key or get next from cycler
        self.api_key = api_key or get_next_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.notes = None
    
    def create_notes(self, transcript_text, style="detailed"):
        """
        Create notes from transcript using GPT
        Args:
            transcript_text: Raw transcript text
            style: Note style - "detailed", "summary", "bullet_points", or "flashcards"
        Returns:
            Formatted notes
        """
        prompts = {
            "detailed": """
            Create detailed, well-organized notes from this video transcript. 
            Include:
            - Main topics and subtopics
            - Key concepts and definitions
            - Important examples
            - Action items or takeaways
            Format with clear headers and bullet points.
            """,
            
            "summary": """
            Create a concise summary of this video transcript.
            Focus on the main ideas and key takeaways.
            Keep it brief but comprehensive.
            """,
            
            "bullet_points": """
            Convert this transcript into clear bullet points.
            Organize by main topics.
            Each point should be concise and informative.
            """,
            
            "flashcards": """
            Create flashcard-style Q&A pairs from this transcript.
            Format each as:
            Q: [Question]
            A: [Answer]
            
            Focus on key concepts, definitions, and important facts.
            Make questions clear and answers concise.
            """
        }
        
        prompt = prompts.get(style, prompts["detailed"])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, well-structured study notes."},
                    {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript_text}"}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            self.notes = response.choices[0].message.content
            return self.notes
        
        except Exception as e:
            raise Exception(f"Error creating notes with GPT: {e}")
    
    def save_notes(self, filename):
        """Save notes to file"""
        if not self.notes:
            raise ValueError("No notes available. Call create_notes first.")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.notes)
        
        print(f"Notes saved to: {filename}")


def main():
    """Example usage"""
    # You need to set OPENAI_API_KEY environment variable
    try:
        creator = NotesCreator()
        
        # Example: Load transcript and create notes
        with open("transcript.txt", 'r', encoding='utf-8') as f:
            transcript = f.read()
        
        # Create different styles of notes
        notes = creator.create_notes(transcript, style="flashcards")
        print("Generated Notes:")
        print(notes)
        
        # Save notes
        creator.save_notes("notes.txt")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
