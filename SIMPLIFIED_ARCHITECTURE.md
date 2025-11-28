# FinanceBot - Simplified All-Python Architecture

## Overview
Complete Python-based solution using Streamlit for UI and FastAPI for backend webhooks.

---

## Simplified Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│                    Streamlit App                             │
│  - Login with OTP                                            │
│  - Dashboard (show financial summary)                        │
│  - Initiate calls                                            │
│  - View & download reports                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Direct Python calls
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  PYTHON SERVICES                             │
│  ├─ pixpoc_client.py    (Call Pixpoc API)                   │
│  ├─ agent_service.py    (Run CrewAI agents)                 │
│  └─ report_service.py   (Generate PDFs)                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────────┐
        │          │          │              │
   ┌────▼───┐ ┌───▼────┐ ┌───▼────┐  ┌─────▼─────┐
   │Pixpoc  │ │CrewAI  │ │ SQLite │  │  Files    │
   │  API   │ │Agents  │ │   DB   │  │ /reports/ │
   └────────┘ └────────┘ └────────┘  └───────────┘
```

**Plus**: Small FastAPI webhook server (runs separately) to receive Pixpoc callbacks

---

## Project Structure

```
FinanceBot/
├── streamlit_app/
│   ├── app.py                    # Main Streamlit app
│   ├── pages/
│   │   ├── 1_📊_Dashboard.py    # Dashboard page
│   │   ├── 2_🧮_Calculators.py  # Financial calculators
│   │   └── 3_📄_Reports.py      # View reports
│   ├── components/
│   │   ├── auth.py              # Login/OTP components
│   │   ├── dashboard.py         # Dashboard widgets
│   │   └── reports.py           # Report cards
│   └── utils/
│       ├── session.py           # Session management
│       └── helpers.py           # Utility functions
│
├── services/
│   ├── pixpoc_client.py         # Pixpoc API client
│   ├── agent_service.py         # CrewAI orchestration
│   └── report_service.py        # PDF generation
│
├── webhook_server/
│   ├── main.py                  # FastAPI webhook receiver
│   └── tasks.py                 # Background tasks
│
├── finance_bot/                 # Existing CrewAI agents
│   ├── financial_planning/
│   └── tax_planning/
│
├── database/
│   ├── db.py                    # SQLite database
│   └── models.py                # Database models
│
├── reports/                     # PDF storage
│   └── +91XXXXXXXXXX/
│
├── requirements.txt
└── run.sh                       # Start everything
```

---

## User Flow (Simplified)

### 1. Login
```
User opens: streamlit run app.py
  ↓
Enter phone number: +919876543210
  ↓
Click "Send OTP" → Static OTP: 222222 (dev mode)
  ↓
Enter OTP → Click "Verify"
  ↓
Session created → Redirect to Dashboard
```

### 2. Dashboard
```
Dashboard shows:
  ├─ Welcome message
  ├─ Financial summary (from last call, or dummy data)
  ├─ Button: "Get Financial Advice" → Initiate call
  └─ List of generated reports
```

### 3. Generate Report Flow
```
User clicks "Get Financial Advice"
  ↓
Streamlit: pixpoc_client.initiate_call(phone_number)
  ↓
User receives call from Pixpoc AI
  ↓
Call completes → Pixpoc sends webhook to FastAPI server
  ↓
FastAPI background task:
  1. Fetch Pixpoc data (analysis + transcript + memory)
  2. Run CrewAI agent
  3. Generate PDF
  4. Save to database
  ↓
Streamlit dashboard auto-refreshes (st.rerun every 5 sec)
  ↓
New report appears → User clicks "Download PDF"
```

---

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create `.env` file:
```bash
# Pixpoc
PIXPOC_API_BASE_URL=https://devcallmanager.pixpoc.in
PIXPOC_API_KEY=your_api_key

# Database
DATABASE_PATH=./database/financebot.db

# Storage
REPORTS_PATH=./reports

# Webhook server
WEBHOOK_PORT=8000
WEBHOOK_HOST=0.0.0.0

# Streamlit
STREAMLIT_PORT=8501
```

### 3. Start Services

**Option A: Manual start (development)**
```bash
# Terminal 1: Webhook server
cd webhook_server
uvicorn main:app --reload --port 8000

# Terminal 2: Streamlit app
streamlit run streamlit_app/app.py --server.port 8501

# Terminal 3: Ollama (for agents)
ollama serve
```

**Option B: Single command (production)**
```bash
./run.sh
```

---

## Code Implementation

### Streamlit Main App
```python
# streamlit_app/app.py
import streamlit as st
from utils.session import init_session, is_authenticated
from components.auth import show_login_page
from components.dashboard import show_dashboard

