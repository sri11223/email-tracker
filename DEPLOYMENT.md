# Email Tracker Deployment Guide

## 🚀 Deploy to Render.com (FREE - Recommended)

### Steps:

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Push Code to GitHub**
   ```bash
   cd d:\read-gmail\email-tracker
   git add .
   git commit -m "Ready for deployment"
   git push origin master
   ```

3. **Create New Web Service on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `atharva-vyas/email-tracker`
   - Configure:
     - **Name**: email-tracker
     - **Root Directory**: `server`
     - **Environment**: Node
     - **Build Command**: `npm install`
     - **Start Command**: `node index.js`
     - **Instance Type**: Free

4. **Add Environment Variables**
   - In Render dashboard, go to "Environment"
   - Add:
     - Key: `MONGODB_URI`
     - Value: `mongodb+srv://nutalapatisrikrishna85_db_user:HCTWIjyXhobFdhgT@cluster0.mzatzvb.mongodb.net/?appName=Cluster0`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - You'll get a URL like: `https://email-tracker-xxxx.onrender.com`

6. **Update main.py**
   - Replace the URL in `main.py`:
   ```python
   url = 'https://email-tracker-xxxx.onrender.com/'
   ```

---

## 🔥 Deploy to Railway.app (Alternative - Also FREE)

### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `atharva-vyas/email-tracker`
   - Railway auto-detects Node.js

3. **Configure**
   - Add environment variable:
     - `MONGODB_URI` = `mongodb+srv://nutalapatisrikrishna85_db_user:HCTWIjyXhobFdhgT@cluster0.mzatzvb.mongodb.net/?appName=Cluster0`
   - Set root directory: `server`

4. **Generate Domain**
   - Go to Settings → Generate Domain
   - You'll get: `https://xxxx.up.railway.app`

5. **Update main.py with your Railway URL**

---

## ⚡ Deploy to Vercel (Serverless)

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd d:\read-gmail\email-tracker\server
   vercel
   ```

3. **Add Environment Variables**
   ```bash
   vercel env add MONGODB_URI
   ```
   Paste: `mongodb+srv://nutalapatisrikrishna85_db_user:HCTWIjyXhobFdhgT@cluster0.mzatzvb.mongodb.net/?appName=Cluster0`

4. **You'll get a URL**: `https://email-tracker-xxxx.vercel.app`

---

## 🧪 Quick Test with ngrok (Local Testing)

### If you want to test before deploying:

1. **Download ngrok**: https://ngrok.com/download
2. **Run your server**: `node index.js`
3. **In another terminal**:
   ```bash
   ngrok http 3000
   ```
4. **You'll get a temporary URL**: `https://xxxx.ngrok.io`
5. **Update main.py** with this URL (valid for 2 hours on free plan)

---

## 📝 After Deployment

1. Get your deployed URL (e.g., `https://email-tracker-xxxx.onrender.com`)
2. Update `main.py`:
   ```python
   url = 'https://your-deployed-url.com/'
   ```
3. Create new tracking URLs
4. Use them in emails - they'll work from anywhere!

---

## ⚠️ Important Notes

- **Free tiers** may sleep after inactivity (takes 30 sec to wake up)
- **Render Free**: Best option, always-on for first month
- **Railway Free**: $5 credit/month
- **Vercel**: Good for serverless, some limitations with long-running connections

**Recommended: Start with Render.com - easiest setup!**
