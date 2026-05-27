from shiny import App, reactive, render, ui
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3

# ============================================================================
# DATABASE SETUP
# ============================================================================

def get_db_connection():
    """Initialize SQLite database"""
    conn = sqlite3.connect('leads.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            source TEXT NOT NULL,
            score INTEGER,
            status TEXT,
            last_contact DATE,
            next_followup DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def init_sample_data():
    """Add sample leads if database is empty"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM leads")
    count = cursor.fetchone()['count']

    if count == 0:
        sample_leads = [
            ("Acme Corp", "contact@acme.com", "555-0101", "Google Ads", 85, "Hot", "2026-05-20", "2026-05-28", "Budget approved"),
            ("TechStart Inc", "hello@techstart.com", "555-0102", "Referral", 72, "Warm", "2026-05-15", "2026-05-25", "Waiting on decision"),
            ("Local Bakery", "info@bakery.com", "555-0103", "Website Form", 45, "Cold", "2026-05-10", "2026-05-28", "Low interest"),
            ("Design Studio", "hello@design.com", "555-0104", "Cold Outreach", 90, "Hot", "2026-05-22", "2026-05-25", "Ready to close"),
            ("Consulting Group", "team@consult.com", "555-0105", "Referral", 68, "Warm", "2026-05-18", "2026-05-29", "Negotiating terms"),
        ]
        for lead in sample_leads:
            cursor.execute('''
                INSERT INTO leads (name, email, phone, source, score, status, last_contact, next_followup, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', lead)
        conn.commit()

def get_all_leads():
    """Fetch all leads from database"""
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM leads ORDER BY created_at DESC', conn)
    conn.close()
    return df

def add_lead(name, email, phone, source, score, status, notes):
    """Add new lead to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    next_followup = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO leads (name, email, phone, source, score, status, last_contact, next_followup, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, source, score, status, today, next_followup, notes))
    conn.commit()
    conn.close()

# Initialize
init_sample_data()

# ============================================================================
# SHINY APP - ULTRA SIMPLE VERSION
# ============================================================================

app_ui = ui.page_fluid(
    ui.h1("📊 Lead Tracker MVP"),
    ui.input_select(
        "page",
        "Select Page:",
        {
            "dashboard": "📊 Dashboard",
            "leads": "📋 All Leads",
            "add": "➕ Add Lead",
            "analytics": "📈 Analytics",
        }
    ),
    ui.br(),

    # DASHBOARD PAGE
    ui.conditional_panel(
        "input.page === 'dashboard'",
        ui.row(
            ui.column(3, ui.value_box("Total Leads", ui.output_text("total_leads"), theme="info")),
            ui.column(3, ui.value_box("🔥 Hot Leads", ui.output_text("hot_leads"), theme="danger")),
            ui.column(3, ui.value_box("⏰ Due Today", ui.output_text("due_today"), theme="warning")),
            ui.column(3, ui.value_box("Conversion %", ui.output_text("conversion_rate"), theme="success")),
        ),
        ui.br(),
        ui.row(
            ui.column(6, ui.output_plot("status_chart")),
            ui.column(6, ui.output_plot("source_chart")),
        ),
        ui.br(),
        ui.h3("📅 Upcoming Follow-ups (Next 7 Days)"),
        ui.output_table("upcoming_table"),
    ),

    # ALL LEADS PAGE
    ui.conditional_panel(
        "input.page === 'leads'",
        ui.h2("📋 Lead Database"),
        ui.row(
            ui.column(6, ui.input_select("filter_status", "Filter by Status", choices=[])),
            ui.column(6, ui.input_select("filter_source", "Filter by Source", choices=[])),
        ),
        ui.br(),
        ui.output_table("all_leads_table"),
        ui.br(),
        ui.download_button("download_leads", "📥 Download as CSV"),
    ),

    # ADD LEAD PAGE
    ui.conditional_panel(
        "input.page === 'add'",
        ui.h2("➕ Add New Lead"),
        ui.row(
            ui.column(
                6,
                ui.h3("Lead Information"),
                ui.input_text("new_name", "Company Name *", placeholder="Acme Corp"),
                ui.input_text("new_email", "Email *", placeholder="contact@company.com"),
                ui.input_text("new_phone", "Phone", placeholder="555-0000"),
                ui.input_select("new_source", "Lead Source *",
                    choices=["Google Ads", "Referral", "Website Form", "Cold Outreach", "Social Media", "Event", "Other"]
                ),
                ui.input_slider("new_score", "Lead Score (0-100)", 0, 100, 50, step=5),
                ui.input_select("new_status", "Status *", choices=["Cold", "Warm", "Hot"]),
                ui.input_text_area("new_notes", "Notes", placeholder="Any relevant information...", rows=4),
                ui.input_action_button("submit_lead", "✅ Add Lead", class_="btn-primary w-100"),
                ui.br(),
                ui.output_ui("success_message"),
            ),
            ui.column(
                6,
                ui.h3("✨ Next Steps"),
                ui.markdown("""
                **Quick Follow-up Tasks:**
                1. ✉️ Send welcome email
                2. 📅 Set 48-hour reminder
                3. 📊 Add to your CRM

                **Lead Scoring:**
                - **Hot (75+):** Budget confirmed
                - **Warm (40-74):** Interested
                - **Cold (0-39):** Early stage
                """),
                ui.br(),
                ui.value_box("Total Leads", ui.output_text("total_leads_add"), theme="primary"),
                ui.value_box("Hot %", ui.output_text("hot_pct_add"), theme="danger"),
            ),
        ),
    ),

    # ANALYTICS PAGE
    ui.conditional_panel(
        "input.page === 'analytics'",
        ui.h2("📈 Lead Analytics"),
        ui.row(
            ui.column(6, ui.output_plot("score_distribution")),
            ui.column(6, ui.output_ui("conversion_metrics")),
        ),
        ui.br(),
        ui.h3("Lead Age vs Quality"),
        ui.output_plot("age_analysis"),
        ui.br(),
        ui.h3("Lead Source Performance"),
        ui.output_table("source_performance"),
    ),
)

