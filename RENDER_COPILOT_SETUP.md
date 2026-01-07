# 🚀 Deploying FastScribe with Copilot API to Render

This guide shows you how to deploy the fully automated, free flashcard generator to Render.

## 🔑 Prerequisites

1. **GitHub Copilot Account** with active subscription (free for students)
2. **Copilot Token** - You need to authenticate locally first
3. **Render Account** (free tier works!)

## 📋 Step 1: Get Your Copilot Token

You've already done this locally! The token is in:
```
C:\Users\Daniel Thomas\4Cheych\copilot-api\.copilot_token
```

**Read the token:**
```powershell
Get-Content "C:\Users\Daniel Thomas\4Cheych\copilot-api\.copilot_token"
```

Copy the entire token string (it's a long alphanumeric string).

## 🔐 Step 2: Add Token to Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Select your **FastScribe** service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   - **Key**: `COPILOT_TOKEN`
   - **Value**: Paste the token you copied
6. Click **Save Changes**

## 📦 Step 3: Update Render Configuration

The `render.yaml` and `start.sh` are already configured! Here's what they do:

### render.yaml
- Builds the app with all dependencies
- Runs `start.sh` to launch both services

### start.sh
- Clones copilot-api repository
- Creates `.copilot_token` from environment variable
- Starts copilot-api on port 8080 (background)
- Starts Flask app with Gunicorn (foreground)

## 🚀 Step 4: Deploy to Render

### Option A: Push to GitHub (Auto-Deploy)
```powershell
cd "C:\Users\Daniel Thomas\4Cheych"
git add .
git commit -m "Add copilot-api integration for free flashcard generation"
git push origin main
```

Render will automatically detect the changes and deploy!

### Option B: Manual Deploy
1. Go to Render dashboard
2. Select your service
3. Click **Manual Deploy** → **Deploy latest commit**

## ⏳ Step 5: Monitor Deployment

Watch the deployment logs in Render. You should see:
```
🚀 Starting FastScribe with Copilot API integration...
✅ Copilot token found
🔧 Starting Copilot API server on port 8080...
⏳ Waiting for Copilot API to be ready...
✅ Copilot API is running (PID: 1234)
🌐 Starting Flask app with Gunicorn...
```

## ✅ Step 6: Test the Deployment

Once deployed, test the API:

```powershell
# Test Copilot API is working
$url = "https://fastscribe-4nzr.onrender.com/api/process-complete"
$body = @{
    video_url = "https://youtube.com/watch?v=SHORT_VIDEO"
    language = "English"
} | ConvertTo-Json

Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"
```

## 🔧 Troubleshooting

### "No COPILOT_TOKEN environment variable found"
- Make sure you added the token to Render's environment variables
- Redeploy after adding the variable

### "Copilot API failed to start"
- Check if the token is valid (they expire after some time)
- Re-authenticate locally and upload new token

### "Could not connect to Copilot API"
- The copilot-api might be taking longer to start
- Increase sleep time in `start.sh` (change `sleep 5` to `sleep 10`)

### Token Expired
If your Copilot token expires:
1. Run locally: `cd copilot-api && python api.py 8080`
2. Re-authenticate when prompted
3. Copy the new token from `.copilot_token`
4. Update the `COPILOT_TOKEN` variable on Render
5. Redeploy

## 💰 Cost Analysis

| Component | Monthly Cost |
|-----------|--------------|
| Render Free Tier | **$0** |
| Copilot API (Student) | **$0** |
| Local Whisper | **$0** |
| **Total** | **$0** |

## 🎯 How It Works in Production

```
User Request
    ↓
Render Web Service
    ↓
Flask App (port from $PORT env var)
    ↓
Local Whisper Transcription
    ↓
Copilot API (localhost:8080)
    ↓
GPT-4 Flashcard Generation
    ↓
Return to User
```

## 🔄 Updating the Token

Copilot tokens refresh every 25 minutes automatically when the server is running. However, if the server restarts, it needs the original GitHub access token to refresh.

**Best Practice:**
- The `.copilot_token` file contains the ACCESS TOKEN (not the API token)
- This token is longer-lived and can refresh the API tokens
- Update it only when you get authentication errors

## 🚨 Important Notes

1. **Token Security**: The Copilot token is sensitive! Never commit it to Git
2. **Render Free Tier**: Spins down after inactivity, first request may be slow
3. **Memory**: Whisper base model + Copilot API fits in 512MB RAM (free tier)
4. **Timeout**: Set Gunicorn timeout to 120s for longer transcriptions

## 🎓 For Students

This setup gives you:
- ✅ Unlimited free GPT-4 flashcard generation
- ✅ Free hosting on Render
- ✅ No API costs ever
- ✅ Professional-grade app

Perfect for study tools without spending money!

## 📝 Alternative: Render Secret Files (More Secure)

Instead of environment variables, you can use Render Secret Files:

1. Go to Render dashboard → Your service → **Environment**
2. Scroll to **Secret Files**
3. Add new secret file:
   - **Filename**: `/etc/secrets/copilot_token`
   - **Contents**: Paste your token
4. Update `start.sh` to read from `/etc/secrets/copilot_token`

This is more secure as the token isn't visible in environment variables.

## 🔮 Next Steps

- [ ] Set up automatic token refresh mechanism
- [ ] Add health check endpoint for copilot-api
- [ ] Monitor token expiration and send alerts
- [ ] Add rate limiting for free tier protection

---

**You're now running a 100% free, GPT-4 powered flashcard generator in the cloud! 🎉**
