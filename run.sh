#!/bin/bash

# FinanceBot Startup Script
# Starts all required services

set -e  # Exit on error

echo "🚀 Starting FinanceBot..."
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if core dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing dependencies (this may take a minute)..."
    pip install streamlit fastapi "uvicorn[standard]" httpx requests markdown python-dotenv plotly loguru pyyaml
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from database.db import init_db; init_db()"

# Create reports directory
mkdir -p reports
echo "✅ Reports directory ready"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating default..."
    cat > .env << 'EOF'
# Pixpoc API Configuration
PIXPOC_API_BASE_URL=https://app.pixpoc.ai
PIXPOC_API_KEY=your_api_key_here
PIXPOC_AGENT_ID=your_agent_id_here

# Database Configuration
DATABASE_PATH=./database/financebot.db

# File Storage
REPORTS_PATH=./reports

# Server Configuration
WEBHOOK_HOST=127.0.0.1
WEBHOOK_PORT=8000
STREAMLIT_PORT=8501

# Ollama Configuration (for AI agents)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral-nemo

# Public Webhook URL (for Pixpoc callbacks)
# WEBHOOK_URL=https://your-domain.com/webhook/pixpoc
EOF
    echo "✅ .env file created with defaults"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Pixpoc credentials:"
    echo "   - PIXPOC_API_KEY: Get from https://app.pixpoc.ai"
    echo "   - PIXPOC_AGENT_ID: Your AI agent UUID"
fi

echo ""
echo "🔧 Starting services..."
echo ""

# Start webhook server in background
echo "📡 Starting webhook server on port 8000..."
cd webhook_server
nohup uvicorn main:app --host 127.0.0.1 --port 8000 > ../logs/webhook.log 2>&1 &
WEBHOOK_PID=$!
cd ..
sleep 2

if ps -p $WEBHOOK_PID > /dev/null; then
    echo "✅ Webhook server running (PID: $WEBHOOK_PID)"
else
    echo "❌ Webhook server failed to start"
    echo "   Check logs/webhook.log for details"
fi

# Start Streamlit app in background
echo "🌐 Starting Streamlit app on port 8501..."
mkdir -p logs
nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!
sleep 3

if ps -p $STREAMLIT_PID > /dev/null; then
    echo "✅ Streamlit app running (PID: $STREAMLIT_PID)"
else
    echo "❌ Streamlit app failed to start"
    echo "   Check logs/streamlit.log for details"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ FinanceBot is running!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📱 Streamlit App:    http://localhost:8501"
echo "🔌 Webhook Server:   http://localhost:8000"
echo "📚 API Docs:         http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   - Webhook:        logs/webhook.log"
echo "   - Streamlit:      logs/streamlit.log"
echo ""
echo "🔐 Test Login:"
echo "   - Phone:          9876543210"
echo "   - OTP:            222222"
echo ""
echo "🛑 To stop: ./stop.sh or kill $WEBHOOK_PID $STREAMLIT_PID"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Save PIDs to file for easy stopping
echo "$WEBHOOK_PID" > .webhook.pid
echo "$STREAMLIT_PID" > .streamlit.pid

echo "💡 Services running in background. You can close this terminal."
echo "   View logs with: tail -f logs/streamlit.log"
echo ""

