# Local AI Setup for FastScribe

This guide shows how to run Whisper and LLM locally without OpenAI API keys.

## Overview

**Local Whisper**: OpenAI's open-source Whisper model
- Runs on CPU (slower) or GPU (faster)
- Model sizes: tiny (39MB), base (74MB), small (244MB), medium (769MB), large (1550MB)
- **Recommended for Render**: `base` (good balance of speed/quality, 74MB)

**Local LLM**: HuggingFace transformers
- TinyLlama-1.1B (1.1GB) - Recommended for Render
- Phi-2 (2.7GB) - Better quality if you have RAM
- Mistral-7B (14GB) - Best quality, needs GPU

## Installation

```bash
cd backend
pip install -r requirements-server.txt
```

This installs:
- `openai-whisper` - Local Whisper transcription
- `torch` - PyTorch for running models
- `transformers` - HuggingFace models
- `accelerate` - Optimized model loading

## Usage

### Test Local Whisper

```bash
# Download a YouTube video first
python transcriber.py  # This downloads audio

# Then transcribe with local Whisper
python local_whisper.py /path/to/audio.mp3
```

### Test Local LLM

```bash
# Create a transcript file first
echo "Sample transcript text..." > transcript.txt

# Generate flashcards
python local_llm.py transcript.txt
```

## Integration

Update `transcriber.py` to use local Whisper:

```python
from local_whisper import LocalWhisperTranscriber

# Instead of OpenAI API:
# client = OpenAI(api_key=...)
# result = client.audio.transcriptions.create(...)

# Use local Whisper:
whisper = LocalWhisperTranscriber(model_size='base')
transcript = whisper.transcribe(audio_file, language='en')
```

Update `createNotes.py` to use local LLM:

```python
from local_llm import LocalLLM

# Instead of OpenAI API:
# client = OpenAI(api_key=...)
# response = client.chat.completions.create(...)

# Use local LLM:
llm = LocalLLM()
notes = llm.generate_flashcards(transcript, style='flashcards')
```

## Performance Considerations

### Render Free Tier Limits:
- **RAM**: 512 MB
- **CPU**: Shared CPU
- **Storage**: 1 GB (ephemeral)

### Recommendations:
1. **Whisper**: Use `tiny` or `base` model (fits in RAM)
2. **LLM**: Use TinyLlama-1.1B (1.1GB - may need to stream load)
3. **Consider**: Processing timeouts on free tier

### Alternative: Use Render Paid Tier
- **Starter**: $7/month, 512MB RAM
- **Standard**: $25/month, 2GB RAM (can run base Whisper + TinyLlama comfortably)

## Docker Considerations

Models will be downloaded on first run. On Render:
- First deployment will be slow (downloading models)
- Models will be re-downloaded on each deploy (ephemeral storage)
- Consider using persistent disk for model cache

## Hybrid Approach

You can mix local and API:
- Use local Whisper (faster than API, no cost)
- Use GPT-4 API for better quality flashcards (only pay for LLM calls)

Or vice versa:
- Use Whisper API (offload transcription)
- Use local LLM (reduce API costs)

## Testing Locally

```bash
# Install dependencies
pip install openai-whisper torch transformers accelerate

# Test Whisper (requires FFmpeg)
python local_whisper.py test_audio.mp3

# Test LLM
python local_llm.py test_transcript.txt
```

## Next Steps

1. Test locally with the above commands
2. Update `transcriber.py` and `createNotes.py` to use local models
3. Test the full pipeline
4. Deploy to Render and monitor memory usage
5. Upgrade Render plan if needed for better performance
