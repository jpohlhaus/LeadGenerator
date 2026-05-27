# Lead Tracker MVP - Shiny for Python Deployment Guide

## Why Shiny for Python?

**Shiny for Python** is Posit's Python implementation of Shiny (R). It gives you:

✅ **Same reactive programming as R Shiny** — but in Python  
✅ **Professional UI components** — not basic like Streamlit  
✅ **Better control** — more customization than Streamlit  
✅ **Larger ecosystem** — Shiny for R has proven patterns  
✅ **Production-ready** — used by enterprises  

**Comparison:**

| Feature | Streamlit | Shiny Python | Shiny R |
|---------|-----------|--------------|---------|
| **Language** | Python | Python | R |
| **Reactivity** | Simple | Advanced | Advanced |
| **UI Control** | Limited | Excellent | Excellent |
| **Deployment** | Easy | Medium | Medium |
| **Learning Curve** | Easy | Medium | Medium |
| **Enterprise Ready** | Yes | Yes | Yes |

---

## Quick Start (Local)

### Run Locally (30 seconds)

```bash
# Install dependencies
pip install -r requirements_shiny.txt

# Run the app
shiny run app_shiny.py
```

Opens at `http://localhost:8000` with hot reload enabled.

---

## Deployment Options

### Option 1: Posit Cloud (Easiest) ⭐

Deploy to Posit's managed hosting service (similar to shinyapps.io for R).

#### Step 1: Sign Up
- Go to https://posit.cloud
- Create free account
- Verify email

#### Step 2: Install Posit CLI
```bash
# macOS/Linux
curl -fsSL https://cdn.posit.co/publish/posit-public.asc | gpg --dearmor | sudo tee /usr/share/keyrings/posit-archive-keyring.gpg > /dev/null
sudo apt-add-repository "deb [signed-by=/usr/share/keyrings/posit-archive-keyring.gpg] https://posit-releases.s3.amazonaws.com/debian stable main"
sudo apt-get update
sudo apt-get install rsconnect-python

# macOS with Homebrew
brew install posit-cli

# Windows: Download from posit.co/download/tools/
```

#### Step 3: Configure Credentials
```bash
posit connect api-tokens
# Follow prompts to add your Posit Cloud token
```

#### Step 4: Deploy
```bash
shiny deploy posit app_shiny.py
```

**Your app is now live!** Get the URL from the output.

### Option 2: Shiny for Python Hosting

Deploy directly to Posit's native Shiny hosting:

```bash
# Install shiny CLI
pip install shiny[dev]

# Deploy
shiny deploy posit app_shiny.py --title lead-tracker
```

### Option 3: Heroku

Use Heroku for self-hosted deployment.

#### Step 1: Create Procfile
```
web: shiny run app_shiny.py --host 0.0.0.0 --port $PORT
```

#### Step 2: Create runtime.txt
```
python-3.11.0
```

#### Step 3: Deploy
```bash
heroku login
heroku create lead-tracker-yourname
git push heroku main
```

Visit: `https://lead-tracker-yourname.herokuapp.com`

### Option 4: Docker

Build and deploy as a container.

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_shiny.txt .
RUN pip install -r requirements_shiny.txt

COPY app_shiny.py .
COPY leads.db .

EXPOSE 8000

