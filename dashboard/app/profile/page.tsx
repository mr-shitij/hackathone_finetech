"use client"

import { useEffect, useState } from "react"
import { AuthGuard } from "@/components/auth-guard"
import { DashboardHeader } from "@/components/dashboard/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import Link from "next/link"
import { Calculator, FileText, User, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { getUser, setUser } from "@/lib/auth"
import { useToast } from "@/hooks/use-toast"

export default function ProfilePage() {
  const [user, setUserState] = useState<{ phone: string; name: string } | null>(null)
  const [email, setEmail] = useState("")
  const [language, setLanguage] = useState("English")
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [whatsappUpdates, setWhatsappUpdates] = useState(true)
  const [weeklySummary, setWeeklySummary] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    const currentUser = getUser()
    setUserState(currentUser)
  }, [])

  const handleSave = () => {
    if (user) {
      setUser({ ...user, name: user.name })
      toast({
        title: "Profile Updated",
        description: "Your profile has been updated successfully!",
      })
    }
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-background p-4 lg:p-6">
        <div className="mx-auto max-w-4xl">
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
              <Button variant="ghost" size="sm">
                <FileText className="w-4 h-4 mr-2" />
                Reports
              </Button>
            </Link>
            <Link href="/profile">
              <Button variant="default" size="sm">
                <User className="w-4 h-4 mr-2" />
                Profile
              </Button>
            </Link>
          </div>

          <h1 className="text-3xl font-bold mb-6">👤 Profile</h1>
          <p className="text-muted-foreground mb-8">Manage your account and preferences</p>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>📱 Account Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Phone Number</Label>
                    <Input value={user?.phone || ""} disabled />
                  </div>
                  <div className="space-y-2">
                    <Label>Name</Label>
                    <Input
                      value={user?.name || ""}
                      onChange={(e) =>
                        setUserState(user ? { ...user, name: e.target.value } : null)
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Email</Label>
                    <Input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="your.email@example.com"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Preferred Language</Label>
                    <Select value={language} onValueChange={setLanguage}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="English">English</SelectItem>
                        <SelectItem value="Hindi">Hindi</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <Button onClick={handleSave}>💾 Save Changes</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>⚙️ Preferences</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>📧 Email notifications</Label>
                    <p className="text-sm text-muted-foreground">
                      Receive updates via email
                    </p>
                  </div>
                  <Switch checked={emailNotifications} onCheckedChange={setEmailNotifications} />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <Label>💬 WhatsApp updates</Label>
                    <p className="text-sm text-muted-foreground">
                      Get updates on WhatsApp
                    </p>
                  </div>
                  <Switch checked={whatsappUpdates} onCheckedChange={setWhatsappUpdates} />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <Label>📊 Weekly financial summary</Label>
                    <p className="text-sm text-muted-foreground">
                      Receive weekly summaries
                    </p>
                  </div>
                  <Switch checked={weeklySummary} onCheckedChange={setWeeklySummary} />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>ℹ️ About FinanceBot</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  <strong>FinanceBot</strong> is an AI-powered financial advisory platform designed
                  to provide personalized financial planning, tax optimization, and investment
                  guidance.
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>🤖 Powered by advanced AI agents</li>
                  <li>📞 Voice-based data collection</li>
                  <li>📄 Personalized PDF reports</li>
                  <li>🔒 Secure and private</li>
                </ul>
                <p className="text-xs text-muted-foreground mt-4">Version: 1.0.0</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}

