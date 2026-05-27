# Lead Tracker MVP

> An automated lead management dashboard that helps small businesses stop losing customers

## 🎯 The Problem

From analyzing **5,642 Reddit pain points**, the #1 automation opportunity is **Lead Management**:

- **739 mentions** of marketing/leads being a challenge
- **467 mentions** of manual, time-consuming work
- **366 mentions** of expensive marketing campaigns
- **Small teams losing track** of leads and missing follow-ups

## ✨ The Solution

**Lead Tracker** is a web dashboard that automates lead management for small businesses.

Instead of juggling spreadsheets, emails, and calendar reminders, teams now have:
- **One central database** for all leads
- **Automatic scoring** to identify hot prospects
- **Follow-up reminders** so no lead falls through the cracks
- **Analytics** to see which channels bring the best customers
- **Time savings:** 2-3 hours/week managing leads manually

---

## 🚀 Quick Start

### Run Locally
```r
# Install packages
install.packages(c("shiny", "shinydashboard", "dplyr", "ggplot2", "DT", "lubridate"))

# Run the app
library(shiny)
runApp("app.R")
```

### Deploy to Shiny Apps (Free)
```r
install.packages("rsconnect")
rsconnect::setAccountInfo(name='YOUR_NAME', token='YOUR_TOKEN', secret='YOUR_SECRET')
rsconnect::deployApp('app.R')
```

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

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
- Searchable lead table
- Sort by any field
- Filter by status/source
- Export ready (ready for Phase 2)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | R Shiny |
| **UI** | Shiny Dashboard |
| **Data** | In-memory (R data frames) |
| **Plotting** | ggplot2 |
| **Tables** | DT (DataTables) |
| **Deployment** | Shiny Apps / Self-hosted |

---

## 📈 Sample Data

Includes 5 starter leads:
- Acme Corp (Hot lead, score: 85)
- TechStart Inc (Warm lead, score: 72)
- Local Bakery (Cold lead, score: 45)
- Design Studio (Hot lead, score: 90)
- Consulting Group (Warm lead, score: 68)

**Add your own** via the "Add Lead" tab.

---

## 🔄 User Workflow

```
1. New lead comes in (website form, referral, cold outreach)
   ↓
2. Click "Add Lead" → Fill form (30 seconds)
   ↓
3. System calculates score & sets 2-day follow-up reminder
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

## 💡 MVP Scope

**What's Included:**
✅ Lead database with scoring  
✅ Follow-up tracking  
✅ Status classification  
✅ Basic analytics  
✅ Dashboard & charts  
✅ Ready to deploy  

**What's Next (Phase 2+):**
⏳ SQLite/PostgreSQL persistence  
⏳ Email integration  
⏳ Bulk import from Excel  
⏳ Team collaboration features  
⏳ Automated email templates  
⏳ SMS reminders  
⏳ ML-based lead scoring  

---

## 📊 Impact

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

## 📁 Files

- **app.R** - Main Shiny application
- **DEPLOYMENT_GUIDE.md** - Step-by-step deployment instructions
- **README.md** - This file

---

## 🚢 Deployment Options

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Shiny Apps Free** | $0/mo | 5 min | Testing, single user |
| **Shiny Apps Paid** | $9-99/mo | 5 min | Production, team use |
| **Self-hosted (Linux)** | $5-20/mo | 30 min | Full control |
| **Docker/Cloud** | $10-50/mo | 1 hour | Scalability |

**Recommendation for MVP:** Start free on shinyapps.io, upgrade to $9/mo when ready.

---

## 📞 Support

Need help? Check:
1. `DEPLOYMENT_GUIDE.md` for deployment issues
2. R Shiny docs: https://shiny.posit.co/
3. Shiny Dashboard: https://rstudio.github.io/shinydashboard/

---

## 📝 License

This MVP is provided as-is for deployment and customization.

---

**Ready to deploy?** See `DEPLOYMENT_GUIDE.md` for next steps! 🚀