CMD ["shiny", "run", "app_shiny.py", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Run
```bash
docker build -t lead-tracker .
docker run -p 8000:8000 lead-tracker
```

### Option 5: Self-Hosted (Linux + Systemd)

For full control on your own server.

#### Step 1: Install Dependencies
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

#### Step 2: Setup Virtual Environment
```bash
mkdir /opt/lead-tracker
cd /opt/lead-tracker

python3 -m venv venv
source venv/bin/activate
pip install -r requirements_shiny.txt
```

#### Step 3: Create Systemd Service

Create `/etc/systemd/system/lead-tracker.service`:

```ini
[Unit]
Description=Lead Tracker Shiny App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/lead-tracker
ExecStart=/opt/lead-tracker/venv/bin/shiny run app_shiny.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Step 4: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable lead-tracker
sudo systemctl start lead-tracker
sudo systemctl status lead-tracker
```

Access at: `http://your-server:8000`

#### View Logs
```bash
sudo journalctl -u lead-tracker -f
```

---

## Deployment Comparison

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Posit Cloud** | Free tier | 2 min | MVP/Testing ⭐ |
| **Heroku** | $5-50/mo | 5 min | Small teams |
| **Self-hosted** | $5-20/mo | 30 min | Full control |
| **Docker** | $10-50/mo | 20 min | Scalability |

**Recommendation:** Start with Posit Cloud free tier, upgrade to paid when needed.

---

## Production Considerations

### Add Database Persistence

Currently uses SQLite. For production, upgrade to PostgreSQL:

```python
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
```

Use environment variables for secrets:
```bash
export DB_HOST="your-postgres-host"
export DB_NAME="lead_tracker"
export DB_USER="postgres"
export DB_PASSWORD="your-secure-password"
```

### Enable HTTPS

On Posit Cloud: Automatic (custom domain support available)

On self-hosted: Use Nginx as reverse proxy:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Monitor & Logging

On Posit Cloud:
- Use Posit Cloud dashboard
- View app metrics and logs
- Monitor usage

On self-hosted:
```bash
# View logs
sudo journalctl -u lead-tracker -f

# Monitor resources
htop

# Check disk usage
df -h
```

---

## Shiny for Python vs Streamlit vs Shiny for R

### Code Structure

**Streamlit (Imperative):**
```python
# Runs from top to bottom every interaction
st.title("My App")
if st.button("Click me"):
    st.write("Clicked!")
```

**Shiny for Python (Reactive):**
```python
# Define dependencies once, update reactively
@output
@render.text
def my_text():
    return f"Button clicked {input.click_count()} times"
```

**Shiny for R (Reactive):**
```r
# Same pattern as Shiny for Python
output$myText <- renderText({
  paste("Button clicked", input$click_count, "times")
})
```

### When to Use Each

| Use Case | Streamlit | Shiny Python | Shiny R |
|----------|-----------|--------------|---------|
| **Quick dashboards** | ✅ | ⭕ | ⭕ |
| **MVP/prototyping** | ✅ | ✅ | ✅ |
| **Complex interactions** | ⭕ | ✅ | ✅ |
| **Enterprise apps** | ⭕ | ✅ | ✅ |
| **Python-heavy data** | ✅ | ✅ | ⭕ |
| **Statistics/modeling** | ⭕ | ⭕ | ✅ |

**For this app:** Shiny for Python is ideal because:
- Complex reactivity needed
- Professional UI required
- Python data tools (pandas)
- Enterprise-ready

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'shiny'"

```bash
pip install -r requirements_shiny.txt
```

### App crashes on start

Check logs:
```bash
shiny run app_shiny.py --reload
```

Look for Python errors in terminal output.

### Database locked

On Posit Cloud, if multiple sessions:
1. Refresh page
2. Data persists (SQLite handles this)
3. Consider upgrading to PostgreSQL

### Port already in use

```bash
# Use different port
shiny run app_shiny.py --port 8001

# Kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Deployment fails

**Posit Cloud:**
- Check credentials: `shiny auth-token`
- Verify app runs locally first
- Check internet connection

**Heroku:**
```bash
heroku logs --tail
heroku config  # Check env vars
```

**Self-hosted:**
```bash
sudo systemctl status lead-tracker
sudo journalctl -u lead-tracker -f
```

---

## Advanced: Customization

### Add Custom CSS

```python
app_ui = ui.page_navbar(
    ui.tags.head(
        ui.tags.style("""
        .custom-card {
            border: 2px solid #ff6b6b;
            padding: 20px;
        }
        """)
    ),
    # ... rest of UI
)
```

### Add JavaScript

```python
ui.tags.script("""
function logEvent(msg) {
    console.log(msg);
}
"""),
```

### Custom Reactive

```python
@reactive.Calc
def expensive_calculation():
    df = get_all_leads()
    # Do heavy computation
    return processed_data

# Use in multiple outputs without re-computing
@output
@render.table
def table1():
    return expensive_calculation()

@output
@render.plot
def plot1():
    return expensive_calculation()
```

---

## Cost Breakdown (Year 1)

| Platform | Cost | Notes |
|----------|------|-------|
| **Posit Cloud Free** | $0 | For MVP |
| **Custom domain** | $12 | Optional |
| **Posit Cloud Paid** | $99/year | When scaling |
| **PostgreSQL (Supabase)** | $0-25/month | When needed |
| **Total (MVP)** | **$12** | Minimal investment |

---

## Next Steps (Roadmap)

### Phase 2: Scaling
- [ ] Migrate to PostgreSQL
- [ ] Add user authentication
- [ ] Multi-user support

### Phase 3: Automation
- [ ] Email reminders (SendGrid)
- [ ] Background jobs (Celery)
- [ ] SMS alerts (Twilio)

### Phase 4: AI
- [ ] ML-based lead scoring
- [ ] Predictive follow-ups
- [ ] Sales insights

### Phase 5: Mobile
- [ ] React Native app
- [ ] Push notifications
- [ ] Offline support

---

## Resources

- **Shiny for Python Docs:** https://shiny.posit.co/py/
- **Posit Cloud:** https://posit.cloud
- **Shiny Gallery:** https://shinygallery.io/
- **Community Forum:** https://community.rstudio.com/

---

## Questions?

- **Shiny Python:** https://shiny.posit.co/py/docs/
- **Posit Cloud Help:** https://docs.posit.cloud/
- **GitHub Issues:** Create an issue if you find bugs

Happy deploying! 🚀
