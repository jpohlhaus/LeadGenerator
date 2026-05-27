import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Lead Tracker MVP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .hot-lead {
        color: #ff6b6b;
        font-weight: bold;
    }
    .warm-lead {
        color: #ffa500;
        font-weight: bold;
    }
    .cold-lead {
        color: #4ecdc4;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE SETUP
# ============================================================================

@st.cache_resource
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
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
    return pd.read_sql_query('SELECT * FROM leads ORDER BY created_at DESC', conn)

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

# Initialize database with sample data
init_sample_data()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("📋 Lead Tracker")
page = st.sidebar.radio("Navigate", ["Dashboard", "All Leads", "Add Lead", "Analytics"])

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

if page == "Dashboard":
    st.title("📊 Lead Tracker Dashboard")

    df = get_all_leads()

    if len(df) == 0:
        st.warning("No leads yet. Go to 'Add Lead' to get started!")
    else:
        # Convert date columns
        df['last_contact'] = pd.to_datetime(df['last_contact'])
        df['next_followup'] = pd.to_datetime(df['next_followup'])

        today = datetime.now().date()

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Leads",
                value=len(df),
                delta=None,
                delta_color="off"
            )

        with col2:
            hot_count = len(df[df['status'] == 'Hot'])
            st.metric(
                label="Hot Leads 🔥",
                value=hot_count,
                delta=None,
                delta_color="off"
            )

        with col3:
            due_count = len(df[df['next_followup'].dt.date <= today])
            st.metric(
                label="Due Today ⏰",
                value=due_count,
                delta=None,
                delta_color="off"
            )

        with col4:
            hot_rate = round((hot_count / len(df) * 100), 1) if len(df) > 0 else 0
            st.metric(
                label="Hot Lead Rate %",
                value=f"{hot_rate}%",
                delta=None,
                delta_color="off"
            )

        st.divider()

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Lead Status Distribution")
            status_counts = df['status'].value_counts()
            colors = {'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'}
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.index,
                color_discrete_map=colors,
                text=status_counts.values
            )
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Top Lead Sources")
            source_counts = df['source'].value_counts().head(8)
            fig = px.barh(
                x=source_counts.values,
                y=source_counts.index,
                labels={'x': 'Count', 'y': 'Source'},
                text=source_counts.values,
                color=source_counts.values,
                color_continuous_scale='blues'
            )
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Upcoming Follow-ups
        st.subheader("📅 Upcoming Follow-ups (Next 7 Days)")
        future_date = today + timedelta(days=7)
        upcoming = df[(df['next_followup'].dt.date >= today) &
                      (df['next_followup'].dt.date <= future_date)].copy()

        if len(upcoming) > 0:
            upcoming['next_followup'] = upcoming['next_followup'].dt.strftime('%Y-%m-%d')
            upcoming['last_contact'] = upcoming['last_contact'].dt.strftime('%Y-%m-%d')
            display_cols = ['name', 'email', 'phone', 'status', 'next_followup', 'notes']
            st.dataframe(
                upcoming[display_cols].sort_values('next_followup'),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No follow-ups scheduled for the next 7 days")

# ============================================================================
# PAGE: ALL LEADS
# ============================================================================

elif page == "All Leads":
    st.title("📋 Lead Database")

    df = get_all_leads()

    if len(df) == 0:
        st.warning("No leads yet. Go to 'Add Lead' to get started!")
    else:
        # Convert dates for display
        df['last_contact'] = pd.to_datetime(df['last_contact']).dt.strftime('%Y-%m-%d')
        df['next_followup'] = pd.to_datetime(df['next_followup']).dt.strftime('%Y-%m-%d')

        # Filter options
        col1, col2 = st.columns(2)

        with col1:
            filter_status = st.multiselect(
                "Filter by Status",
                options=df['status'].unique(),
                default=df['status'].unique()
            )

        with col2:
            filter_source = st.multiselect(
                "Filter by Source",
                options=df['source'].unique(),
                default=df['source'].unique()
            )

        # Apply filters
        df_filtered = df[
            (df['status'].isin(filter_status)) &
            (df['source'].isin(filter_source))
        ]

        # Display table
        st.subheader(f"Showing {len(df_filtered)} of {len(df)} leads")

        # Color code status
        def color_status(status):
            if status == "Hot":
                return f'<span class="hot-lead">{status}</span>'
            elif status == "Warm":
                return f'<span class="warm-lead">{status}</span>'
            else:
                return f'<span class="cold-lead">{status}</span>'

        display_cols = ['name', 'email', 'phone', 'source', 'score', 'status', 'last_contact', 'next_followup', 'notes']
        st.dataframe(
            df_filtered[display_cols],
            use_container_width=True,
            hide_index=True
        )

        # Export option
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ============================================================================
# PAGE: ADD LEAD
# ============================================================================

elif page == "Add Lead":
    st.title("➕ Add New Lead")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Lead Information")

        name = st.text_input("Company Name*", placeholder="Acme Corp")
        email = st.text_input("Email*", placeholder="contact@company.com")
        phone = st.text_input("Phone", placeholder="555-0000")

        source = st.selectbox(
            "Lead Source*",
            options=["Google Ads", "Referral", "Website Form", "Cold Outreach", "Social Media", "Event", "Other"]
        )

        score = st.slider("Lead Score (0-100)", min_value=0, max_value=100, value=50, step=5)

        status = st.selectbox("Status*", options=["Cold", "Warm", "Hot"])

        notes = st.text_area("Notes", placeholder="Any relevant information...", height=80)

        # Submit button
        if st.button("✅ Add Lead", use_container_width=True, type="primary"):
            if not name or not email:
                st.error("⚠️ Please fill in Company Name and Email (required fields)")
            else:
                add_lead(name, email, phone, source, score, status, notes)
                st.success(f"✅ Lead '{name}' added successfully!")
                st.balloons()

                # Clear session state to reset form
                st.session_state.clear()

    with col2:
        st.subheader("✨ Next Steps")
        st.info("""
        **Quick Follow-up Tasks:**

        1. ✉️ Send welcome email to new lead
        2. 📅 Set a reminder for 48-hour follow-up
        3. 📊 Add to your CRM if you have one

        **Lead Scoring Tips:**

        **Hot (75+):** Budget confirmed, decision maker present, timeline aligned

        **Warm (40-74):** Interested, asking questions, checking with team

        **Cold (0-39):** Early stage, just learning, long timeline
        """)

        st.divider()

        st.subheader("📈 Quick Stats")
        df = get_all_leads()
        if len(df) > 0:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Leads", len(df))
            with col_b:
                hot_pct = round(len(df[df['status'] == 'Hot']) / len(df) * 100, 1)
                st.metric("Hot %", f"{hot_pct}%")

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

elif page == "Analytics":
    st.title("📈 Lead Analytics")

    df = get_all_leads()

    if len(df) == 0:
        st.warning("No leads yet. Go to 'Add Lead' to get started!")
    else:
        # Convert dates
        df['last_contact'] = pd.to_datetime(df['last_contact'])
        df['next_followup'] = pd.to_datetime(df['next_followup'])
        df['days_since'] = (datetime.now() - df['last_contact']).dt.days

        col1, col2 = st.columns(2)

        # Score Distribution
        with col1:
            st.subheader("Lead Score Distribution")
            fig = px.histogram(
                df,
                x='score',
                nbins=10,
                color='status',
                color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'},
                labels={'score': 'Lead Score', 'count': 'Number of Leads'}
            )
            fig.update_layout(height=350, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

        # Conversion Metrics
        with col2:
            st.subheader("Conversion Metrics")
            total = len(df)
            hot = len(df[df['status'] == 'Hot'])
            warm = len(df[df['status'] == 'Warm'])
            cold = len(df[df['status'] == 'Cold'])
            avg_score = round(df['score'].mean(), 1)

            metric_text = f"""
            **Total Leads:** {total}

            **Hot Leads:** {hot} ({round(hot/total*100, 1)}%)

            **Warm Leads:** {warm} ({round(warm/total*100, 1)}%)

            **Cold Leads:** {cold} ({round(cold/total*100, 1)}%)

            ---

            **Average Lead Score:** {avg_score}
            """
            st.markdown(metric_text)

        st.divider()

        # Lead Age vs Quality
        st.subheader("Lead Age vs Quality")
        fig = px.scatter(
            df,
            x='days_since',
            y='score',
            color='status',
            size='score',
            hover_data=['name', 'email'],
            color_discrete_map={'Hot': '#ff6b6b', 'Warm': '#ffa500', 'Cold': '#4ecdc4'},
            labels={'days_since': 'Days Since Last Contact', 'score': 'Lead Quality Score'},
            title='Bubble size = Lead Quality'
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **How to read this chart:**
        - **Upper Left (Red zone):** Hot leads needing urgent follow-up
        - **Upper Right (Nurturing zone):** Old hot leads, should re-engage
        - **Lower Left (Action zone):** Should follow up soon
        - **Lower Right (Low priority zone):** Cold leads, can wait
        """)

        st.divider()

        # Source Analysis
        st.subheader("Lead Source Performance")
        source_analysis = df.groupby('source').agg({
            'name': 'count',
            'score': 'mean',
            'status': lambda x: (x == 'Hot').sum()
        }).rename(columns={
            'name': 'Leads',
            'score': 'Avg Score',
            'status': 'Hot Count'
        }).reset_index()
        source_analysis['Hot %'] = (source_analysis['Hot Count'] / source_analysis['Leads'] * 100).round(1)
        source_analysis['Avg Score'] = source_analysis['Avg Score'].round(1)

        st.dataframe(
            source_analysis.sort_values('Hot %', ascending=False),
            use_container_width=True,
            hide_index=True
        )

# ============================================================================
# Footer
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    <p>Lead Tracker MVP | Powered by Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)
