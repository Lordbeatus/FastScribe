"""
Fully Automated Flashcard Generator using GitHub Copilot API
Uses the copilot-api library to generate flashcards programmatically.
"""

import requests
import json
import os
import sys

class CopilotFlashcardGenerator:
    """Generate flashcards using GitHub Copilot API (free for students)"""
    
    def __init__(self, copilot_api_url="http://localhost:8080/api"):
        """
        Initialize the Copilot flashcard generator
        
        Args:
            copilot_api_url: URL of the copilot-api server
        """
        self.api_url = copilot_api_url
    
    def generate_flashcards(self, transcript, language="English"):
        """
        Generate Anki flashcards from a transcript using Copilot API
        
        Args:
            transcript: The video transcript text
            language: Language of the content
            
        Returns:
            List of flashcard dictionaries with 'front' and 'back' keys
        """
        prompt = self._create_flashcard_prompt(transcript, language)
        
        try:
            # Send the prompt to Copilot API
            flashcards_text = self._call_copilot_api(prompt, language="markdown")
            
            # Parse the generated flashcards
            flashcards = self._parse_flashcards(flashcards_text)
            
            return flashcards
            
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Could not connect to Copilot API. "
                "Please make sure the copilot-api server is running:\n"
                "python copilot-api/api.py 8080"
            )
    
    def _create_flashcard_prompt(self, transcript, language):
        """Create a detailed prompt for flashcard generation"""
        prompt = f"""# Task: Convert this {language} transcript into Anki flashcards

## Transcript:
{transcript[:3000]}  # Limit to avoid token issues

## Instructions:
Create comprehensive Anki flashcards following these rules:

1. Format: Each flashcard must be in this exact format:
   Q: [Question]
   A: [Answer]
   
   [blank line between flashcards]

2. Content Guidelines:
   - Extract ALL key concepts, definitions, and important facts
   - Create 15-25 flashcards covering the main topics
   - Questions should be clear and specific
   - Answers should be concise but complete
   - Use simple language, avoid jargon unless defined
   - Include context when needed

3. Types of flashcards to create:
   - Definitions: "What is [term]?"
   - Explanations: "How does [concept] work?"
   - Examples: "Give an example of [concept]"
   - Comparisons: "What is the difference between X and Y?"
   - Applications: "When would you use [technique]?"

4. Quality Standards:
   - Each flashcard should test ONE concept
   - Avoid yes/no questions
   - Use active recall format
   - Keep answers focused and factual

## Output (generate flashcards below):

"""
        return prompt
    
    def _call_copilot_api(self, prompt, language="python", max_iterations=5):
        """
        Call the Copilot API iteratively to build the complete response
        
        The copilot-api returns completions incrementally, so we need to
        append generated text and call again until we get a complete response.
        """
        result = ""
        current_prompt = prompt
        
        for i in range(max_iterations):
            response = requests.post(
                self.api_url,
                json={
                    "prompt": current_prompt,
                    "language": language
                },
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Copilot API error: {response.status_code} - {response.text}")
            
            completion = response.text.strip()
            
            # If empty response, we're done
            if not completion:
                break
            
            result += completion
            current_prompt += completion
            
            # Check if we have enough flashcards (looking for multiple Q: patterns)
            if result.count("Q:") >= 10:  # Stop after getting at least 10 flashcards
                break
        
        return result
    
    def _parse_flashcards(self, flashcards_text):
        """
        Parse the generated text into structured flashcard format
        
        Expected format:
        Q: Question here
        A: Answer here
        
        Q: Next question
        A: Next answer
        """
        flashcards = []
        lines = flashcards_text.split('\n')
        
        current_question = None
        current_answer = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                # Save the current flashcard if both Q and A are present
                if current_question and current_answer:
                    flashcards.append({
                        'front': current_question,
                        'back': current_answer
                    })
                    current_question = None
                    current_answer = None
                continue
            
            # Check for question
            if line.startswith('Q:'):
                # Save previous flashcard if exists
                if current_question and current_answer:
                    flashcards.append({
                        'front': current_question,
                        'back': current_answer
                    })
                
                current_question = line[2:].strip()
                current_answer = None
            
            # Check for answer
            elif line.startswith('A:'):
                current_answer = line[2:].strip()
            
            # Multi-line answer continuation
            elif current_answer is not None and not line.startswith('Q:'):
                current_answer += ' ' + line
        
        # Don't forget the last flashcard
        if current_question and current_answer:
            flashcards.append({
                'front': current_question,
                'back': current_answer
            })
        
        return flashcards
    
    def format_for_anki(self, flashcards):
        """
        Format flashcards for Anki import (CSV format)
        
        Args:
            flashcards: List of flashcard dictionaries
            
        Returns:
            String in Anki CSV format
        """
        # Anki CSV format: Front,Back
        lines = []
        for card in flashcards:
            # Escape quotes and commas
            front = card['front'].replace('"', '""')
            back = card['back'].replace('"', '""')
            lines.append(f'"{front}","{back}"')
        
        return '\n'.join(lines)


def main():
    """CLI interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: python copilot_flashcard_generator.py <transcript_file>")
        print("\nMake sure copilot-api is running:")
        print("  git clone https://github.com/B00TK1D/copilot-api.git")
        print("  cd copilot-api")
        print("  pip install -r requirements.txt")
        print("  python api.py 8080")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    
    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    print("🚀 Generating flashcards with GitHub Copilot API...")
    
    # Generate flashcards
    generator = CopilotFlashcardGenerator()
    flashcards = generator.generate_flashcards(transcript)
    
    print(f"✅ Generated {len(flashcards)} flashcards!")
    print("\n" + "="*60)
    
    # Display flashcards
    for i, card in enumerate(flashcards, 1):
        print(f"\n📝 Flashcard {i}:")
        print(f"Q: {card['front']}")
        print(f"A: {card['back']}")
    
    # Save to Anki format
    anki_csv = generator.format_for_anki(flashcards)
    output_file = transcript_file.replace('.txt', '_flashcards.csv')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(anki_csv)
    
    print("\n" + "="*60)
    print(f"💾 Saved to: {output_file}")
    print("\n📚 Import into Anki:")
    print("  1. Open Anki")
    print("  2. File → Import")
    print(f"  3. Select: {output_file}")
    print("  4. Set Field separator: Comma")
    print("  5. Click Import")


if __name__ == '__main__':
    main()
