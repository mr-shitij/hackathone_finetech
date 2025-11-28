# FinanceBot - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- Ollama (for AI agents)
- Git

### 1. Clone & Setup

```bash
# Clone repository
git clone <your-repo>
cd FinanceBot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your Pixpoc API key
nano .env  # or use your preferred editor
```

**Required Configuration:**
```env
PIXPOC_API_KEY=your_api_key_here
```

### 3. Start Ollama (for AI Agents)

```bash
# In a separate terminal
ollama serve
ollama pull mistral-nemo
```

### 4. Run FinanceBot

**Option A: Using the startup script (recommended)**
```bash
chmod +x run.sh
./run.sh
```

**Option B: Manual start**
```bash
# Terminal 1: Webhook server
cd webhook_server
uvicorn main:app --reload --port 8000

# Terminal 2: Streamlit app
streamlit run streamlit_app/app.py --server.port 8501
```

### 5. Access the App

- **Streamlit UI:** http://localhost:8501
- **Webhook API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📱 Using the App

### Login
1. Open http://localhost:8501
2. Enter phone number: `+919876543210` (or any 10-digit number)
3. Click "Send OTP"
4. Enter OTP: `222222` (static for testing)
5. Click "Verify"

### Generate Report
1. From dashboard, click "Start AI Call"
2. You'll receive a call from Pixpoc AI (if configured)
3. Answer questions about your finances
4. After call ends, report will be auto-generated
5. Download PDF from dashboard

### Use Calculators
1. Go to "Calculators" page
2. Use SIP, EMI, or Tax calculators
3. Get instant calculations

---

## 🧪 Testing Without Pixpoc

If you don't have Pixpoc API access yet:

1. **Mock the webhook callback:**
```bash
curl -X POST http://localhost:8000/webhook/pixpoc \
  -H "Content-Type: application/json" \
  -d '{
    "callId": "test-call-123",
    "contactId": "test-contact-456",
    "status": "COMPLETED",
    "duration": 300
  }'
```

2. **Check logs** to see processing

3. **View generated reports** in `/reports/+919876543210/`

---

## 📁 Project Structure

```
FinanceBot/
├── streamlit_app/           # Streamlit UI
│   ├── app.py              # Main app
│   ├── components/         # Reusable components
│   └── pages/              # Additional pages
├── webhook_server/         # FastAPI webhook receiver
│   └── main.py
├── services/               # Business logic
│   ├── pixpoc_client.py
│   ├── agent_service.py
│   └── report_service.py
├── database/               # SQLite database
│   └── db.py
├── finance_bot/            # CrewAI agents
│   ├── financial_planning/
│   └── tax_planning/
└── reports/                # Generated PDFs
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Pull model
ollama pull mistral-nemo
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Database Issues
```bash
# Delete and recreate database
rm database/financebot.db
python -c "from database.db import init_db; init_db()"
```

---

## 🎯 Next Steps

1. **Get Pixpoc API Key** - Contact Pixpoc for production access
2. **Configure Webhook URL** - Set up ngrok or deploy to get public URL
3. **Customize Agents** - Modify CrewAI agents in `/finance_bot/`
4. **Add More Calculators** - Extend calculator pages
5. **Deploy** - Deploy to cloud (Streamlit Cloud, Railway, etc.)

---

## 📚 Documentation

- **Architecture:** See `SIMPLIFIED_ARCHITECTURE.md`
- **Pixpoc API:** See `API_CALL_ANALYSIS_TRANSCRIPT_CONTACT.md`
- **Agent Specs:** See `docs/agent-specifications.md`

---

## 🆘 Support

- Check logs in terminal
- Review error messages in Streamlit
- Webhook logs at http://localhost:8000
- Database check: Use SQLite viewer

---

## 🎉 You're Ready!

Start exploring FinanceBot and get personalized financial advice powered by AI!

