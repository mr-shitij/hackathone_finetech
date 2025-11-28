# V1 API - Initiate Single Call

This guide explains how to initiate a single phone call using the Call Manager V1 API with API key authentication.

## Overview

The V1 API endpoint allows external systems to programmatically initiate individual phone calls. Each call uses an AI agent configuration to handle the conversation automatically.

**Endpoint**: `POST /api/v1/calls`  
**Authentication**: API Key (required)  
**Content-Type**: `application/json`

## Authentication

The V1 API requires an API key for authentication. You can provide the API key in one of three ways:

### Method 1: Header (Recommended)
```http
X-API-Key: cm_your_api_key_here
```

### Method 2: Authorization Header
```http
Authorization: Bearer cm_your_api_key_here
```

### Method 3: Query Parameter
```
POST /api/v1/calls?api_key=cm_your_api_key_here
```

**Note**: The API key format is `cm_` followed by a 64-character hexadecimal string (e.g., `cm_abc123...`).

## Request Format

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `toNumber` | string | Phone number to call in E.164 format (e.g., `+1234567890`) |
| `agentId` | string (UUID) | ID of the AI agent to use for this call. Agent must be approved and owned by your account. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `contactName` | string | Name of the contact being called (for personalization) |
| `contactData` | object | Additional contact data as key-value pairs. These can be used in agent prompts via variables. |
| `fromNumberId` | string (UUID) | Specific phone number to use as the caller ID. If not provided, uses the agent's default from number. |

### Request Schema

```json
{
  "toNumber": "+1234567890",
  "agentId": "uuid-of-agent",
  "contactName": "John Doe",
  "contactData": {
    "company": "Acme Corp",
    "department": "Sales",
    "customField": "customValue"
  },
  "fromNumberId": "uuid-of-from-number"
}
```

## Response Format

### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "call": {
      "id": "call-uuid",
      "callSid": "tracking-id",
      "trackingId": "tracking-id",
      "status": "INITIATED",
      "campaignId": "temp-campaign-id",
      "contactId": "contact-uuid",
      "agentId": "agent-uuid",
      "startTime": "2024-01-01T12:00:00.000Z",
      "creditsUsed": 5,
      "toNumber": "+1234567890",
      "contactName": "John Doe"
    },
    "contact": {
      "id": "contact-uuid",
      "phoneNumber": "+1234567890",
      "additionalData": {
        "name": "John Doe",
        "company": "Acme Corp",
        "department": "Sales"
      }
    },
    "campaign": {
      "id": "temp-campaign-id",
      "name": "API Single Call - John Doe",
      "status": "ACTIVE"
    },
    "message": "Call initiated successfully"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `call.id` | string (UUID) | Unique identifier for the call record |