st.set_page_config(
    page_title="FinanceBot",
    page_icon="💰",
    layout="wide"
)

# Initialize session
init_session()

# Main app logic
if not is_authenticated():
    show_login_page()
else:
    show_dashboard()
```

### Authentication Component
```python
# streamlit_app/components/auth.py
import streamlit as st

def show_login_page():
    st.title("🏦 Welcome to FinanceBot")
    st.markdown("Your AI-powered financial advisor")
    
    tab1, tab2 = st.tabs(["📱 Enter Phone", "🔐 Verify OTP"])
    
    with tab1:
        phone = st.text_input(
            "Mobile Number",
            placeholder="+919876543210",
            max_chars=13
        )
        
        if st.button("Send OTP", type="primary", use_container_width=True):
            if len(phone) == 13:
                st.session_state.phone_number = phone
                st.session_state.otp_sent = True
                st.success("OTP sent! Use: 222222")
                st.rerun()
            else:
                st.error("Invalid phone number")
    
    with tab2:
        if st.session_state.get("otp_sent"):
            otp = st.text_input("Enter OTP", max_chars=6, type="password")
            
            if st.button("Verify OTP", type="primary", use_container_width=True):
                if otp == "222222":  # Static OTP for dev
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "phone": st.session_state.phone_number,
                        "name": "User"
                    }
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid OTP")
        else:
            st.info("👈 First enter your phone number")
```

### Dashboard Component
```python
# streamlit_app/components/dashboard.py
import streamlit as st
from services.pixpoc_client import PixpocClient
from database.db import get_user_reports, get_user_financial_data

def show_dashboard():
    st.title(f"👋 Hello, {st.session_state.user['name']}!")
    
    # Financial Summary Cards
    col1, col2, col3 = st.columns(3)
    
    # Get user's financial data from database
    financial_data = get_user_financial_data(st.session_state.user['phone'])
    
    with col1:
        st.metric(
            label="💰 Monthly Income",
            value=f"₹{financial_data.get('income', 0):,}",
            delta="+5% from last month"
        )
    
    with col2:
        st.metric(
            label="💵 Savings",
            value=f"₹{financial_data.get('savings', 0):,}",
            delta="+₹10,000"
        )
    
    with col3:
        st.metric(
            label="💸 Expenses",
            value=f"₹{financial_data.get('expenses', 0):,}",
            delta="-₹5,000"
        )
    
    # Initiate Call Button
    st.divider()
    st.subheader("📞 Get Personalized Financial Advice")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Talk to our AI financial advisor and get a personalized report")
    with col2:
        if st.button("🎯 Start Call", type="primary", use_container_width=True):
            with st.spinner("Initiating call..."):
                initiate_pixpoc_call(st.session_state.user['phone'])
    
    # Reports Section
    st.divider()
    st.subheader("📄 Your Financial Reports")
    
    reports = get_user_reports(st.session_state.user['phone'])
    
    if reports:
        for report in reports:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{report['title']}**")
                    st.caption(f"Generated on {report['date']}")
                
                with col2:
                    st.write(f"📊 {report['type']}")
                
                with col3:
                    with open(report['path'], 'rb') as f:
                        st.download_button(
                            label="⬇️ Download",
                            data=f,
                            file_name=report['filename'],
                            mime="application/pdf"
                        )
    else:
        st.info("No reports yet. Start a call to generate your first report!")
    
    # Auto-refresh to check for new reports
    if st.session_state.get('call_in_progress'):
        st.write("⏳ Processing your call... Dashboard will update automatically")
        import time
        time.sleep(5)
        st.rerun()

def initiate_pixpoc_call(phone_number):
    """Initiate call through Pixpoc"""
    try:
        from services.pixpoc_client import PixpocClient
        import os
        
        client = PixpocClient(
            base_url=os.getenv("PIXPOC_API_BASE_URL"),
            api_key=os.getenv("PIXPOC_API_KEY")
        )
        
        result = client.initiate_call_sync(phone_number)
        
        st.session_state.call_in_progress = True
        st.session_state.current_call_id = result['callId']
        
        st.success("📞 Call initiated! You'll receive a call shortly.")
        st.info("The call will analyze your finances and generate a personalized report.")
        
        # Save to database
        from database.db import save_call
        save_call(phone_number, result['callId'])
        
    except Exception as e:
        st.error(f"Failed to initiate call: {str(e)}")
```

### Calculator Page
```python
# streamlit_app/pages/2_🧮_Calculators.py
import streamlit as st
from utils.helpers import calculate_sip, calculate_emi, format_currency

st.set_page_config(page_title="Calculators", page_icon="🧮", layout="wide")

st.title("🧮 Financial Calculators")

