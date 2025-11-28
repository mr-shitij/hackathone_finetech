# FinanceBot - Complete System Flow

## Overview
FinanceBot is an AI-powered financial advisory platform that combines voice-based data collection (via Pixpoc.ai) with multi-agent financial analysis (CrewAI) to deliver personalized financial reports.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  1. AUTHENTICATION (Frontend - Next.js)                              │
│     - User enters mobile number                                      │
│     - OTP verification (222222 for testing)                          │
│     - Session created in localStorage                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. DASHBOARD INITIAL VIEW (Frontend)                                │
│     - Show dummy data (usage patterns, spending, income)             │
│     - Welcome message                                                │
│     - "Generate Financial Report" button                             │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. TRIGGER PIXPOC CALL (Backend API)                                │
│     POST /api/user/initiate-call                                     │
│     {                                                                │
│       "phoneNumber": "+91XXXXXXXXXX",                                │
│       "userId": "user_id"                                            │
│     }                                                                │
│                                                                      │
│     → Calls Pixpoc API to initiate voice call                        │
│     → User receives call and converses with AI agent                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. PIXPOC CALLBACK (Webhook)                                        │
│     POST /api/webhooks/pixpoc/call-completed                         │
│     {                                                                │
│       "callId": "call-uuid",                                         │
│       "callSid": "CA123...",                                         │
│       "contactId": "clx1234567890abcdef",                            │
│       "status": "COMPLETED",                                         │
│       "duration": 450                                                │
│     }                                                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. FETCH PIXPOC DATA (Backend)                                      │
│                                                                      │
│  A. Get Call Analysis                                                │
│     GET /api/v1/calls/{callId}/analysis                              │
│     X-API-Key: <pixpoc_api_key>                                      │
│     → Returns: sentiment, summary, key points, action items          │
│                                                                      │
│  B. Get Call Transcript                                              │
│     GET /api/v1/calls/{callId}/transcript                            │
│     X-API-Key: <pixpoc_api_key>                                      │
│     → Returns: Full conversation transcript                          │
│                                                                      │
│  C. Get Contact Metadata                                             │
│     GET /api/v1/contacts/{contactId}/metadata                        │
│     X-API-Key: <pixpoc_api_key>                                      │
│     → Returns: {                                                     │
│         "contactId": "...",                                          │
│         "phoneNumber": "+91...",                                     │
│         "metadata": {                                                │
│           "name": "...",                                             │
│           "memory": {  // EXTRACTED FINANCIAL DATA                   │
│             "income": { ... },                                       │
│             "expenses": { ... },                                     │
│             "goals": [ ... ],                                        │
│             "assets": { ... },                                       │
│             "liabilities": { ... }                                   │
│           }                                                          │
│         }                                                            │
│       }                                                              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  6. PARSE & STRUCTURE DATA (Backend)                                 │
│     - Extract memory field from contact metadata                     │
│     - Parse transcript for additional context                        │
│     - Combine analysis + memory into structured JSON                 │
│     - Determine which agent to trigger based on analysis             │
│                                                                      │
│     Example structured data:                                         │
│     {                                                                │
│       "user_id": "USER_12345",                                       │
│       "personal_info": {                                             │
│         "name": "...",                                               │
│         "age": 30,                                                   │
│         "phone": "+91...",                                           │
│         "occupation": "..."                                          │
│       },                                                             │
│       "financials": {                                                │
│         "income": { ... },                                           │
│         "expenses": { ... },                                         │
│         "assets": { ... },                                           │
│         "liabilities": { ... }                                       │
│       },                                                             │
│       "goals": [ ... ],                                              │
│       "risk_profile": "...",                                         │
│       "agent_type": "financial_planning" // or "tax_planning"        │
│     }                                                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  7. TRIGGER FINANCE AGENTS (Backend - CrewAI)                        │
│                                                                      │
│  Option A: Financial Planning Agent                                  │
│     from finance_bot.financial_planning.main import                  │
│         FinancialPlanningCrew                                        │
│                                                                      │
│     crew = FinancialPlanningCrew(user_data)                          │
│     result = crew.run()  # Returns Markdown report                   │
│                                                                      │
│  Option B: Tax Planning Agent                                        │
│     from finance_bot.tax_planning.main import TaxPlanningCrew        │
│                                                                      │
│     crew = TaxPlanningCrew(user_tax_data)                            │
│     result = crew.run()  # Returns Markdown report                   │
│                                                                      │
│  → Multi-agent workflow executes:                                    │
│    - Analysis agents analyze data                                    │
│    - Research agents find best products                              │
│    - Strategy agents create recommendations                          │
│    - Report generators compile final report                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  8. CONVERT MD TO PDF (Backend)                                      │
│     - Receive Markdown report from CrewAI agents                     │
│     - Convert to PDF using library (markdown-pdf, weasyprint)        │
│     - Add branding, formatting, charts                               │
│     - Generate filename: {phone_number}_{report_type}_{timestamp}.pdf│
│                                                                      │
│     Storage structure:                                               │
│     reports/                                                         │
│       └── +91XXXXXXXXXX/                                             │
│           ├── financial_plan_2025-11-28.pdf                          │
│           ├── tax_plan_2025-11-28.pdf                                │
│           └── metadata.json                                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  9. STORE REPORT & UPDATE DATABASE (Backend)                         │
│     - Save PDF to: /reports/{phoneNumber}/                           │
│     - Update database:                                               │
│       {                                                              │
│         "userId": "...",                                             │
│         "phoneNumber": "+91...",                                     │
│         "reports": [                                                 │
│           {                                                          │
│             "type": "financial_planning",                            │
│             "createdAt": "2025-11-28T...",                           │
│             "filePath": "/reports/+91.../financial_plan.pdf",        │
│             "status": "completed",                                   │
│             "callId": "call-uuid",                                   │
│             "summary": "Net worth: ₹X, Savings rate: Y%"             │
│           }                                                          │
│         ],                                                           │
│         "latestAnalysis": {                                          │
│           "netWorth": 450000,                                        │
│           "monthlyIncome": 75000,                                    │
│           "monthlyExpenses": 50000,                                  │
│           "savingsRate": 33.3                                        │
│         }                                                            │
│       }                                                              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  10. UPDATE DASHBOARD (Frontend)                                     │
│      GET /api/user/dashboard                                         │
│      {                                                               │
│        "user": { ... },                                              │
│        "financialSummary": {                                         │
│          "income": 75000,                                            │
│          "savings": 25000,                                           │
│          "expenses": 50000,                                          │
│          "netWorth": 450000                                          │
│        },                                                            │
│        "reports": [                                                  │
│          {                                                           │
│            "title": "Financial Plan Report",                         │
│            "date": "Nov 28, 2025",                                   │
│            "downloadUrl": "/api/reports/download/...",               │
│            "thumbnail": "..."                                        │
│          }                                                           │
│        ],                                                            │
│        "insights": [                                                 │
│          "Your savings rate is 33% - Great job!",                    │
│          "Consider investing in ELSS for tax savings"                │
│        ]                                                             │
│      }                                                               │
│                                                                      │
│      Dashboard displays:                                             │
│      ✓ Real financial data (from Pixpoc + agents)                    │
│      ✓ List of generated reports with download links                 │
│      ✓ Key insights and recommendations                              │
│      ✓ Charts and visualizations                                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  11. USER DOWNLOADS REPORT (Frontend)                                │
│      - User clicks "Download Report" button                          │
│      - GET /api/reports/download/{reportId}                          │
│      - Backend streams PDF file                                      │
│      - User receives personalized financial plan                     │
└─────────────────────────────────────────────────────────────────────┘

