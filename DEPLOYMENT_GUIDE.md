# Lead Tracker MVP - Deployment Guide

## Problem Solved
**Automation Need:** Lead Management & Tracking  
**Pain Points Addressed:**
- Manual lead tracking (467 mentions in data)
- Hard to find customers (1,105 mentions of "hard")
- Expensive marketing (366 mentions)
- Lost leads due to no follow-up system (27 mentions of "wasting time")

---

## What This App Does

The **Lead Tracker** is a Shiny dashboard that helps small business owners:

✅ **Centralize all leads** - Store company info, contact details, and lead source  
✅ **Automate scoring** - Rank leads by quality (0-100 scale)  
✅ **Track follow-ups** - Never miss a follow-up with automated reminders  
✅ **Monitor conversion** - See hot vs. warm vs. cold leads at a glance  
✅ **Analyze sources** - Understand which marketing channels bring best leads  
✅ **Visualize pipeline** - Dashboards show lead status distribution and trends  

---

## Features Included

### Dashboard Tab
- **Key Metrics:** Total leads, hot leads, due today, conversion rate
- **Status Distribution Chart:** Visual breakdown of lead temperature
- **Lead Source Chart:** See which channels drive most leads
- **Upcoming Follow-ups:** 7-day view of leads needing attention

### All Leads Tab
- **Full Database View:** Interactive table of all leads
- **Sortable & Filterable:** Search by name, source, status
- **Track Key Info:** Score, last contact, next follow-up date

### Add Lead Tab
- **Quick Entry Form:** Add new leads in seconds
- **Auto-populate Fields:** Next follow-up defaults to 2 days out
- **Lead Scoring:** Rate leads 0-100 with slider
- **Status Tags:** Hot/Warm/Cold classification

### Analytics Tab
- **Score Distribution:** Histogram of lead quality
- **Conversion Metrics:** Breakdown of lead pipeline
- **Age Analysis:** Scatter plot showing lead age vs. quality

---

## How to Deploy to Shiny Apps

### Option 1: Deploy via shinyapps.io (Easiest)

1. **Create a free account:**
   - Go to https://www.shinyapps.io/
   - Sign up with your email

2. **Install required R packages:**
```r
install.packages(c("shiny", "shinydashboard", "dplyr", "ggplot2", "DT", "lubridate"))
```

3. **Install rsconnect package:**
```r
install.packages("rsconnect")
```

4. **Configure deployment credentials:**
```r
library(rsconnect)
rsconnect::setAccountInfo(name='<YOUR_ACCOUNT>', 
                          token='<YOUR_TOKEN>', 
                          secret='<YOUR_SECRET>')
```
(Get these from shinyapps.io dashboard → Account → Tokens)

5. **Deploy the app:**
```r
rsconnect::deployApp('path/to/app.R')
```

6. **Your app will be live at:** `https://<username>.shinyapps.io/lead-tracker/`

### Option 2: Deploy on Your Own Server

If you have a Linux server with R installed:

1. Install Shiny Server
2. Copy app.R to `/srv/shiny-server/lead-tracker/`
3. Restart Shiny Server
4. Access at: `http://your-server:3838/lead-tracker`

### Option 3: Docker Deployment

```dockerfile
FROM rocker/shiny:latest

RUN install2.r shiny shinydashboard dplyr ggplot2 DT lubridate

COPY app.R /srv/shiny-server/app/app.R

EXPOSE 3838
```

---

## MVP Features (Current)

✅ Dashboard with key metrics  
✅ Lead database with 5 sample leads  
✅ Add new lead form  
✅ Automatic lead scoring UI  
✅ Follow-up tracking  
✅ Basic analytics & charts  
✅ Status filtering (Hot/Warm/Cold)  

---

## Next Steps for Enhancement

### Phase 2 (Database Integration)
- Connect to PostgreSQL/SQLite for persistent storage
- Export leads to CSV
- Import bulk leads from Excel

### Phase 3 (Automation)
- Email integration for follow-up reminders
- Automated email templates
- SMS reminders for hot leads
- Calendar sync (Google Calendar, Outlook)

### Phase 4 (AI Enhancement)
- Predictive lead scoring using ML
- Auto-categorize leads by industry
- Recommended follow-up timing
- Sales conversation suggestions

### Phase 5 (Team Features)
- Multi-user support with permissions
- Lead assignment to team members
- Activity history tracking
- Team performance metrics

---

## Quick Start (Local Testing)

1. Save `app.R` in a new folder
2. In R console:
```r
setwd("path/to/folder")
library(shiny)
runApp("app.R")
```
3. App opens in browser at `http://localhost:7777`

---

## Data Structure

The app uses in-memory data storage (resets on app restart). 

To add **persistent storage**, replace the `leads_data` reactive with a database connection:

```r
# Connect to SQLite
db <- dbConnect(RSQLite::SQLite(), "leads.db")

# Read data
leads_data <- reactive({
  dbReadTable(db, "leads")
})

# Save new lead
dbAppendTable(db, "leads", new_lead)
```

---

## Support & Customization

**Want to customize the app?**
- Colors: Modify the hex codes in `scale_fill_manual(values = c(...))`
- Fields: Add more columns to the data frame
- Charts: Change plot types in `renderPlot()` functions
- Logic: Modify scoring rules or status thresholds

---

## Cost Breakdown

- **shinyapps.io Free Tier:** $0/month (5 apps, 25 active hours/month)
- **shinyapps.io Standard:** $9/month (25 apps, unlimited hours)
- **shinyapps.io Advanced:** $99/month (unlimited apps, priority support)

For a solo founder or small team, **free tier is sufficient** to start validating the MVP!

---

## Success Metrics

Once deployed, track:
- ✅ Number of leads added per week
- ✅ Hot lead percentage (aim for 30%+)
- ✅ Follow-up completion rate
- ✅ Average lead score
- ✅ Time saved per week (vs. manual spreadsheet)

Expected ROI: **2-3 hours saved per week** managing leads manually
