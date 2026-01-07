# 🎉 Quick Deploy Guide - FastScribe with Free Copilot API

## 🚀 Deploy in 3 Easy Steps!

### Step 1: Get Your Copilot Token (30 seconds)

```powershell
# Read your token
Get-Content "C:\Users\Daniel Thomas\4Cheych\copilot-api\.copilot_token"
```

Copy the entire token (it's a long string starting with "ghu_" or similar).

### Step 2: Add to Render (2 minutes)

1. Go to: https://dashboard.render.com/web/srv-YOUR-SERVICE-ID/env
2. Click **Add Environment Variable**
3. Add:
   - **Key**: `COPILOT_TOKEN`
   - **Value**: [Paste the token]
4. **Save Changes**

### Step 3: Deploy (1 command)

```powershell
cd "C:\Users\Daniel Thomas\4Cheych"

git add .
git commit -m "Add free Copilot API integration - $0/month solution!"
git push origin main
```

**That's it!** Render will auto-deploy in ~5 minutes.

## ✅ What You Get

- ✅ **Free Hosting** on Render
- ✅ **Free GPT-4** via your student Copilot account
- ✅ **Free Transcription** with local Whisper
- ✅ **$0/month** total cost
- ✅ **Unlimited usage** (no rate limits!)

## 🔍 Check Deployment Status

Watch at: https://dashboard.render.com/web/srv-YOUR-SERVICE-ID/deploys

You should see:
```
🚀 Starting FastScribe with Copilot API integration...
✅ Copilot token found
🔧 Starting Copilot API server on port 8080...
✅ Copilot API is running
🌐 Starting Flask app with Gunicorn...
```

## 🧪 Test It

```powershell
# Test the free endpoint
Invoke-RestMethod -Uri "https://fastscribe-4nzr.onrender.com/api/process-free" `
  -Method Post `
  -Body (@{
    url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    language = "English"
  } | ConvertTo-Json) `
  -ContentType "application/json"
```

## 🎯 API Endpoints

### FREE Endpoint (Recommended)
**POST** `/api/process-free`
- Uses local Whisper + Copilot API
- $0 cost
- No API keys needed

```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "language": "English"
}
```

### Standard Endpoint (Requires OpenAI API)
**POST** `/api/process-complete`
- Uses OpenAI Whisper API + GPT-4 API
- Costs money
- Requires OPENAI_API_KEY

## ⚠️ Troubleshooting

### "Free processing not available"
- Check if `COPILOT_TOKEN` env var is set on Render
- Redeploy after adding the variable

### "Could not connect to Copilot API"
- copilot-api might still be starting
- Wait 30 seconds and try again
- Check deployment logs for errors

### First request is slow
- Render free tier spins down after inactivity
- First request wakes it up (~30-60 seconds)
- Subsequent requests are fast!

## 💡 Pro Tips

1. **Keep a backup of your token** - save it somewhere safe
2. **Monitor usage** - check Render logs occasionally
3. **Use the free endpoint** - `/api/process-free` for $0 costs
4. **Bookmark the deployment logs** - helpful for debugging

## 🎓 Perfect for Students

This setup is designed for students who:
- ✅ Have GitHub Copilot Pro (free with student account)
- ✅ Want unlimited flashcard generation
- ✅ Don't want to pay for APIs
- ✅ Need a reliable, cloud-hosted solution

Total cost: **$0 per month** 🎉

---

**Next**: Check [RENDER_COPILOT_SETUP.md](RENDER_COPILOT_SETUP.md) for detailed troubleshooting
