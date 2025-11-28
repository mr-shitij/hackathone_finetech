# 💰 FinanceBot - AI-Powered Financial Advisory Platform

> **All-Python, Streamlit-based financial advisory system powered by AI agents**

FinanceBot provides personalized financial planning through AI-powered voice conversations and generates comprehensive financial reports.

---

## ✨ Features

- 🎯 **Voice-based Data Collection** - Talk to AI agents via Pixpoc.ai
- 📊 **Personalized Financial Reports** - AI-generated PDF reports  
- 🧮 **Financial Calculators** - SIP, EMI, and Tax calculators
- 📱 **Clean Streamlit UI** - Simple, intuitive interface
- 🤖 **Multi-Agent System** - CrewAI-powered financial analysis
- 💾 **SQLite Database** - No complex setup required

---

## 🚀 Quick Start

### 1. Install & Configure

```bash
# Clone repository
git clone <your-repo>
cd FinanceBot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your PIXPOC_API_KEY
```

### 2. Start Services

```bash
# Start everything with one command
./run.sh
```

Or manually:

```bash
# Terminal 1: Webhook server
cd webhook_server && uvicorn main:app --port 8000

# Terminal 2: Streamlit app
streamlit run streamlit_app/app.py

# Terminal 3: Ollama (for AI agents)
ollama serve && ollama pull mistral-nemo
```

### 3. Access the App

- **Streamlit UI:** http://localhost:8501
- **Webhook API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📖 User Journey

### Step 1: Login
```
1. Open http://localhost:8501
2. Enter phone number: +919876543210
3. Enter OTP: 222222 (test OTP)
4. Access dashboard
```

### Step 2: Dashboard
```
- View financial summary (income, savings, expenses)
- See savings rate and trends
- Access calculators
- View past reports
```

### Step 3: Generate Report
```
1. Click "Start AI Call" button
2. Receive call from Pixpoc AI agent
3. Answer questions about finances:
   - Income sources
   - Monthly expenses
   - Financial goals
   - Risk tolerance
   - Insurance coverage
4. Call ends → Processing starts automatically
5. Dashboard auto-refreshes
6. Download PDF report when ready
```

### Step 4: Download & Review
```
- Click download button
- Get professional PDF report with:
  ✓ Financial health analysis
  ✓ Personalized recommendations
  ✓ Goal-based roadmap
  ✓ Investment strategy
  ✓ Tax optimization tips
```

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                  STREAMLIT UI                          │
│  Login → Dashboard → Calculators → Reports             │
└────────────────┬───────────────────────────────────────┘
                 │
                 ↓
┌────────────────────────────────────────────────────────┐
│              PYTHON SERVICES                           │
│  • pixpoc_client.py    (API integration)               │
│  • agent_service.py    (CrewAI orchestration)          │
│  • report_service.py   (PDF generation)                │
└────────────────┬───────────────────────────────────────┘
                 │
        ┌────────┼───────┬────────────┬────────┐
        │        │       │            │        │
    ┌───▼──┐ ┌──▼───┐ ┌─▼──────┐ ┌───▼────┐  │
    │Pixpoc│ │CrewAI│ │ SQLite │ │ Files  │  │
    │ API  │ │Agents│ │   DB   │ │/reports│  │
    └──────┘ └──────┘ └────────┘ └────────┘  │
                                              │
                ┌─────────────────────────────▼──┐
                │    FastAPI Webhook Server      │
                │  (Receives Pixpoc callbacks)   │
                └────────────────────────────────┘
```

---

## 📁 Project Structure

```
FinanceBot/
├── streamlit_app/              # Streamlit UI
│   ├── app.py                 # Main app
│   ├── components/
│   │   ├── auth.py            # Login/OTP
│   │   └── dashboard.py       # Dashboard UI
│   ├── pages/
│   │   ├── calculators.py     # Financial calculators
│   │   ├── reports.py         # Report listing
│   │   └── profile.py         # User profile
│   └── utils/
│       ├── session.py         # Session management
│       └── helpers.py         # Utility functions
│
├── webhook_server/             # FastAPI webhook receiver
│   └── main.py                # Webhook endpoints
│
├── services/                   # Business logic
│   ├── pixpoc_client.py       # Pixpoc API client
│   ├── agent_service.py       # Agent orchestration
│   └── report_service.py      # PDF generation
│
├── database/                   # SQLite database
│   └── db.py                  # Database operations
│
├── finance_bot/                # CrewAI agents (existing)
│   ├── financial_planning/
│   │   ├── main.py
│   │   ├── config/
│   │   └── tools/
│   └── tax_planning/
│       ├── main.py
│       ├── config/
│       └── tools/
│
├── reports/                    # Generated PDFs (organized by phone)
│   └── +91XXXXXXXXXX/
│       ├── financial_plan_2025-11-28.pdf
│       └── tax_plan_2025-11-28.pdf
│
├── docs/                       # Documentation
│   └── agent-specifications.md
│
├── requirements.txt            # Python dependencies
├── run.sh                      # Startup script
├── .env.example               # Environment template
├── QUICKSTART.md              # Quick start guide
├── SIMPLIFIED_ARCHITECTURE.md # Architecture doc
└── README.md                  # This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Webhook Server** | FastAPI |
| **Database** | SQLite |
| **AI Agents** | CrewAI |
| **LLM** | Ollama (Mistral-Nemo) |
| **PDF Generation** | WeasyPrint |
| **Voice AI** | Pixpoc.ai |

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Pixpoc API (Required)
PIXPOC_API_BASE_URL=https://devcallmanager.pixpoc.in
PIXPOC_API_KEY=your_api_key_here

