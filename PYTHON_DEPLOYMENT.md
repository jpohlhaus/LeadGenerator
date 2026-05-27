# Lead Tracker MVP - Python/Streamlit Deployment Guide

## What's Different from R?

This Python version uses **Streamlit** instead of Shiny. Both are dashboard frameworks, but:

| Feature | Streamlit | Shiny |
|---------|-----------|-------|
| Language | Python | R |
| Deployment | Streamlit Cloud (easiest) | shinyapps.io |
| Setup Complexity | ~1 minute | ~5 minutes |
| Data Storage | SQLite (included) | In-memory or database |
| Learning Curve | Very easy | Easy |
| Production Ready | Yes | Yes |

**Bottom line:** This Python version is actually **easier to deploy** and includes built-in SQLite database persistence (data doesn't disappear on reload).

---

## Quick Start (Local Testing)

### Option 1: Run Immediately (Fastest)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_python.py
```

Your browser will open at `http://localhost:8501`

### Option 2: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app_python.py
```

---

## Deploy to Streamlit Cloud (FREE) ⭐

This is the **easiest deployment method** for a Python Streamlit app.

### Step 1: Prepare Your Code

1. Create a GitHub account (if you don't have one) at https://github.com
2. Create a new repository named `lead-tracker`
3. Upload these files to the repo:
   - `app_python.py`
   - `requirements.txt`

### Step 2: Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Connect your GitHub account
4. Select:
   - Repository: `yourusername/lead-tracker`
   - Branch: `main`
   - Main file path: `app_python.py`
5. Click "Deploy"

**That's it!** Your app is now live at:
```
https://lead-tracker-RANDOMSTRING.streamlit.app/
```

### Important: Persistent Storage

The Python version uses **SQLite**, so your data persists! However, Streamlit Cloud has some limitations:

- Data persists within a session
- If the app is restarted, data is preserved (stored in `leads.db`)
- Safe for small teams (< 1000 leads)

For enterprise use, upgrade to Streamlit+ or add PostgreSQL.

---

## Deploy to Heroku (Alternative)

If you want more control, Heroku is a good option:

### Step 1: Create Heroku Account
- Go to https://www.heroku.com
- Sign up and verify email

### Step 2: Install Heroku CLI
```bash
# On Windows, download from:
https://devcenter.heroku.com/articles/heroku-cli

# Or on Mac:
brew tap heroku/brew && brew install heroku
```

### Step 3: Create Procfile

Create a file named `Procfile` (no extension) in your repo:
```
web: streamlit run app_python.py --logger.level=error
```

### Step 4: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create lead-tracker-yourname

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Your app will be at: `https://lead-tracker-yourname.herokuapp.com`

---

## Deploy to Your Own Server

### Option A: Linux Server with Supervisor

1. **Install dependencies:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

2. **Clone your repo:**
```bash
git clone https://github.com/yourname/lead-tracker.git
cd lead-tracker
```

3. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Create Supervisor config** (`/etc/supervisor/conf.d/lead-tracker.conf`):
```ini
[program:lead-tracker]
command=/home/ubuntu/lead-tracker/venv/bin/streamlit run app_python.py --server.port=8501
directory=/home/ubuntu/lead-tracker
user=ubuntu
autostart=true
autorestart=true
```

5. **Start the app:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start lead-tracker
```

### Option B: Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app_python.py .

EXPOSE 8501

CMD ["streamlit", "run", "app_python.py", "--server.port=8501"]
```

Deploy:
```bash
docker build -t lead-tracker .
docker run -p 8501:8501 lead-tracker
```

---

## Comparison: Deployment Options

| Platform | Cost | Setup Time | Best For | Data Persistence |
|----------|------|-----------|----------|------------------|
| **Streamlit Cloud** | Free | 2 min | MVP/testing | ✅ Yes |
| **Heroku** | $5-50/mo | 10 min | Small teams | ✅ Yes |
| **Self-hosted Linux** | $5-20/mo | 30 min | Full control | ✅ Yes |
| **Docker** | $10-50/mo | 20 min | Scalability | ✅ Yes |

**Recommendation:** Start with **Streamlit Cloud Free Tier**, upgrade to Paid when you have 100+ leads.

---

## Database: SQLite vs PostgreSQL

### Current Setup (SQLite)
- ✅ No setup required
- ✅ Data persists automatically
- ✅ Perfect for MVP
- ⚠️ Limited to ~10K leads
- ⚠️ Single user limitations

### Upgrade Path (PostgreSQL)

When you need to scale, upgrade to PostgreSQL:

```python
import psycopg2

connection = psycopg2.connect(
    host="your-db-host",
    database="lead_tracker",
    user="postgres",
    password="your-password"
)
```

This gives you:
- ✅ Unlimited leads
- ✅ Multi-user support
- ✅ Enterprise reliability
- ⚠️ Costs ~$15/month (e.g., Railway, Supabase)

---

## Environment Variables (For Production)

If you add a database password, use environment variables:

Create `.streamlit/secrets.toml`:
```toml
[database]
host = "your-db.com"
user = "postgres"
password = "your-password"
```

Access in code:
```python
db_password = st.secrets["database"]["password"]
```

---

## Monitoring Your Deployment

### Streamlit Cloud Dashboard
- View logs at https://share.streamlit.io
- Monitor resource usage
- Check app status

### Heroku Logs
```bash
heroku logs --tail
```

### Self-hosted (Supervisor)
```bash
sudo tail -f /var/log/supervisor/lead-tracker.log
```

---

## Troubleshooting

### App Crashes After Deployment

**On Streamlit Cloud:**
1. Check the app logs (red "X" icon)
2. Verify `requirements.txt` has all dependencies
3. Make sure `app_python.py` is the correct filename

**On Heroku:**
```bash
heroku logs --tail
heroku config  # Check environment variables
```

### "ModuleNotFoundError: No module named 'streamlit'"

```bash
# Make sure requirements are installed
pip install -r requirements.txt

# Or manually:
pip install streamlit pandas plotly
```

### Database Locked Error

On Streamlit Cloud, if you see this:
1. It's normal if multiple sessions are running
2. Refresh the page
3. Data will still be there

For production, upgrade to PostgreSQL.

### Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill it
kill -9 <PID>

# Or use different port
streamlit run app_python.py --server.port=8502
```

---

## Next Steps (Roadmap)

### Phase 2: Database Upgrade
- [ ] Migrate to PostgreSQL
- [ ] Add multi-user support
- [ ] User authentication (login)

### Phase 3: Automation
- [ ] Email integration for reminders
- [ ] Scheduled tasks (Celery)
- [ ] SMS alerts via Twilio

### Phase 4: AI Enhancement
- [ ] ML-based lead scoring
- [ ] Predictive follow-up timing
- [ ] Sales conversation suggestions

### Phase 5: Mobile
- [ ] Mobile app (React Native)
- [ ] Push notifications
- [ ] Offline support

---

## Cost Breakdown (Year 1)

| Item | Cost | Notes |
|------|------|-------|
| Streamlit Cloud (Free) | $0 | For MVP |
| Domain (optional) | $12 | nameserver.com |
| Custom domain setup | $0 | Streamlit does this free |
| **Total Year 1** | **$12** | Minimal investment |

If upgrading to Streamlit Paid:
- Streamlit Professional: $30/month = $360/year
- Postgres (Supabase): $25/month = $300/year
- **Total: $660/year** (still affordable)

---

## API Integration (Future)

Once deployed, you can add external integrations:

```python
# Send emails on lead add
import smtplib
from email.mime.text import MIMEText

def send_welcome_email(email):
    msg = MIMEText(f"Welcome! We received your inquiry.")
    msg['Subject'] = "Welcome"
    msg['From'] = "noreply@leadtracker.com"
    msg['To'] = email

    # Requires SMTP setup
    # smtp.sendmail(...)
```

This is in Phase 3 of the roadmap.

---

## Questions?

- **Streamlit Docs:** https://docs.streamlit.io
- **Deployment Help:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- **Community:** https://discuss.streamlit.io

Happy deploying! 🚀