def server(input, output, session):

    # Reactive data
    leads_data = reactive.Value(get_all_leads())

    def refresh_leads():
        leads_data.set(get_all_leads())

    # ========== DASHBOARD OUTPUTS ==========

    @output
    @render.text
    def total_leads():
        return str(len(leads_data()))

    @output
    @render.text
    def hot_leads():
        df = leads_data()
        return str(len(df[df['status'] == 'Hot']))

    @output
    @render.text
    def due_today():
        today = datetime.now().date()
        df = leads_data().copy()
        df['next_followup'] = pd.to_datetime(df['next_followup']).dt.date
        return str(len(df[df['next_followup'] <= today]))

    @output
    @render.text
    def conversion_rate():
        df = leads_data()
        if len(df) == 0:
            return "0%"
        hot_count = len(df[df['status'] == 'Hot'])
        rate = round((hot_count / len(df)) * 100, 1)
        return f"{rate}%"

    @output
    @render.plot
    def status_chart():
        df = leads_data()
        status_counts = df['status'].value_counts()
        colors = {'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'}
        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            color=status_counts.index,
            color_discrete_map=colors,
            text=status_counts.values,
            title="Lead Status Distribution"
        )
        fig.update_layout(showlegend=False, height=350)
        return fig

    @output
    @render.plot
    def source_chart():
        df = leads_data()
        source_counts = df['source'].value_counts().head(8)
        fig = px.barh(
            x=source_counts.values,
            y=source_counts.index,
            text=source_counts.values,
            color=source_counts.values,
            color_continuous_scale='blues',
            title="Top Lead Sources"
        )
        fig.update_layout(showlegend=False, height=350)
        return fig

    @output
    @render.table
    def upcoming_table():
        df = leads_data().copy()
        today = datetime.now().date()
        future_date = today + timedelta(days=7)
        df['next_followup'] = pd.to_datetime(df['next_followup']).dt.date
        df['last_contact'] = pd.to_datetime(df['last_contact']).dt.date
        upcoming = df[(df['next_followup'] >= today) & (df['next_followup'] <= future_date)]
        if len(upcoming) > 0:
            return upcoming[['name', 'email', 'phone', 'status', 'next_followup', 'notes']].sort_values('next_followup')
        return pd.DataFrame()

    # ========== ALL LEADS OUTPUTS ==========

    @output
    @render.table
    def all_leads_table():
        df = leads_data().copy()
        df['last_contact'] = pd.to_datetime(df['last_contact']).dt.strftime('%Y-%m-%d')
        df['next_followup'] = pd.to_datetime(df['next_followup']).dt.strftime('%Y-%m-%d')
        status_filter = input.filter_status()
        source_filter = input.filter_source()
        if status_filter:
            df = df[df['status'].isin(status_filter)]
        if source_filter:
            df = df[df['source'].isin(source_filter)]
        return df[['name', 'email', 'phone', 'source', 'score', 'status', 'last_contact', 'next_followup']]

    @output
    @render.download(filename="leads.csv")
    def download_leads():
        return leads_data().to_csv(index=False)

    # Update filters
    @reactive.Effect
    def _():
        df = leads_data()
        if len(df) > 0:
            ui.update_select("filter_status", choices=sorted(df['status'].unique().tolist()))
            ui.update_select("filter_source", choices=sorted(df['source'].unique().tolist()))

    # ========== ADD LEAD OUTPUTS ==========

    @output
    @render.text
    def total_leads_add():
        return str(len(leads_data()))

    @output
    @render.text
    def hot_pct_add():
        df = leads_data()
        if len(df) == 0:
            return "0%"
        hot_count = len(df[df['status'] == 'Hot'])
        return f"{round(hot_count/len(df)*100, 1)}%"

    @output
    @render.ui
    def success_message():
        return ui.div()

    @reactive.Effect
    def _():
        if input.submit_lead() > 0:
            name = input.new_name()
            email = input.new_email()
            if not name or not email:
                return
            add_lead(name, input.new_email(), input.new_phone(), input.new_source(),
                    input.new_score(), input.new_status(), input.new_notes())
            refresh_leads()
            ui.update_text("new_name", value="")
            ui.update_text("new_email", value="")
            ui.update_text("new_phone", value="")
            ui.update_slider("new_score", value=50)
            ui.update_text_area("new_notes", value="")

    # ========== ANALYTICS OUTPUTS ==========

    @output
    @render.plot
    def score_distribution():
        df = leads_data()
        if len(df) == 0:
            return px.bar()
        fig = px.histogram(
            df, x='score', nbins=10, color='status',
            color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'},
            title="Lead Score Distribution"
        )
        fig.update_layout(height=350)
        return fig

    @output
    @render.ui
    def conversion_metrics():
        df = leads_data()
        if len(df) == 0:
            return ui.div("No leads")
        total = len(df)
        hot = len(df[df['status'] == 'Hot'])
        warm = len(df[df['status'] == 'Warm'])
        cold = len(df[df['status'] == 'Cold'])
        avg_score = round(df['score'].mean(), 1)
        return ui.markdown(f"""
        **Total:** {total}
        **Hot:** {hot} ({round(hot/total*100, 1)}%)
        **Warm:** {warm} ({round(warm/total*100, 1)}%)
        **Cold:** {cold} ({round(cold/total*100, 1)}%)
        **Avg Score:** {avg_score}
        """)

    @output
    @render.plot
    def age_analysis():
        df = leads_data().copy()
        if len(df) == 0:
            return px.scatter()
        df['last_contact'] = pd.to_datetime(df['last_contact'])
        df['days_since'] = (datetime.now() - df['last_contact']).dt.days
        fig = px.scatter(df, x='days_since', y='score', color='status', size='score',
            color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'},
            title='Lead Age vs Quality')
        fig.update_layout(height=450)
        return fig

    @output
    @render.table
    def source_performance():
        df = leads_data()
        if len(df) == 0:
            return pd.DataFrame()
        result = df.groupby('source').agg({
            'name': 'count',
            'score': 'mean',
            'status': lambda x: (x == 'Hot').sum()
        }).rename(columns={'name': 'Leads', 'score': 'Avg Score', 'status': 'Hot Count'}).reset_index()
        result['Hot %'] = (result['Hot Count'] / result['Leads'] * 100).round(1)
        result['Avg Score'] = result['Avg Score'].round(1)
        return result.sort_values('Hot %', ascending=False)

app = App(app_ui, server)