---

## API Endpoints Design

### Backend API (New - To Be Created)

```
POST   /api/auth/send-otp
POST   /api/auth/verify-otp
GET    /api/user/profile
GET    /api/user/dashboard

POST   /api/calls/initiate          # Trigger Pixpoc call
POST   /api/webhooks/pixpoc/callback # Receive Pixpoc callback

GET    /api/reports                 # List all user reports
GET    /api/reports/:reportId       # Get specific report details
GET    /api/reports/download/:reportId # Download PDF

POST   /api/agents/trigger          # Manual trigger for agents (dev/testing)
GET    /api/agents/status/:jobId    # Check agent processing status
```

---

## Data Flow Sequence

```
1. User Login
   Frontend → Backend: POST /api/auth/send-otp
   Frontend → Backend: POST /api/auth/verify-otp
   Backend → Frontend: { token, user }

2. Dashboard Load
   Frontend → Backend: GET /api/user/dashboard
   Backend → Frontend: { user, financialSummary, reports }

3. Initiate Call
   Frontend → Backend: POST /api/calls/initiate
   Backend → Pixpoc: POST /api/calls (outbound call API)
   Pixpoc → User: Phone call
   User ↔ Pixpoc: Voice conversation

4. Call Completion
   Pixpoc → Backend: POST /api/webhooks/pixpoc/callback
   Backend → Pixpoc: GET /api/v1/calls/{callId}/analysis
   Backend → Pixpoc: GET /api/v1/calls/{callId}/transcript
   Backend → Pixpoc: GET /api/v1/contacts/{contactId}/metadata

5. Agent Processing
   Backend → CrewAI: FinancialPlanningCrew(user_data).run()
   CrewAI Agents: Execute multi-agent workflow
   CrewAI → Backend: Markdown report

6. Report Generation
   Backend: Convert MD → PDF
   Backend: Save PDF to /reports/{phone}/
   Backend: Update database

7. Dashboard Update
   Frontend → Backend: GET /api/user/dashboard (polling or WebSocket)
   Backend → Frontend: Updated data with new report
   Frontend: Display report with download button
```

