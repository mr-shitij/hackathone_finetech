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

# Kill Next.js dashboard
if [ -f ".dashboard.pid" ]; then
    DASHBOARD_PID=$(cat .dashboard.pid)
    if ps -p $DASHBOARD_PID > /dev/null 2>&1; then
        kill $DASHBOARD_PID
        echo "✅ Next.js dashboard stopped (PID: $DASHBOARD_PID)"
    fi
    rm .dashboard.pid
fi

# Also kill any remaining uvicorn/next/streamlit processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "next dev" 2>/dev/null
pkill -f "next start" 2>/dev/null
pkill -f "streamlit run" 2>/dev/null

echo "✅ All services stopped"

