# Troubleshooting 503 Error on `/api/calls/initiate`

## Problem
Getting `503 Service Unavailable` when trying to initiate a call.

## Common Causes & Solutions

### 1. Python Backend Not Running ✅ **MOST COMMON**

**Check:**
```bash
# Check if backend is running on port 8000
curl http://localhost:8000/health
```

**Solution:**
```bash
# Start the Python backend
cd webhook_server
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Wrong Backend URL

**Check:**
- The Next.js API route uses `process.env.BACKEND_URL || "http://localhost:8000"`
- Make sure the backend is accessible at this URL

**Solution:**
Create `.env.local` in the `dashboard` directory:
```env
BACKEND_URL=http://localhost:8000
```

Or if your backend runs on a different port:
```env
BACKEND_URL=http://localhost:8001
```

### 3. Backend Endpoint Not Found

**Check:**
```bash
# Test the endpoint directly
curl -X POST http://localhost:8000/api/calls/initiate \
  -H "Content-Type: application/json" \
  -d '{"phone": "+919876543210", "name": "Test User"}'
```

**Solution:**
- Make sure `webhook_server/main.py` has the `/api/calls/initiate` endpoint
- Restart the backend server after making changes

### 4. CORS Issues (if backend is on different domain)

**Solution:**
Add CORS middleware to FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Missing Environment Variables

**Check:**
The backend needs these in `.env`:
```env
PIXPOC_API_BASE_URL=https://app.pixpoc.ai
PIXPOC_API_KEY=your_api_key
PIXPOC_AGENT_ID=your_agent_id
PIXPOC_FROM_NUMBER_ID=your_from_number_id
```

**Solution:**
- Create `.env` file in project root
- Add all required Pixpoc credentials
- Restart backend server

## Debugging Steps

### Step 1: Check Backend Health
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"healthy","service":"financebot-webhook"}`

### Step 2: Check Backend Endpoints
```bash
curl http://localhost:8000/
```
Should list all available endpoints

### Step 3: Test Call Initiation Directly
```bash
curl -X POST http://localhost:8000/api/calls/initiate \
  -H "Content-Type: application/json" \
  -d '{"phone": "+919876543210", "name": "Test User"}'
```

### Step 4: Check Next.js Console
- Open browser DevTools → Console
- Look for error messages
- Check Network tab for the failed request

### Step 5: Check Backend Logs
Look at the terminal where you started the backend server for error messages.

## Quick Fix Checklist

- [ ] Python backend is running (`uvicorn main:app --reload --port 8000`)
- [ ] Backend responds to `/health` endpoint
- [ ] `.env` file exists with Pixpoc credentials
- [ ] Backend endpoint `/api/calls/initiate` exists
- [ ] Next.js can reach `http://localhost:8000`
- [ ] No firewall blocking port 8000
- [ ] Backend logs show no errors

## Expected Behavior

When working correctly:
1. User clicks "Start AI Call" in dashboard
2. Next.js calls `/api/calls/initiate` (Next.js API route)
3. Next.js API route calls `http://localhost:8000/api/calls/initiate` (Python backend)
4. Python backend initiates Pixpoc call
5. Success response returned to frontend
6. Toast notification shows "Call Initiated"

## Error Messages

### "Backend service unavailable"
→ Backend server is not running or not reachable

### "PIXPOC_AGENT_ID not configured"
→ Missing environment variable in `.env`

### "Phone number required"
→ Frontend didn't send phone number (check user session)

### Network error in browser console
→ Backend URL is wrong or server is down

