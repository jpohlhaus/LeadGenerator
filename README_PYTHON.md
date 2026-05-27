# Lead Tracker MVP (Python/Streamlit)

> An automated lead management dashboard built with Python that helps small businesses stop losing customers

## 🎯 The Problem

From analyzing **5,642 Reddit pain points**, the #1 automation opportunity is **Lead Management**:

- **739 mentions** of marketing/leads being a challenge
- **467 mentions** of manual, time-consuming work
- **366 mentions** of expensive marketing campaigns
- **Small teams losing track** of leads and missing follow-ups

## ✨ The Solution

**Lead Tracker** is a web dashboard that automates lead management for small businesses.

Instead of juggling spreadsheets, emails, and calendar reminders, teams now have:
- **One central database** for all leads (with data persistence!)
- **Automatic scoring** to identify hot prospects
- **Follow-up reminders** so no lead falls through the cracks
- **Analytics** to see which channels bring the best customers
- **Time savings:** 2-3 hours/week managing leads manually

---

## 🚀 Quick Start (Choose One)

### Option 1: Run Locally (30 seconds)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_python.py
```

Opens automatically at `http://localhost:8501` ✨

### Option 2: Deploy to Streamlit Cloud (FREE, 2 minutes)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" → Select your repo
4. **DONE!** Your app is live

See `PYTHON_DEPLOYMENT.md` for detailed instructions.

---

## 📊 Features

### Dashboard
- Real-time metrics (total leads, hot leads, due today)
- Status distribution chart
- Lead source analytics
- 7-day upcoming follow-ups

### Lead Management
- Add new leads in seconds
- Auto-calculate lead score (0-100)
- Set status (Hot/Warm/Cold)
- Track last contact & next follow-up
- Store custom notes

### Analytics
- Lead quality distribution
- Conversion funnel breakdown
- Lead age vs. quality scatter plot
- Source performance tracking

### Database
- **SQLite persistence** (data doesn't disappear!)
- Searchable lead table
- Sort by any field
- Filter by status/source
- Export to CSV

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **Language** | Python 3.9+ |
| **Data** | Pandas |
| **Database** | SQLite |
| **Charts** | Plotly |
| **Deployment** | Streamlit Cloud / Heroku / Self-hosted |

---

## 📁 File Structure

```
lead-tracker/
├── app_python.py              # Main Streamlit app (single file!)
├── requirements.txt           # Python dependencies
├── leads.db                   # SQLite database (auto-created)
├── PYTHON_DEPLOYMENT.md      # Deployment guide
├── README_PYTHON.md          # This file
└── USING_THE_APP.md          # User guide
```

---

## 🎯 Sample Data

The app comes with 5 starter leads:
- Acme Corp (Hot, score: 85)
- TechStart Inc (Warm, score: 72)
- Local Bakery (Cold, score: 45)
- Design Studio (Hot, score: 90)
- Consulting Group (Warm, score: 68)

**Add your own** via the "Add Lead" tab.

---

## 📈 Impact

**Time Saved:**
- ⏱️ Manual data entry: **2-3 hrs/week**
- ⏱️ Searching for leads: **30 min/week**
- ⏱️ Follow-up reminders: **45 min/week**

**Total: ~3-4 hours/week** (150+ hours/year)

**Revenue Impact:**
- If that 3-4 hours/week leads to **1 extra deal/month**
- At **$5K average deal** = **$60K/year** additional revenue
- ROI: **Infinite** (costs $0 to deploy on free tier)

---

## 🎓 Addressing Reddit Pain Points

| Pain Point | How We Solve It |
|-----------|-----------------|
| "Marketing is expensive" | Track which channels bring best leads → focus budget there |
| "Can't find customers" | Centralized database ensures no lead is lost |
| "Manual work is killing me" | Automate scoring, follow-ups, reminders |
| "Don't have time" | Dashboard gives 30-sec overview of what's urgent |
| "Customers keep slipping away" | Follow-up reminders + next action tracking |

---

## 💡 MVP Scope

**What's Included:**
✅ Lead database with scoring  
✅ Follow-up tracking  
✅ Status classification  
✅ Basic analytics  
✅ Dashboard & charts  
✅ SQLite persistence  
✅ Ready to deploy  

**What's Next (Phase 2+):**
⏳ PostgreSQL for scaling  
⏳ Email integration  
⏳ Bulk import from Excel  
⏳ Team collaboration features  
⏳ Automated email templates  
⏳ SMS reminders  
⏳ ML-based lead scoring  

---

## 🚢 Deployment Options

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Streamlit Cloud** | Free | 2 min | MVP/testing ⭐ |
| **Heroku** | $5+/mo | 10 min | Small teams |
| **Self-hosted** | $5-20/mo | 30 min | Full control |
| **Docker** | $10-50/mo | 20 min | Scalability |

**Recommendation for MVP:** Start **FREE on Streamlit Cloud**, upgrade when you outgrow it.

---

## 🔄 User Workflow

```
1. New lead comes in (website form, referral, cold outreach)
   ↓
2. Click "Add Lead" → Fill form (30 seconds)
   ↓
3. System saves to database + sets 2-day follow-up
   ↓
4. View dashboard → Prioritize hot leads
   ↓
5. Analytics show which sources bring best leads
   ↓
6. Next day: Get notified of leads needing follow-up
   ↓
7. Close deal or move to next stage
```

---

## 📊 Why Python > R for This?

| Aspect | Python | R |
|--------|--------|---|
| Deployment | Easier (Streamlit Cloud) | Harder (shinyapps.io) |
| Data Persistence | SQLite included | Requires setup |
| Learning Curve | Easier | Moderate |
| Data Import | Pandas (excellent) | Base R (OK) |
| Production Ready | Yes | Yes |
| Developer Community | Larger | Smaller |

**TL;DR:** Python Streamlit = easier to deploy, built-in database, larger community.

---

## 🛠️ Customization

### Change Colors
```python
color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'}
```

### Add Custom Fields
Edit the `CREATE TABLE` SQL:
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leads (
        ...
        custom_field TEXT,  # Add this
        ...
    )
''')
```

### Change Scoring Logic
```python
# Add automatic scoring based on lead age
if days_since < 3:
    score += 10
```

---

## 📝 License

This MVP is provided as-is for deployment and customization.

---

## 🎉 Next Steps

1. **Test locally:**
   ```bash
   pip install -r requirements.txt
   streamlit run app_python.py
   ```

2. **Deploy free:**
   - Push to GitHub
   - Sign up at https://streamlit.io/cloud
   - Deploy in 2 minutes

3. **Add your leads:**
   - Click "Add Lead" tab
   - Start building your pipeline

4. **Share with team:**
   - Everyone gets the same URL
   - Real-time updates
   - No installation needed

---

## 📚 Documentation

- **PYTHON_DEPLOYMENT.md** — Step-by-step deployment guide
- **USING_THE_APP.md** — How to use each feature
- **app_python.py** — Full source code (600 lines, well-commented)

---

**Ready to deploy?** See `PYTHON_DEPLOYMENT.md` for next steps! 🚀

Questions? Check out Streamlit docs at https://docs.streamlit.io
