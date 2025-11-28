#!/bin/bash

# FinanceBot Stop Script
# Stops all running services

echo "🛑 Stopping FinanceBot services..."

# Kill webhook server
if [ -f ".webhook.pid" ]; then
    WEBHOOK_PID=$(cat .webhook.pid)
    if ps -p $WEBHOOK_PID > /dev/null 2>&1; then
        kill $WEBHOOK_PID
        echo "✅ Webhook server stopped (PID: $WEBHOOK_PID)"
    fi
    rm .webhook.pid
fi

# Kill Streamlit app
if [ -f ".streamlit.pid" ]; then
    STREAMLIT_PID=$(cat .streamlit.pid)
    if ps -p $STREAMLIT_PID > /dev/null 2>&1; then
        kill $STREAMLIT_PID
        echo "✅ Streamlit app stopped (PID: $STREAMLIT_PID)"
    fi
    rm .streamlit.pid
fi

# Also kill any remaining uvicorn/streamlit processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "streamlit run" 2>/dev/null

echo "✅ All services stopped"