# Database
DATABASE_PATH=./database/financebot.db

# Storage
REPORTS_PATH=./reports

# Webhook Server
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000

# Streamlit
STREAMLIT_PORT=8501

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral-nemo
```

---

## 🧮 Available Calculators

### 1. SIP Calculator
Calculate returns on Systematic Investment Plans
- Inputs: Monthly amount, expected return, time period
- Outputs: Total investment, returns, maturity value

### 2. EMI Calculator
Calculate loan EMIs
- Inputs: Loan amount, interest rate, tenure
- Outputs: Monthly EMI, total interest, total amount

### 3. Tax Calculator
*(Coming soon)* Compare old vs new tax regimes

---

## 🤖 AI Agents

### Financial Planning Agent
- Analyzes income, expenses, assets, liabilities
- Creates goal-based financial roadmap
- Recommends investment strategies
- Suggests insurance coverage
- Provides retirement planning

### Tax Planning Agent
- Calculates tax liability (old vs new regime)
- Identifies tax-saving opportunities
- Recommends deductions (80C, 80D, etc.)
- Provides actionable tax strategies

---

## 🔄 Complete Flow

```
1. User Login (OTP)
   ↓
2. Dashboard (Financial Summary)
   ↓
3. Click "Start AI Call"
   ↓
4. Pixpoc calls user → AI conversation
   ↓
5. Call ends → Webhook triggered
   ↓
6. Background Processing:
   - Fetch Pixpoc data (analysis + transcript + memory)
   - Parse financial information
   - Run CrewAI agent
   - Generate Markdown report
   - Convert to PDF
   - Save to database
   ↓
7. Dashboard updates automatically
   ↓
8. User downloads PDF report
```

---

## 📊 Database Schema

```sql
users (phone_number, name, email, created_at, last_login)
calls (id, phone_number, call_id, status, created_at, completed_at)
reports (id, phone_number, call_id, type, filename, file_path, created_at)
user_financial_data (phone_number, income, savings, expenses, data_json)
```

---

## 🧪 Testing

### Test Without Pixpoc

```bash
# Mock webhook callback
curl -X POST http://localhost:8000/webhook/pixpoc \
  -H "Content-Type: application/json" \
  -d '{
    "callId": "test-123",
    "contactId": "contact-456",
    "status": "COMPLETED"
  }'
```

### Test Login

- Phone: Any 10-digit number (e.g., `9876543210`)
- OTP: `222222` (static for testing)

---

## 📚 Documentation

- **Quick Start:** `QUICKSTART.md`
- **Architecture:** `SIMPLIFIED_ARCHITECTURE.md`
- **Agent Specs:** `docs/agent-specifications.md`
- **Pixpoc API:** `API_CALL_ANALYSIS_TRANSCRIPT_CONTACT.md`

---

## 🚢 Deployment

### Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Deploy on Streamlit Cloud
# https://streamlit.io/cloud
```

### Railway / Render
```bash
# Configure build command
pip install -r requirements.txt

# Configure start command
./run.sh
```

---

## 🔒 Security

- ✅ OTP-based authentication
- ✅ Session management
- ✅ User data isolation (by phone number)
- ✅ Secure API key handling
- ✅ Database access controls

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 💬 Support

- **Documentation:** See `/docs/` folder
- **Issues:** GitHub Issues
- **Email:** support@financebot.com

---

## 🎉 You're Ready!

Start FinanceBot and get personalized financial advice powered by AI!

```bash
./run.sh
```

Then open http://localhost:8501 and start exploring! 🚀