| `call.callSid` | string | Call tracking ID from the telephony provider |
| `call.trackingId` | string | Internal tracking ID for the call |
| `call.status` | string | Current call status (`INITIATED`, `RINGING`, `ANSWERED`, `COMPLETED`, `FAILED`, `BUSY`, `NO_ANSWER`) |
| `call.campaignId` | string | ID of the temporary campaign created for this call |
| `call.contactId` | string | ID of the contact record |
| `call.agentId` | string | ID of the agent used for this call |
| `call.startTime` | string (ISO 8601) | Timestamp when the call was initiated |
| `call.creditsUsed` | number | Number of credits reserved for this call (based on agent's max duration) |
| `call.toNumber` | string | Phone number that was called |
| `call.contactName` | string | Name of the contact (if provided) |

## Examples

### cURL

```bash
curl -X POST https://devcallmanager.pixpoc.in/api/v1/calls \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cm_your_api_key_here" \
  -d '{
    "toNumber": "+1234567890",
    "agentId": "550e8400-e29b-41d4-a716-446655440000",
    "contactName": "John Doe",
    "contactData": {
      "company": "Acme Corp",
      "department": "Sales"
    }
  }'
```

### JavaScript (Fetch API)

```javascript
const response = await fetch('https://devcallmanager.pixpoc.in/api/v1/calls', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'cm_your_api_key_here'
  },
  body: JSON.stringify({
    toNumber: '+1234567890',
    agentId: '550e8400-e29b-41d4-a716-446655440000',
    contactName: 'John Doe',
    contactData: {
      company: 'Acme Corp',
      department: 'Sales'
    }
  })
});

const data = await response.json();
console.log(data);
```

### Python (requests)

```python
import requests

url = 'https://devcallmanager.pixpoc.in/api/v1/calls'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'cm_your_api_key_here'
}
payload = {
    'toNumber': '+1234567890',
    'agentId': '550e8400-e29b-41d4-a716-446655440000',
    'contactName': 'John Doe',
    'contactData': {
        'company': 'Acme Corp',
        'department': 'Sales'
    }
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)
```

### Node.js (axios)

```javascript
const axios = require('axios');

const response = await axios.post(
  'https://devcallmanager.pixpoc.in/api/v1/calls',
  {
    toNumber: '+1234567890',
    agentId: '550e8400-e29b-41d4-a716-446655440000',
    contactName: 'John Doe',
    contactData: {
      company: 'Acme Corp',
      department: 'Sales'
    }
  },
  {
    headers: {
      'X-API-Key': 'cm_your_api_key_here'
    }
  }
);

console.log(response.data);
```

## Error Responses

### 400 Bad Request - Invalid Request Body

```json
{
  "success": false,
  "error": "Invalid request body",
  "issues": {
    "toNumber": ["Invalid phone number format. Please use international format (e.g., +1234567890)."],
    "agentId": ["Invalid Agent ID format"]
  }
}
```

### 401 Unauthorized - Missing or Invalid API Key

```json
{
  "success": false,
  "error": "Authentication required",
  "message": "API key is required. Please provide it in the x-api-key header, Authorization header, or api_key query parameter."
}
```

```json
{
  "success": false,
  "error": "Invalid API key",
  "message": "The provided API key is invalid or inactive."
}
```

### 402 Payment Required - Insufficient Credits

```json
{
  "success": false,
  "error": "Insufficient credits",
  "details": {
    "required": 5,
    "available": 2,
    "deficit": 3
  }
}
```

### 404 Not Found - Agent Not Found

```json
{
  "success": false,
  "error": "Agent not found, not owned by user, or not approved"
}
```

### 500 Internal Server Error - Call Initiation Failed

```json
{
  "success": false,
  "error": "Failed to initiate call",
  "details": "Error message from telephony provider"
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Call initiated successfully |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing or invalid API key) |
| 402 | Payment required (insufficient credits) |
| 404 | Not found (agent or from number not found) |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

## Important Notes

### Credit Deduction

- Credits are **reserved immediately** when a call is initiated
- The amount reserved is based on the agent's `maxDurationSeconds` (rounded up to minutes)
- If the call fails to initiate, credits are not deducted
- Actual credits used are calculated after the call completes based on actual duration

### Agent Requirements

- The agent must be **approved** (`status: 'APPROVED'`)
- The agent must be **owned by your account** (user-scoped)
- The agent must have a default `fromNumber` OR you must provide `fromNumberId`

### Phone Number Format

- Phone numbers must be in **E.164 international format**
- Must start with `+` followed by country code and number
- Example: `+1234567890` (US), `+919876543210` (India)

### Contact Data

- `contactData` can contain any key-value pairs
- These values can be used in agent prompts via variables (e.g., `{{company}}`, `{{department}}`)
- Contact data is stored with the contact record for future reference

### Temporary Campaigns

- Each API-initiated call creates a temporary campaign
- Campaigns are named: `API Single Call - {contactName or toNumber}`
- These campaigns are used for tracking and analytics
- Campaigns are automatically cleaned up if call initiation fails

### Call Status Lifecycle

1. **INITIATED** - Call request received and queued
2. **RINGING** - Phone is ringing
3. **ANSWERED** - Call was answered
4. **COMPLETED** - Call finished successfully
5. **FAILED** - Call failed (various reasons)
6. **BUSY** - Line was busy
7. **NO_ANSWER** - Call was not answered

## Best Practices

1. **Store the `call.id`** - Use this to track call status and retrieve call details later
2. **Handle errors gracefully** - Check for 402 (insufficient credits) and 404 (agent not found) errors
3. **Validate phone numbers** - Ensure phone numbers are in E.164 format before sending
4. **Use contactData for personalization** - Pass relevant data that can be used in agent prompts
5. **Monitor credit balance** - Check your account credits before initiating calls
6. **Implement retry logic** - For transient errors (500, 429), implement exponential backoff

## Related Endpoints

- `GET /api/v1/calls` - Get call history
- `GET /api/v1/calls/{callId}` - Get call details
- `GET /api/v1/calls/{callId}/transcript` - Get call transcript
- `GET /api/v1/calls/{callId}/analysis` - Get call analysis
- `GET /api/v1/account` - Get account information
- `GET /api/v1/account/usage` - Get usage statistics

## Support

For API support and questions:
- Base URL: `https://devcallmanager.pixpoc.in`
- API Documentation: See `/api-docs` endpoint
- Contact: See your account dashboard for support information

