# Deploy Lead Tracker to GitHub + Streamlit Cloud

## Step 1: Create GitHub Repository (2 minutes)

1. Go to **https://github.com/new**
2. Repository name: `lead-tracker`
3. Description: `Lead management dashboard with Streamlit`
4. Make it **Public** (required for free Streamlit Cloud deployment)
5. Click **Create repository**

You'll get a URL like: `https://github.com/YOUR_USERNAME/lead-tracker`

---

## Step 2: Push Code to GitHub (3 minutes)

In your project folder (`C:\DecisionAnalytics\ShinyAppExamples\LeadGenerator`):

```bash
# Initialize git repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Lead Tracker MVP"

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/lead-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub.

---

## Step 3: Deploy to Streamlit Cloud (2 minutes)

1. Go to **https://streamlit.io/cloud**
2. Click **"New app"**
3. Sign in with GitHub (it will ask for permission)
4. Select:
   - **Repository:** `YOUR_USERNAME/lead-tracker`
   - **Branch:** `main`
   - **Main file path:** `app_python.py`
5. Click **Deploy**

**That's it!** Your app is live at:
```
https://lead-tracker-RANDOMSTRING.streamlit.app/
```

---

## Step 4: Share Your App

Copy the URL and share it! Your team can use it immediately with no installation.

---

## Files That Got Pushed to GitHub

```
lead-tracker/
├── app_python.py           ✅ Main Streamlit app
├── requirements.txt        ✅ Dependencies
├── leads.db               ✅ SQLite database (auto-created)
├── .gitignore            ✅ Tells git what to skip
└── README_PYTHON.md      ✅ Documentation
```

---

## What Your App Can Do

- ✅ **Add leads** — 30-second form
- ✅ **View all leads** — Search & filter
- ✅ **See dashboard** — Key metrics
- ✅ **Analytics** — Charts & insights
- ✅ **Download CSV** — Export anytime
- ✅ **Data persists** — SQLite keeps everything

---

## Troubleshooting

### "git: command not found"
Install Git from https://git-scm.com/download/win

### "Permission denied" when pushing
Make sure you're using HTTPS URL, not SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/lead-tracker.git
```

### Streamlit app shows error
1. Check the app logs (Streamlit Cloud dashboard)
2. Make sure `requirements.txt` has all dependencies
3. Verify `app_python.py` is the correct filename

### "leads.db not found"
- Database auto-creates on first run
- It gets saved in Streamlit Cloud
- Data persists across reloads

---

## Next Steps

1. **Test locally first:**
   ```bash
   streamlit run app_python.py
   ```

2. **Push to GitHub** (follow Step 2 above)

3. **Deploy to Streamlit Cloud** (follow Step 3 above)

4. **Share the URL** with your team!

---

## Upgrade Options (Later)

When you're ready:
- **Add PostgreSQL** for scaling (Supabase, Railway)
- **Add email reminders** (SendGrid)
- **Add authentication** (Streamlit Enterprise)
- **Custom domain** (Streamlit Cloud supports this)

---

## Your Live App URL Format

Once deployed, your app will be at:
```
https://lead-tracker-YOURUSERNAME.streamlit.app/
```

Share this with anyone — no installation needed! 🎉
