"""
Hybrid Notes Creator - supports both local LLM and OpenAI API
Automatically uses local if no API key is available
"""

import os


class HybridNotesCreator:
    """Generate flashcards using local LLM or OpenAI API"""
    
    def __init__(self, use_local=None, model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
        """
        Args:
            use_local: True=force local, False=force API, None=auto-detect
            model_name: For local LLM: HuggingFace model name
        """
        # Auto-detect if not specified
        if use_local is None:
            api_key = os.getenv('OPENAI_API_KEY')
            use_local = not api_key or api_key.startswith('sk-abcde')
        
        self.use_local = use_local
        
        if use_local:
            print(f"Using LOCAL LLM ({model_name})")
            from local_llm import LocalLLM
            self.llm = LocalLLM(model_name=model_name)
        else:
            print("Using OpenAI GPT-4 API")
            from openai import OpenAI
            from apiKeyCycler import get_next_api_key
            api_key = get_next_api_key()
            self.client = OpenAI(api_key=api_key)
    
    def create_notes(self, transcript, style='flashcards', max_cards=10):
        """
        Generate notes from transcript
        Args:
            transcript: The transcript text
            style: Output style (flashcards, detailed, summary, bullet_points)
            max_cards: Maximum number of flashcards
        Returns:
            Generated notes text
        """
        if self.use_local:
            # Use local LLM
            notes = self.llm.generate_flashcards(
                transcript, 
                style=style, 
                max_cards=max_cards
            )
        else:
            # Use OpenAI API
            style_prompts = {
                'flashcards': f'Create {max_cards} study flashcards in Q&A format from this transcript. Use this exact format:\n\nQ: [question]\nA: [answer]\n\nQ: [question]\nA: [answer]',
                'detailed': 'Create detailed study notes from this transcript with explanations and examples.',
                'summary': 'Summarize the main points from this transcript in a concise format.',
                'bullet_points': 'Extract the key points from this transcript as bullet points.'
            }
            
            system_prompt = style_prompts.get(style, style_prompts['flashcards'])
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript[:4000]}  # Limit context
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            notes = response.choices[0].message.content
        
        return notes


if __name__ == '__main__':
    # Test
    sample_transcript = """
    Today we're learning about photosynthesis. Photosynthesis is the process where plants
    convert sunlight into energy. The process happens in chloroplasts. Plants absorb carbon
    dioxide from the air and water from the ground. Using sunlight as energy, they convert
    these into glucose and oxygen. The glucose provides energy for the plant, while oxygen
    is released into the air for us to breathe.
    """
    
    creator = HybridNotesCreator(use_local=True)
    notes = creator.create_notes(sample_transcript, style='flashcards', max_cards=3)
    
    print(f"\nGenerated notes:\n{notes}")
