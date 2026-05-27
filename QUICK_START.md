# Quick Start Guide - Lead Tracker Python MVP

**TL;DR:** 30 seconds to run locally, 2 minutes to deploy free.

---

## 🚀 Run Locally (30 seconds)

```bash
pip install -r requirements.txt
streamlit run app_python.py
```

That's it! Opens at `http://localhost:8501`

---

## 🌐 Deploy Free (2 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Add Lead Tracker MVP"
git remote add origin https://github.com/YOUR_USERNAME/lead-tracker.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repo
4. Select `app_python.py` as main file
5. Click "Deploy"

**Your app is now live!** 🎉

---

## 📦 What's Included

| File | Purpose |
|------|---------|
| `app_python.py` | Main Streamlit app (all-in-one file) |
| `requirements.txt` | Python dependencies |
| `leads.db` | SQLite database (auto-created) |
| `PYTHON_DEPLOYMENT.md` | Detailed deployment guide |
| `README_PYTHON.md` | Full documentation |
| `USING_THE_APP.md` | How to use the app |

---

## ✨ Features at a Glance

✅ **Dashboard** - See leads at a glance  
✅ **Add Leads** - Quick form (30 sec per lead)  
✅ **Lead Database** - Search, filter, sort  
✅ **Analytics** - Visualizations & trends  
✅ **Data Persistence** - SQLite stores everything  
✅ **Mobile Friendly** - Works on phones  

---

## 🎯 Common Tasks

### Add a Lead
1. Click "Add Lead" tab
2. Fill form (Company, Email, Source, Score, Status)
3. Click "✅ Add Lead"

### View All Leads
1. Click "All Leads" tab
2. Filter by Status or Source
3. Click columns to sort

### Check Analytics
1. Click "Analytics" tab
2. See score distribution
3. View lead age vs quality

### Export Leads
1. Go to "All Leads" tab
2. Click "📥 Download as CSV"
3. Open in Excel/Google Sheets

---

## 🔧 Deployment Comparison

| Method | Cost | Time | Best For |
|--------|------|------|----------|
| **Streamlit Cloud** | Free | 2 min | MVP ⭐ |
| **Heroku** | $5+/mo | 10 min | Small teams |
| **Self-hosted** | $5-20/mo | 30 min | Control |

**Start with Streamlit Cloud!** Upgrade later if needed.

---

## 🆘 Troubleshooting

### "Command not found: streamlit"
```bash
pip install streamlit
```

### "Port 8501 already in use"
```bash
streamlit run app_python.py --server.port 8502
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Database locked"
- Refresh the page
- If on Streamlit Cloud, it's normal. Just restart.

---

## 📊 Next Steps

**Phase 2 Ideas:**
- Upgrade to PostgreSQL for multi-user
- Add email reminders via SendGrid
- Import leads from CSV
- Team collaboration features
- Predictive lead scoring

---

## 🎓 Learning Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Pandas Guide:** https://pandas.pydata.org/docs/
- **Plotly Charts:** https://plotly.com/python/
- **SQLite Tutorial:** https://www.sqlite.org/docs.html

---

## 💡 Pro Tips

### Tip 1: Use Virtual Environments
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Tip 2: Track Database Changes
```bash
# See all leads
sqlite3 leads.db "SELECT * FROM leads;"

# Export data
sqlite3 leads.db ".mode csv" ".output leads.csv" "SELECT * FROM leads;"
```

### Tip 3: Customize Colors
Edit `app_python.py`, find:
```python
color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'}
```

Change hex codes to your brand colors.

### Tip 4: Add Custom Fields
1. Edit `CREATE TABLE` in `init_sample_data()`
2. Add new columns to add lead form
3. Add to display tables
4. Restart app

---

## 📈 Success Metrics

Once deployed, track:
- ✅ Leads added per week
- ✅ Hot lead % (aim for 30%+)
- ✅ Follow-up completion rate
- ✅ Average lead score trending up
- ✅ Hours saved per week

---

## 🎉 You're Ready!

1. Run locally: `streamlit run app_python.py`
2. Test the features
3. Deploy: Push to GitHub → Streamlit Cloud
4. Share URL with your team
5. Start tracking leads!

**Questions?** See `PYTHON_DEPLOYMENT.md` or `README_PYTHON.md`

Happy tracking! 🚀
