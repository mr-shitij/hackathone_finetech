import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    const phone = request.headers.get("x-phone") || request.nextUrl.searchParams.get("phone")

    if (!phone) {
      return NextResponse.json(
        { error: "Phone number required" },
        { status: 400 }
      )
    }

    // Call Python backend API
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000"
    
    try {
      const response = await fetch(`${backendUrl}/api/reports?phone=${encodeURIComponent(phone)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (response.ok) {
        const data = await response.json()
        // Backend returns array directly, or wrapped in {reports: [...]}
        // Handle both cases
        if (Array.isArray(data)) {
          return NextResponse.json(data)
        } else if (data.reports && Array.isArray(data.reports)) {
          return NextResponse.json(data.reports)
        } else {
          return NextResponse.json([])
        }
      } else {
        return NextResponse.json([])
      }
    } catch (error) {
      return NextResponse.json([])
    }
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

