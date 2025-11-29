import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { phone, name } = await request.json()

    if (!phone) {
      return NextResponse.json(
        { error: "Phone number required" },
        { status: 400 }
      )
    }

    // Get Pixpoc API credentials from environment
    const pixpocApiKey = process.env.PIXPOC_API_KEY
    const pixpocAgentId = process.env.PIXPOC_AGENT_ID
    const pixpocFromNumberId = process.env.PIXPOC_FROM_NUMBER_ID
    const pixpocBaseUrl = process.env.PIXPOC_API_BASE_URL || "https://app.pixpoc.ai"

    if (!pixpocApiKey || !pixpocAgentId) {
      return NextResponse.json(
        { error: "PIXPOC_API_KEY and PIXPOC_AGENT_ID must be configured in .env.local" },
        { status: 500 }
      )
    }

    // Format phone number to E.164 format
    let formattedPhone = phone.trim()
    if (!formattedPhone.startsWith('+')) {
      // Assume Indian number if no country code
      formattedPhone = formattedPhone.replace(/^0+/, '') // Remove leading zeros
      formattedPhone = `+91${formattedPhone}`
    }

    // Prepare Pixpoc API request payload
    const payload: any = {
      toNumber: formattedPhone,
      agentId: pixpocAgentId,
    }

    if (name) {
      payload.contactName = name
    }

    if (pixpocFromNumberId) {
      payload.fromNumberId = pixpocFromNumberId
    }

    // Call Pixpoc API directly
    try {
      const response = await fetch(`${pixpocBaseUrl}/api/v1/calls`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          "X-API-Key": pixpocApiKey,
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        // Extract call details from Pixpoc response
        const callData = data.data

        return NextResponse.json({
          success: true,
          message: "Call initiated successfully",
          call: {
            id: callData.call.id,
            trackingId: callData.call.trackingId,
            status: callData.call.status,
          },
          contact: callData.contact ? {
            id: callData.contact.id,
            name: name,
          } : null,
          campaign: callData.campaign ? {
            id: callData.campaign.id,
          } : null,
          phone: phone,
        })
      } else {
        // Handle Pixpoc API error
        const errorMessage = data.message || data.error || `Pixpoc API returned ${response.status}`
        return NextResponse.json(
          { 
            error: errorMessage,
            details: data,
          },
          { status: response.status || 500 }
        )
      }
    } catch (error: any) {
      console.error("Error calling Pixpoc API:", error)
      return NextResponse.json(
        { 
          error: `Failed to initiate call: ${error.message || "Unknown error"}`,
        },
        { status: 500 }
      )
    }
  } catch (error: any) {
    console.error("Error parsing request:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

