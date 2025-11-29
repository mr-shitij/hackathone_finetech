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

# Check if core Python dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing Python dependencies (this may take a minute)..."
    pip install fastapi "uvicorn[standard]" httpx requests markdown python-dotenv plotly loguru pyyaml
    echo "✅ Python dependencies installed"
else
    echo "✅ Python dependencies already installed"
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
NEXTJS_PORT=3000

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

# Create logs directory if it doesn't exist
mkdir -p logs

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

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "   Please install Node.js from https://nodejs.org/"
    echo "   Or use: brew install node (on macOS)"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

# Setup dashboard environment file
echo "⚙️  Checking dashboard environment..."
cd dashboard
if [ ! -f ".env.local" ]; then
    echo "📝 Creating dashboard/.env.local from root .env..."
    if [ -f "../.env" ]; then
        # Extract Pixpoc variables from root .env and create .env.local
        grep -E "^PIXPOC_" ../.env > .env.local 2>/dev/null || true
        echo "BACKEND_URL=http://localhost:8000" >> .env.local
        echo "✅ Created .env.local"
        echo "⚠️  Review dashboard/.env.local and update if needed"
    else
        echo "⚠️  No .env file found. Creating default .env.local..."
        cat > .env.local << 'EOF'
# Pixpoc API Configuration (from root .env)
PIXPOC_API_BASE_URL=https://app.pixpoc.ai
PIXPOC_API_KEY=your_api_key_here
PIXPOC_AGENT_ID=your_agent_id_here
PIXPOC_FROM_NUMBER_ID=your_from_number_id_here

# Backend API URL
BACKEND_URL=http://localhost:8000
EOF
        echo "⚠️  IMPORTANT: Edit dashboard/.env.local and add your Pixpoc credentials"
    fi
else
    echo "✅ Dashboard .env.local exists"
fi

# Install Next.js dependencies if needed
echo "📦 Checking Next.js dependencies..."
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Next.js dependencies (this may take a minute)..."
    npm install
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi
cd ..

# Start Next.js dashboard in background
echo "🌐 Starting Next.js dashboard on port 3000..."
mkdir -p logs
cd dashboard
nohup npm run dev > ../logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
cd ..
sleep 5

if ps -p $DASHBOARD_PID > /dev/null; then
    echo "✅ Next.js dashboard running (PID: $DASHBOARD_PID)"
else
    echo "❌ Next.js dashboard failed to start"
    echo "   Check logs/dashboard.log for details"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ FinanceBot is running!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🎨 Next.js Dashboard: http://localhost:3000"
echo "🔌 Webhook Server:    http://localhost:8000"
echo "📚 API Docs:          http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   - Webhook:         logs/webhook.log"
echo "   - Dashboard:       logs/dashboard.log"
echo ""
echo "🔐 Test Login:"
echo "   - Phone:           +919876543210 (or any 10-digit)"
echo "   - OTP:             222222"
echo ""
echo "⚠️  Environment Setup:"
echo "   - Make sure .env has PIXPOC_API_KEY, PIXPOC_AGENT_ID"
echo "   - Dashboard uses .env.local (copy from .env if needed)"
echo ""
echo "🛑 To stop: ./stop.sh or kill $WEBHOOK_PID $DASHBOARD_PID"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Save PIDs to file for easy stopping
echo "$WEBHOOK_PID" > .webhook.pid
echo "$DASHBOARD_PID" > .dashboard.pid

echo "💡 Services running in background. You can close this terminal."
echo "   View logs with: tail -f logs/dashboard.log"
echo ""

