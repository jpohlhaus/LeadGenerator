# Quick Start - Shiny for Python Lead Tracker

**Get running in 30 seconds. Deploy in 2 minutes.**

---

## 🚀 Run Locally

```bash
pip install -r requirements_shiny.txt
shiny run app_shiny.py
```

Opens at `http://localhost:8000` with **hot reload** ✨

---

## 🌐 Deploy Free (Posit Cloud)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Lead Tracker MVP - Shiny"
git push origin main
```

### Step 2: Sign Up & Deploy
1. Go to https://posit.cloud
2. Click "New App" → Select "Python" → "Shiny"
3. Connect GitHub repo
4. Deploy!

**Live in 2 minutes.** Share the URL with your team.

---

## 📦 What You Get

| File | Purpose |
|------|---------|
| `app_shiny.py` | Shiny app (450 lines, all-in-one) |
| `requirements_shiny.txt` | Dependencies |
| `leads.db` | SQLite database (auto-created) |
| `SHINY_PYTHON_DEPLOYMENT.md` | All deployment options |
| `README_SHINY_PYTHON.md` | Full docs |

---

## ✨ Features Overview

✅ **Dashboard** — 4 key metrics + 2 charts  
✅ **All Leads** — Searchable database  
✅ **Add Lead** — 30-second form  
✅ **Analytics** — 3 advanced visualizations  
✅ **Reactive UI** — Changes update instantly  
✅ **CSV Export** — Download anytime  
✅ **Data Persistence** — SQLite keeps everything  

---

## 🎯 Common Tasks (30 seconds each)

### Add a Lead
1. Click "Add Lead" tab
2. Fill form
3. Click "✅ Add Lead"
4. Watch dashboard update instantly (reactive!)

### View All Leads
1. Click "All Leads" tab
2. Filter by Status or Source
3. Click column header to sort
4. Click "Download as CSV" to export

### Check Analytics
1. Click "Analytics" tab
2. See score distribution
3. View lead age vs quality
4. Check which sources work best

---

## 🔧 Why Shiny for Python?

**Reactive programming** — Outputs update automatically when inputs change

**Professional UI** — Not basic like Streamlit, production-grade design

**Enterprise-ready** — Used by Fortune 500 companies

**Python-native** — Works with pandas, scikit-learn, etc.

```python
# When user adds lead, ALL outputs refresh automatically
@output
@render.table
def all_leads_table():
    return leads_data()  # Recomputes when data changes
```

---

## 📊 Deployment Options

| Platform | Cost | Setup Time |
|----------|------|-----------|
| **Posit Cloud** | Free | 2 min ⭐ |
| **Heroku** | $5+/mo | 5 min |
| **Self-hosted** | $5-20/mo | 30 min |
| **Docker** | $10-50/mo | 20 min |

**Start free.** Upgrade when you need it.

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'shiny'"
```bash
pip install -r requirements_shiny.txt
```

### Port 8000 already in use
```bash
shiny run app_shiny.py --port 8001
```

### App crashes
```bash
# Run with debug info
shiny run app_shiny.py --reload
```

### Database locked
- Refresh page
- Data still there (SQLite persists)
- If on Posit Cloud, auto-resolved

---

## 📈 What's Happening Under the Hood?

1. **You add a lead** → SQLite records it
2. **Reactive trigger fires** → `leads_data()` updates
3. **All outputs recompute** → Dashboard, tables, charts
4. **UI refreshes** → User sees changes instantly

No manual "reload" or "refresh" needed!

---

## 🎓 Next Steps

1. **Run it:**
   ```bash
   pip install -r requirements_shiny.txt
   shiny run app_shiny.py
   ```

2. **Test locally:** Add a few leads, check analytics

3. **Deploy:** 
   - Sign up posit.cloud
   - Push to GitHub
   - Deploy in dashboard (2 min)

4. **Share:** Give team the URL

5. **Scale:** Upgrade to PostgreSQL when you hit 10K+ leads

---

## 💡 Pro Tips

### Customize Colors
Edit `app_shiny.py`, find:
```python
colors = {'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'}
```

### Add New Field
1. Edit `CREATE TABLE` SQL
2. Add input in "Add Lead" form
3. Add to display tables
4. Restart app

### Check Database Directly
```bash
sqlite3 leads.db "SELECT * FROM leads LIMIT 5;"
```

### Export Data
```bash
sqlite3 leads.db ".mode csv" ".output leads.csv" "SELECT * FROM leads;"
```

---

## 🚀 You're Ready!

```bash
# Step 1: Install
pip install -r requirements_shiny.txt

# Step 2: Run
shiny run app_shiny.py

# Step 3: Deploy
# Push to GitHub → Posit Cloud → Live!
```

**Questions?** See SHINY_PYTHON_DEPLOYMENT.md or README_SHINY_PYTHON.md

Happy tracking! 🎉
