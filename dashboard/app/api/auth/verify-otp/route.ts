import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { phone, otp, name } = await request.json()

    // Validate OTP (for testing, accept 222222)
    if (otp !== "222222") {
      return NextResponse.json(
        { error: "Invalid OTP. Please try again." },
        { status: 400 }
      )
    }

    // In a real app, verify OTP with backend service
    // For now, we just authenticate the user
    return NextResponse.json({
      success: true,
      user: {
        phone,
        name: name || "User",
      },
    })
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

