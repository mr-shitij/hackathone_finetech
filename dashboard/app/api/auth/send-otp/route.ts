import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { phone, name } = await request.json()

    // Validate phone number
    if (!phone || !phone.startsWith("+")) {
      return NextResponse.json(
        { error: "Phone number must start with + (country code required)" },
        { status: 400 }
      )
    }

    if (phone.startsWith("+91")) {
      const digits = phone.slice(3)
      if (digits.length !== 10 || !digits.match(/^\d+$/)) {
        return NextResponse.json(
          { error: "Invalid phone number format. Use: +91XXXXXXXXXX (10 digits)" },
          { status: 400 }
        )
      }
    }

    if (!name || name.trim().length < 2) {
      return NextResponse.json(
        { error: "Please enter your full name" },
        { status: 400 }
      )
    }

    // In a real app, you would send OTP via SMS service
    // For now, we just return success (OTP is always 222222 for testing)
    return NextResponse.json({
      success: true,
      message: `OTP sent to ${phone}`,
      testOtp: "222222", // For development
    })
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

