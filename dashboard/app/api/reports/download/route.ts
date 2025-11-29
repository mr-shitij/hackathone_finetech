import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const filePath = searchParams.get("path")
    const filename = searchParams.get("filename") || "report.pdf"

    if (!filePath) {
      return NextResponse.json(
        { error: "File path is required" },
        { status: 400 }
      )
    }

    // Call Python backend API to get the file
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000"
    
    try {
      const response = await fetch(
        `${backendUrl}/api/reports/download?path=${encodeURIComponent(filePath)}&filename=${encodeURIComponent(filename)}`,
        {
          method: "GET",
        }
      )

      if (response.ok) {
        // Get the file as a blob
        const blob = await response.blob()
        
        // Return the file with proper headers
        return new NextResponse(blob, {
          headers: {
            "Content-Type": "application/pdf",
            "Content-Disposition": `attachment; filename="${filename}"`,
          },
        })
      } else {
        return NextResponse.json(
          { error: "File not found" },
          { status: 404 }
        )
      }
    } catch (error: any) {
      console.error("Error fetching report file:", error)
      return NextResponse.json(
        { error: "Failed to download file" },
        { status: 500 }
      )
    }
  } catch (error: any) {
    console.error("Error in download route:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}