tab1, tab2, tab3 = st.tabs(["📈 SIP Calculator", "🏦 EMI Calculator", "💼 Tax Calculator"])

with tab1:
    st.header("SIP Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_amount = st.number_input("Monthly Investment (₹)", value=5000, step=500)
        expected_return = st.slider("Expected Return (%)", 1, 30, 12)
        time_period = st.slider("Investment Period (Years)", 1, 30, 10)
    
    with col2:
        result = calculate_sip(monthly_amount, expected_return, time_period)
        
        st.metric("Total Investment", format_currency(result['total_investment']))
        st.metric("Estimated Returns", format_currency(result['estimated_returns']))
        st.metric("Maturity Value", format_currency(result['maturity_value']))

with tab2:
    st.header("EMI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input("Loan Amount (₹)", value=1000000, step=50000)
        interest_rate = st.slider("Interest Rate (%)", 1.0, 20.0, 8.5, 0.1)
        tenure = st.slider("Tenure (Years)", 1, 30, 20)
    
    with col2:
        result = calculate_emi(loan_amount, interest_rate, tenure * 12)
        
        st.metric("Monthly EMI", format_currency(result['emi']))
        st.metric("Total Interest", format_currency(result['total_interest']))
        st.metric("Total Amount", format_currency(result['total_amount']))

with tab3:
    st.header("Income Tax Calculator")
    st.info("Coming soon! This will compare Old vs New tax regimes.")
```

### Simplified Database (SQLite)
```python
# database/db.py
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "financebot.db"

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT,
            last_login TEXT
        )
    ''')
    
    # Calls table
    c.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            call_id TEXT UNIQUE,
            contact_id TEXT,
            status TEXT,
            created_at TEXT,
            completed_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number)
        )
    ''')
    
    # Reports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            phone_number TEXT,
            call_id TEXT,
            type TEXT,
            filename TEXT,
            file_path TEXT,
            created_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number)
        )
    ''')
    
    # Financial data table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_financial_data (
            phone_number TEXT PRIMARY KEY,
            income REAL,
            savings REAL,
            expenses REAL,
            data_json TEXT,
            updated_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_reports(phone_number):
    """Get all reports for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT id, type, filename, file_path, created_at 
        FROM reports 
        WHERE phone_number = ?
        ORDER BY created_at DESC
    ''', (phone_number,))
    
    reports = []
    for row in c.fetchall():
        reports.append({
            'id': row[0],
            'type': row[1],
            'filename': row[2],
            'path': row[3],
            'date': row[4],
            'title': f"{row[1].replace('_', ' ').title()} Report"
        })
    
    conn.close()
    return reports

def get_user_financial_data(phone_number):
    """Get user's financial summary"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT income, savings, expenses, data_json
        FROM user_financial_data
        WHERE phone_number = ?
    ''', (phone_number,))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'income': row[0] or 75000,
            'savings': row[1] or 25000,
            'expenses': row[2] or 50000,
            'data': json.loads(row[3]) if row[3] else {}
        }
    
    # Return dummy data if no data exists
    return {'income': 75000, 'savings': 25000, 'expenses': 50000, 'data': {}}

def save_call(phone_number, call_id, contact_id=None):
    """Save call record"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO calls (phone_number, call_id, contact_id, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (phone_number, call_id, contact_id, 'initiated', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def update_call_status(call_id, status):
    """Update call status"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE calls 
        SET status = ?, completed_at = ?
        WHERE call_id = ?
    ''', (status, datetime.now().isoformat(), call_id))
    
    conn.commit()
    conn.close()

def save_report(phone_number, report_id, call_id, report_type, filename, file_path):
    """Save report record"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO reports (id, phone_number, call_id, type, filename, file_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (report_id, phone_number, call_id, report_type, filename, file_path, 
          datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def update_financial_data(phone_number, income, savings, expenses, data_dict):
    """Update user's financial data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT OR REPLACE INTO user_financial_data 
        (phone_number, income, savings, expenses, data_json, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (phone_number, income, savings, expenses, json.dumps(data_dict),
          datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()
```

### Updated Requirements
```txt
# requirements.txt

# Streamlit
streamlit==1.29.0

# FastAPI (for webhook server)
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlite3  # Built-in with Python

# Pixpoc & HTTP
httpx==0.25.1
requests==2.31.0

# PDF Generation
markdown==3.5.1
weasyprint==60.1

# CrewAI & AI
crewai==0.1.0
langchain==0.1.0
duckduckgo-search==4.1.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
loguru==0.7.2

# Date/Time
python-dateutil==2.8.2
```

This is much simpler! Everything in Python, Streamlit for UI, SQLite for database (no complex setup), and the same powerful CrewAI agents. Want me to continue with the webhook server and startup script?