---

## Technology Stack Integration

### Frontend (Next.js)
- **Framework**: Next.js 14 (App Router)
- **State**: Zustand for auth, SWR/React Query for data fetching
- **Real-time**: WebSockets or polling for report status

### Backend (Python - FastAPI/Flask)
- **Framework**: FastAPI (recommended) or Flask
- **AI Agents**: CrewAI (financial_planning, tax_planning modules)
- **PDF Generation**: `markdown-pdf`, `weasyprint`, or `pdfkit`
- **Storage**: Local filesystem (development) → S3 (production)
- **Database**: PostgreSQL or MongoDB for user data and report metadata

### Integrations
- **Pixpoc.ai**: Call management, analysis, transcripts, contact metadata
- **CrewAI**: Multi-agent financial analysis system
- **Ollama**: Local LLM for agents (mistral-nemo)

---

## File Storage Structure

```
FinanceBot/
├── reports/
│   ├── +919876543210/
│   │   ├── financial_plan_2025-11-28_143022.pdf
│   │   ├── tax_plan_2025-11-28_150015.pdf
│   │   └── metadata.json
│   ├── +919123456789/
│   │   ├── financial_plan_2025-11-27_120000.pdf
│   │   └── metadata.json
│   └── ...
```

**metadata.json** structure:
```json
{
  "phoneNumber": "+919876543210",
  "userId": "user_uuid",
  "reports": [
    {
      "id": "report_uuid",
      "type": "financial_planning",
      "filename": "financial_plan_2025-11-28_143022.pdf",
      "createdAt": "2025-11-28T14:30:22Z",
      "callId": "call-uuid",
      "size": 245678,
      "summary": {
        "netWorth": 450000,
        "savingsRate": 33.3,
        "topRecommendations": [
          "Build emergency fund",
          "Invest in ELSS",
          "Review insurance coverage"
        ]
      }
    }
  ]
}
```

---

