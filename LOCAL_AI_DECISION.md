# Local AI Summary for FastScribe

## Current Situation

**Issue:** No OpenAI API keys available for cloud-based Whisper/GPT
**Solution:** Run models locally on Render

## Implementation Complete

I've added these files to enable local AI:

### Core Local AI Files:
- `backend/local_whisper.py` - Runs OpenAI's Whisper locally
- `backend/local_llm.py` - Runs TinyLlama LLM locally
- `backend/hybrid_transcriber.py` - Auto-switches between local/API Whisper
- `backend/hybrid_notes.py` - Auto-switches between local/API LLM

### Updated Dependencies:
- `backend/requirements-server.txt` - Added torch, transformers, openai-whisper

## System Requirements

### Disk Space:
- PyTorch + dependencies: ~2-3 GB
- Whisper base model: ~74 MB
- TinyLlama-1.1B: ~1.1 GB
- **Total: ~4-5 GB**

### RAM Requirements:
- Whisper base transcription: ~500 MB
- TinyLlama inference: ~1.5 GB
- **Total: ~2 GB minimum**

## Render Deployment Options

### Option 1: Render Free Tier ❌
- 512 MB RAM
- **Won't work** - not enough memory

### Option 2: Render Starter ($7/mo) ❌
- 512 MB RAM
- **Won't work** - still not enough

### Option 3: Render Standard ($25/mo) ✅
- 2 GB RAM
- **Will work** - just enough for both models
- Models re-download on each deploy (ephemeral storage)

### Option 4: Render Pro ($85/mo) ✅
- 4 GB RAM
- **Comfortable** - plenty of headroom
- Can add persistent disk to cache models

## Hybrid Approaches (Cheaper)

### Approach A: Local Whisper + GPT API
- Use local Whisper (free transcription)
- Use GPT-4 API only for flashcard generation
- **Cost:** Pay per flashcard generation (~$0.01-0.03 per video)
- **Render:** Can run on Starter tier ($7/mo)

### Approach B: Whisper API + Local LLM
- Use Whisper API for transcription (~$0.006/minute)
- Use local LLM for flashcards (free)
- **Cost:** Pay per transcription minute
- **Render:** Standard tier ($25/mo) for LLM

### Approach C: Both APIs (Current)
- Use Whisper API + GPT-4 API
- **Cost:** ~$0.01-0.05 per video
- **Render:** Free tier works
- **Issue:** Need API keys

## Recommendation

**For Your Situation (No API Keys):**

1. **Short term:** Get a cheap OpenAI API key
   - $5 credit lasts for hundreds of videos
   - Much cheaper than $25/mo Render plan
   - Can still use Free tier Render

2. **Long term (if you process lots of videos):**
   - Upgrade to Render Standard ($25/mo)
   - Run both models locally
   - Zero per-video costs

## Cost Comparison

**Example: 100 videos/month, 10 min each**

### Using APIs:
- Whisper: 1000 min × $0.006 = $6
- GPT-4: 100 calls × $0.02 = $2
- **Total: $8/mo** (plus Render Free tier)

### Using Local Models:
- Render Standard: $25/mo
- Processing: $0
- **Total: $25/mo**

### Breakeven: ~300 videos/month

If you process fewer than 300 videos per month, APIs are cheaper.
If you process more, local models become cost-effective.

## How to Deploy

### If Using APIs (Recommended):
1. Get OpenAI API key ($5 minimum)
2. Add to Render environment: `OPENAI_API_KEY`
3. Deploy current code (already on Render)
4. Uses Free tier

### If Using Local Models:
1. Upgrade Render to Standard plan ($25/mo)
2. Deploy current code (auto-detects no API key)
3. First deploy will be slow (downloading models)
4. Models re-download on each deploy

## Next Steps

**What would you prefer?**

A. Get a $5 OpenAI API key and keep using Free tier
B. Upgrade to Render Standard ($25/mo) and run everything locally
C. Use hybrid approach (local Whisper + GPT API)

Let me know and I'll help you set it up!
