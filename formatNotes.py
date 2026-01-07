"""
Format Notes for Anki and Google Docs Export
"""

import os
import csv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle


class NotesFormatter:
    """Format notes for Anki import and Google Docs export"""
    
    def __init__(self):
        self.flashcards = []
        self.google_creds = None
    
    def parse_flashcards(self, notes_text):
        """
        Parse Q&A format notes into flashcard list
        Expected format:
        Q: Question text
        A: Answer text
        """
        self.flashcards = []
        lines = notes_text.strip().split('\n')
        
        current_question = None
        current_answer = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Q:'):
                # Save previous flashcard if exists
                if current_question and current_answer:
                    self.flashcards.append({
                        'question': current_question,
                        'answer': current_answer
                    })
                
                current_question = line[2:].strip()
                current_answer = None
            
            elif line.startswith('A:'):
                current_answer = line[2:].strip()
            
            elif current_question and not current_answer:
                # Multi-line question
                current_question += ' ' + line
            
            elif current_answer:
                # Multi-line answer
                current_answer += ' ' + line
        
        # Add last flashcard
        if current_question and current_answer:
            self.flashcards.append({
                'question': current_question,
                'answer': current_answer
            })
        
        return self.flashcards
    
    def export_to_anki_csv(self, filename="anki_flashcards.csv", deck_name="YouTube Notes"):
        """
        Export flashcards to Anki-compatible CSV
        Format: Front, Back, Tags
        """
        if not self.flashcards:
            raise ValueError("No flashcards available. Call parse_flashcards first.")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            
            for card in self.flashcards:
                # Anki CSV format: Front;Back;Tags
                writer.writerow([
                    card['question'],
                    card['answer'],
                    deck_name
                ])
        
        print(f"Anki CSV exported to: {filename}")
        print(f"To import into Anki:")
        print(f"1. Open Anki")
        print(f"2. File > Import > Select {filename}")
        print(f"3. Set delimiter to 'Semicolon'")
        print(f"4. Map fields: Field 1 -> Front, Field 2 -> Back, Field 3 -> Tags")
        
        return filename
    
    def export_to_anki_txt(self, filename="anki_flashcards.txt"):
        """
        Export flashcards to Anki-compatible TXT format
        More flexible format with HTML support
        """
        if not self.flashcards:
            raise ValueError("No flashcards available. Call parse_flashcards first.")
        
        with open(filename, 'w', encoding='utf-8') as f:
            for card in self.flashcards:
                # Format: Question\tAnswer\n
                f.write(f"{card['question']}\t{card['answer']}\n")
        
        print(f"Anki TXT exported to: {filename}")
        return filename
    
    def setup_google_docs_auth(self, credentials_file='credentials.json'):
        """
        Setup Google Docs authentication
        Args:
            credentials_file: Path to Google OAuth credentials JSON
        """
        SCOPES = ['https://www.googleapis.com/auth/documents', 
                  'https://www.googleapis.com/auth/drive.file']
        
        creds = None
        
        # Token file stores user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    raise FileNotFoundError(
                        f"Google OAuth credentials file '{credentials_file}' not found. "
                        "Download it from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.google_creds = creds
        return creds
    
    def export_to_google_docs(self, notes_text, title="YouTube Notes"):
        """
        Export notes to Google Docs
        Args:
            notes_text: Notes content
            title: Document title
        Returns:
            Document URL
        """
        if not self.google_creds:
            raise ValueError("Google Docs not authenticated. Call setup_google_docs_auth first.")
        
        try:
            # Build the Docs API service
            docs_service = build('docs', 'v1', credentials=self.google_creds)
            drive_service = build('drive', 'v3', credentials=self.google_creds)
            
            # Create a new document
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc['documentId']
            
            # Insert text into document
            requests = [
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': notes_text
                    }
                }
            ]
            
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            print(f"Notes exported to Google Docs: {doc_url}")
            
            return doc_url
        
        except Exception as e:
            raise Exception(f"Error exporting to Google Docs: {e}")


def main():
    """Example usage"""
    formatter = NotesFormatter()
    
    # Example: Load notes and format
    try:
        with open("notes.txt", 'r', encoding='utf-8') as f:
            notes = f.read()
        
        # Parse flashcards
        flashcards = formatter.parse_flashcards(notes)
        print(f"Parsed {len(flashcards)} flashcards")
        
        # Export to Anki
        formatter.export_to_anki_csv("anki_cards.csv")
        formatter.export_to_anki_txt("anki_cards.txt")
        
        # Export to Google Docs (requires authentication)
        # formatter.setup_google_docs_auth('credentials.json')
        # formatter.export_to_google_docs(notes, "My YouTube Notes")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
