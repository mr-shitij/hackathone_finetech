"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Phone, ArrowLeft, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function LoginPage() {
  const router = useRouter()
  const [step, setStep] = useState<"phone" | "otp">("phone")
  const [phone, setPhone] = useState("+91")
  const [name, setName] = useState("")
  const [otp, setOtp] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const validatePhone = (phoneNum: string) => {
    if (!phoneNum.startsWith("+")) {
      return "Number must start with + (country code required)"
    }
    if (phoneNum.startsWith("+91")) {
      const digits = phoneNum.slice(3)
      if (digits.length < 10) {
        return `Need ${10 - digits.length} more digit(s)`
      }
      if (digits.length > 10) {
        return `Too many digits (remove ${digits.length - 10})`
      }
      if (!digits.match(/^\d+$/)) {
        return "Only numbers allowed after +91"
      }
    }
    return null
  }

  const handleSendOTP = async () => {
    setError("")
    
    if (!name || name.trim().length < 2) {
      setError("Please enter your full name")
      return
    }

    const phoneError = validatePhone(phone)
    if (phoneError) {
      setError(phoneError)
      return
    }

    setLoading(true)
    try {
      const response = await fetch("/api/auth/send-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, name: name.trim() }),
      })

      const data = await response.json()
      
      if (response.ok) {
        setStep("otp")
      } else {
        setError(data.error || "Failed to send OTP")
      }
    } catch (err) {
      setError("Network error. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async () => {
    setError("")
    
    if (otp.length !== 6) {
      setError("Please enter a 6-digit OTP")
      return
    }

    setLoading(true)
    try {
      const response = await fetch("/api/auth/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, otp, name }),
      })

      const data = await response.json()
      
      if (response.ok) {
        // Store user data in localStorage
        localStorage.setItem("user", JSON.stringify(data.user))
        localStorage.setItem("authenticated", "true")
        router.push("/")
      } else {
        setError(data.error || "Invalid OTP. Please try again.")
      }
    } catch (err) {
      setError("Network error. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-teal-400 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
          </div>
          <CardTitle className="text-2xl">🏦 FinanceBot</CardTitle>
          <CardDescription>Your AI-Powered Financial Advisor</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {step === "phone" ? (
            <>
              <div className="space-y-2">
                <Label htmlFor="name">Your Full Name</Label>
                <Input
                  id="name"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Mobile Number</Label>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4 text-muted-foreground" />
                  <Input
                    id="phone"
                    placeholder="+919876543210"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    maxLength={13}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Format: +91XXXXXXXXXX (10 digits after +91)
                </p>
                {phone && phone !== "+91" && (
                  <p className="text-xs">
                    {validatePhone(phone) ? (
                      <span className="text-red-500">❌ {validatePhone(phone)}</span>
                    ) : (
                      <span className="text-green-500">✅ Valid format</span>
                    )}
                  </p>
                )}
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <Button
                onClick={handleSendOTP}
                disabled={loading}
                className="w-full"
              >
                {loading ? "Sending..." : "📨 Send OTP"}
              </Button>
            </>
          ) : (
            <>
              <div className="space-y-2">
                <p className="text-sm">
                  <strong>Name:</strong> {name}
                </p>
                <p className="text-sm">
                  <strong>Mobile:</strong> {phone}
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="otp">Enter 6-digit OTP</Label>
                <Input
                  id="otp"
                  type="password"
                  placeholder="000000"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                  maxLength={6}
                />
                <p className="text-xs text-muted-foreground">
                  💡 Test OTP: <strong>222222</strong>
                </p>
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    setStep("phone")
                    setOtp("")
                    setError("")
                  }}
                  className="flex-1"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Button>
                <Button
                  onClick={handleVerifyOTP}
                  disabled={loading || otp.length !== 6}
                  className="flex-1"
                >
                  {loading ? "Verifying..." : "✅ Verify"}
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