## Environment Variables

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Backend (.env)
# Pixpoc Configuration
PIXPOC_API_BASE_URL=https://devcallmanager.pixpoc.in
PIXPOC_API_KEY=your_api_key_here
PIXPOC_WEBHOOK_SECRET=webhook_secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/financebot

# Storage
REPORTS_STORAGE_PATH=/path/to/reports
FILE_STORAGE_TYPE=local  # or 's3'
AWS_S3_BUCKET=financebot-reports  # if using S3

# AI Agents
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral-nemo

# Security
JWT_SECRET=your_jwt_secret
SESSION_TIMEOUT=86400  # 24 hours

# Feature Flags
ENABLE_REAL_OTP=false  # Set to true in production
OTP_PROVIDER=twilio    # or other provider
```

---

## Database Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Reports table
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    type VARCHAR(50) NOT NULL,  -- 'financial_planning', 'tax_planning', etc.
    file_path TEXT NOT NULL,
    file_size INTEGER,
    call_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'processing',  -- 'processing', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT NOW(),
    summary JSONB  -- Store key metrics
);

-- Pixpoc calls table
CREATE TABLE pixpoc_calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    call_id VARCHAR(255) UNIQUE NOT NULL,
    call_sid VARCHAR(255),
    contact_id VARCHAR(255),
    status VARCHAR(50),
    duration INTEGER,
    transcript TEXT,
    analysis JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User financial data table (extracted from calls)
CREATE TABLE user_financial_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) UNIQUE,
    income JSONB,
    expenses JSONB,
    assets JSONB,
    liabilities JSONB,
    goals JSONB,
    risk_profile VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_reports_user ON reports(user_id);
CREATE INDEX idx_calls_user ON pixpoc_calls(user_id);
CREATE INDEX idx_reports_created ON reports(created_at DESC);
```

---

## Implementation Phases

### Phase 1: Backend API Setup (Week 1)
- [ ] Set up FastAPI project structure
- [ ] Implement auth endpoints (OTP)
- [ ] Create Pixpoc API client wrapper
- [ ] Set up database and models
- [ ] Implement webhook endpoint for Pixpoc callbacks

### Phase 2: Agent Integration (Week 2)
- [ ] Integrate existing CrewAI agents
- [ ] Create data parser (Pixpoc → Agent format)
- [ ] Implement agent triggering logic
- [ ] Add error handling and logging

### Phase 3: Report Generation (Week 3)
- [ ] Implement MD to PDF conversion
- [ ] Set up file storage system
- [ ] Create report download endpoints
- [ ] Add report metadata management

### Phase 4: Frontend Integration (Week 4)
- [ ] Update dashboard to fetch real data
- [ ] Add report listing and download UI
- [ ] Implement call initiation flow
- [ ] Add loading states and error handling

### Phase 5: Testing & Optimization (Week 5)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Deploy to staging

---

## Security Considerations

1. **API Authentication**
   - Use JWT tokens for API authentication
   - Secure Pixpoc webhook with signature verification
   - Rate limiting on sensitive endpoints

2. **Data Privacy**
   - Encrypt sensitive financial data in database
   - Secure PDF storage with access controls
   - Implement user data deletion (GDPR compliance)

3. **File Access**
   - Signed URLs for report downloads
   - User can only access their own reports
   - Temporary download links with expiration

---

## Monitoring & Logging

```python
# Key metrics to track
- Call completion rate
- Agent processing time
- Report generation success rate
- Average user session duration
- API response times
- Error rates by endpoint

# Logging events
- User authentication attempts
- Call initiations
- Pixpoc callbacks received
- Agent processing start/end
- Report generation success/failure
- File downloads
```

---

## Next Steps

1. **Immediate**: Create backend API structure
2. **This week**: Implement Pixpoc integration
3. **Next week**: Connect CrewAI agents
4. **Following week**: MD to PDF conversion
5. **Final week**: Frontend integration and testing


