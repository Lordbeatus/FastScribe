"""
Local LLM for flashcard generation using HuggingFace transformers
No API keys required - runs entirely locally
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os


class LocalLLM:
    """Generate flashcards using local open-source LLM"""
    
    def __init__(self, model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
        """
        Initialize local LLM
        Args:
            model_name: HuggingFace model to use
                       TinyLlama/TinyLlama-1.1B-Chat-v1.0 (1.1GB) - recommended for Render
                       microsoft/phi-2 (2.7GB) - better quality if you have RAM
                       mistralai/Mistral-7B-Instruct-v0.1 (14GB) - best quality, needs GPU
        """
        self.model_name = model_name
        print(f"Loading {model_name}...")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Use CPU or GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load model with reduced memory usage
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            low_cpu_mem_usage=True,
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        
        print(f"✓ Model loaded on {self.device}")
    
    def generate_flashcards(self, transcript, style='flashcards', max_cards=10):
        """
        Generate flashcards from transcript
        Args:
            transcript: The transcript text to process
            style: Output style (flashcards, detailed, summary, bullet_points)
            max_cards: Maximum number of flashcards to generate
        Returns:
            Generated flashcard text
        """
        # Create prompt based on style
        if style == 'flashcards':
            prompt = f"""Convert this transcript into {max_cards} study flashcards in Q&A format.

Transcript:
{transcript[:2000]}

Generate flashcards in this exact format:
Q: [Question]
A: [Answer]

Q: [Question]
A: [Answer]

Flashcards:"""
        elif style == 'summary':
            prompt = f"""Summarize this transcript into key points.

Transcript:
{transcript[:2000]}

Summary:"""
        else:
            prompt = f"""Create detailed study notes from this transcript.

Transcript:
{transcript[:2000]}

Notes:"""
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generate
        print(f"Generating {style}...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=500,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the generated part (after the prompt)
        generated_text = response[len(prompt):].strip()
        
        print(f"✓ Generation complete")
        
        return generated_text


# Test if run directly
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python local_llm.py <transcript_file>")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    
    with open(transcript_file, 'r') as f:
        transcript = f.read()
    
    llm = LocalLLM()
    flashcards = llm.generate_flashcards(transcript, style='flashcards')
    
    print(f"\nFlashcards:\n{flashcards}")
