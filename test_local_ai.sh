# Test local AI models
cd backend

# Install local AI dependencies
pip install openai-whisper torch transformers accelerate sentencepiece

# Test local Whisper (downloads base model ~74MB on first run)
echo "Testing local Whisper..."
python hybrid_transcriber.py

# Test local LLM (downloads TinyLlama ~1.1GB on first run)
echo "Testing local LLM..."
python hybrid_notes.py

echo "Tests complete! Models are cached for future use."
