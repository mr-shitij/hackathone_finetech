"use client"

import { useEffect, useState } from "react"
import { AuthGuard } from "@/components/auth-guard"
import { DashboardHeader } from "@/components/dashboard/header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { Calculator, FileText, User, Home, Download } from "lucide-react"
import { Button } from "@/components/ui/button"
import { getUser } from "@/lib/auth"
import { useToast } from "@/hooks/use-toast"

interface Report {
  id: string
  type: string
  filename: string
  path: string
  date: string
  title: string
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState<string | null>(null)
  const { toast } = useToast()

  useEffect(() => {
    const fetchReports = async () => {
      const user = getUser()
      if (!user) {
        setLoading(false)
        return
      }

      try {
        const response = await fetch(`/api/reports?phone=${encodeURIComponent(user.phone)}`)
        if (response.ok) {
          const data = await response.json()
          console.log("Reports fetched:", data)
          setReports(data)
        } else {
          console.error("Failed to fetch reports:", response.status, response.statusText)
          toast({
            title: "Error",
            description: "Failed to load reports. Please try again.",
            variant: "destructive",
          })
        }
      } catch (error) {
        console.error("Failed to fetch reports:", error)
        toast({
          title: "Error",
          description: "Failed to load reports. Please try again.",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    fetchReports()
  }, [toast])

  const handleDownload = async (report: Report) => {
    try {
      setDownloading(report.id)
      const response = await fetch(
        `/api/reports/download?path=${encodeURIComponent(report.path)}&filename=${encodeURIComponent(report.filename)}`
      )

      if (!response.ok) {
        throw new Error("Failed to download file")
      }

      // Get the blob and create download link
      const blob = await response.blob()
      const url = globalThis.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = report.filename
      document.body.appendChild(a)
      a.click()
      globalThis.URL.revokeObjectURL(url)
      a.remove()

      toast({
        title: "Success",
        description: "Report downloaded successfully",
      })
    } catch (error) {
      console.error("Download error:", error)
      toast({
        title: "Error",
        description: "Failed to download report. Please try again.",
        variant: "destructive",
      })
    } finally {
      setDownloading(null)
    }
  }

  // Filter reports by type - comprehensive_planning is treated as financial
  const financialReports = reports.filter((r) => 
    r.type?.includes("financial") || r.type?.includes("comprehensive")
  )
  const taxReports = reports.filter((r) => r.type?.includes("tax"))
  const otherReports = reports.filter((r) => 
    !r.type?.includes("financial") && 
    !r.type?.includes("tax") && 
    !r.type?.includes("comprehensive")
  )

  return (
    <AuthGuard>
      <div className="min-h-screen bg-background p-4 lg:p-6">
        <div className="mx-auto max-w-7xl">
          <DashboardHeader />

          {/* Navigation */}
          <div className="mt-4 mb-6 flex gap-2">
            <Link href="/">
              <Button variant="ghost" size="sm">
                <Home className="w-4 h-4 mr-2" />
                Dashboard
              </Button>
            </Link>
            <Link href="/calculators">
              <Button variant="ghost" size="sm">
                <Calculator className="w-4 h-4 mr-2" />
                Calculators
              </Button>
            </Link>
            <Link href="/reports">
              <Button variant="default" size="sm">
                <FileText className="w-4 h-4 mr-2" />
                Reports
              </Button>
            </Link>
            <Link href="/profile">
              <Button variant="ghost" size="sm">
                <User className="w-4 h-4 mr-2" />
                Profile
              </Button>
            </Link>
          </div>

          <h1 className="text-3xl font-bold mb-6">📄 Your Financial Reports</h1>
          <p className="text-muted-foreground mb-8">
            Download and view your personalized financial reports
          </p>

          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading reports...</p>
            </div>
          ) : reports.length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <p className="text-muted-foreground mb-4">📭 No reports yet.</p>
                <p className="text-sm text-muted-foreground mb-4">
                  Generate your first report from the Dashboard!
                </p>
                <Link href="/">
                  <Button>Go to Dashboard</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-8">
              {financialReports.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">💼 Financial Planning Reports</h2>
                  <div className="space-y-4">
                    {financialReports.map((report) => (
                      <Card key={report.id}>
                        <CardContent className="p-6">
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <h3 className="font-semibold mb-1">{report.title}</h3>
                              <p className="text-sm text-muted-foreground">
                                📅 {new Date(report.date).toLocaleDateString()}
                              </p>
                            </div>
                            <Button
                              variant="outline"
                              onClick={() => handleDownload(report)}
                              disabled={downloading === report.id}
                            >
                              <Download className="w-4 h-4 mr-2" />
                              {downloading === report.id ? "Downloading..." : "Download"}
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {taxReports.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">💰 Tax Planning Reports</h2>
                  <div className="space-y-4">
                    {taxReports.map((report) => (
                      <Card key={report.id}>
                        <CardContent className="p-6">
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <h3 className="font-semibold mb-1">{report.title}</h3>
                              <p className="text-sm text-muted-foreground">
                                📅 {new Date(report.date).toLocaleDateString()}
                              </p>
                            </div>
                            <Button
                              variant="outline"
                              onClick={() => handleDownload(report)}
                              disabled={downloading === report.id}
                            >
                              <Download className="w-4 h-4 mr-2" />
                              {downloading === report.id ? "Downloading..." : "Download"}
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {otherReports.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">📋 Other Reports</h2>
                  <div className="space-y-4">
                    {otherReports.map((report) => (
                      <Card key={report.id}>
                        <CardContent className="p-6">
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <h3 className="font-semibold mb-1">{report.title}</h3>
                              <p className="text-sm text-muted-foreground">
                                📅 {new Date(report.date).toLocaleDateString()}
                              </p>
                            </div>
                            <Button
                              variant="outline"
                              onClick={() => handleDownload(report)}
                              disabled={downloading === report.id}
                            >
                              <Download className="w-4 h-4 mr-2" />
                              {downloading === report.id ? "Downloading..." : "Download"}
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              <Card>
                <CardHeader>
                  <CardTitle>📊 Report Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-blue-500/10 rounded-lg">
                      <p className="text-2xl font-bold">{reports.length}</p>
                      <p className="text-sm text-muted-foreground">Total Reports</p>
                    </div>
                    <div className="text-center p-4 bg-green-500/10 rounded-lg">
                      <p className="text-2xl font-bold">{financialReports.length}</p>
                      <p className="text-sm text-muted-foreground">Financial Plans</p>
                    </div>
                    <div className="text-center p-4 bg-purple-500/10 rounded-lg">
                      <p className="text-2xl font-bold">{taxReports.length}</p>
                      <p className="text-sm text-muted-foreground">Tax Plans</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </AuthGuard>
  )
}

