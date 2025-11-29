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
      const response = await fetch(`${backendUrl}/api/financial-data?phone=${encodeURIComponent(phone)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (response.ok) {
        const data = await response.json()
        return NextResponse.json(data)
      } else {
        // Return default data if backend is not available
        return NextResponse.json({
          income: 75000,
          savings: 25000,
          expenses: 50000,
          savingsRate: 33.3,
          data: {},
        })
      }
    } catch (error) {
      // Return default data if backend is not available
      return NextResponse.json({
        income: 75000,
        savings: 25000,
        expenses: 50000,
        savingsRate: 33.3,
        data: {},
      })
    }
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

