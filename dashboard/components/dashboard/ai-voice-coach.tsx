"use client"

import { useState, useEffect } from "react"
import { Phone, Calendar, MessageSquare, Play, Loader2 } from "lucide-react"
import { getUser } from "@/lib/auth"
import { useToast } from "@/hooks/use-toast"

export function AIVoiceCoach() {
  const [user, setUser] = useState<{ phone: string; name: string } | null>(null)
  const [loading, setLoading] = useState(false)
  const [callInitiated, setCallInitiated] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    setUser(getUser())
  }, [])

  const handleStartCall = async () => {
    if (!user) {
      toast({
        title: "Error",
        description: "User not found. Please login again.",
        variant: "destructive",
      })
      return
    }

    setLoading(true)
    try {
      const response = await fetch("/api/calls/initiate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: user.phone, name: user.name }),
      })

      let data
      try {
        data = await response.json()
      } catch (parseError) {
        // Response is not JSON
        const text = await response.text()
        console.error("Non-JSON response:", text)
        toast({
          title: "Error",
          description: `Server error: ${response.status} ${response.statusText}`,
          variant: "destructive",
        })
        setLoading(false)
        return
      }

      if (response.ok) {
        setCallInitiated(true)
        toast({
          title: "Call Initiated",
          description: `Call started successfully! You will receive a call shortly.`,
        })
      } else {
        // Handle error response
        const errorMsg = data?.error || data?.detail || data?.message || `Failed to initiate call (${response.status})`
        toast({
          title: "Error",
          description: errorMsg,
          variant: "destructive",
        })
        console.error("Call initiation error:", {
          status: response.status,
          statusText: response.statusText,
          data: data,
          response: response
        })
      }
    } catch (error: any) {
      console.error("Network error:", error)
      toast({
        title: "Error",
        description: error?.message || "Network error. Please ensure the backend server is running on port 8000.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-card rounded-xl p-5 glow-purple">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-2 rounded-lg bg-gradient-to-br from-purple-500/20 to-pink-500/20">
          <Phone className="w-4 h-4 text-purple-400" />
        </div>
        <h3 className="font-semibold text-foreground">AI Voice Coach</h3>
      </div>

      <div className="space-y-4">
        {callInitiated ? (
          <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20">
            <div className="flex items-center gap-2 mb-2">
              <Phone className="w-4 h-4 text-green-400" />
              <span className="text-xs text-muted-foreground">Call Status</span>
            </div>
            <p className="text-sm font-medium text-foreground">Call initiated successfully!</p>
            <p className="text-xs text-muted-foreground mt-1">
              You will receive a call shortly from our AI financial advisor.
            </p>
          </div>
        ) : (
          <>
            <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-purple-400" />
                <span className="text-xs text-muted-foreground">Get Personalized Advice</span>
              </div>
              <p className="text-sm font-medium text-foreground">Start an AI call now</p>
              <p className="text-xs text-muted-foreground mt-1">
                Talk to our AI financial advisor and receive personalized recommendations
              </p>
            </div>

            <div className="p-3 rounded-lg bg-secondary/30">
              <div className="flex items-center gap-2 mb-2">
                <MessageSquare className="w-4 h-4 text-teal-400" />
                <span className="text-xs text-muted-foreground">What to expect</span>
              </div>
              <p className="text-sm text-foreground/90 leading-relaxed">
                The AI will ask about your income, expenses, goals, and risk tolerance to create a personalized financial plan.
              </p>
            </div>
          </>
        )}

        <button
          onClick={handleStartCall}
          disabled={loading || callInitiated}
          className="w-full p-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center gap-2 hover:opacity-90 transition-opacity group disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 text-white animate-spin" />
              <span className="text-sm font-medium text-white">Initiating...</span>
            </>
          ) : callInitiated ? (
            <>
              <Phone className="w-4 h-4 text-white" />
              <span className="text-sm font-medium text-white">Call Initiated</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 text-white group-hover:scale-110 transition-transform" />
              <span className="text-sm font-medium text-white">Start AI Call</span>
            </>
          )}
        </button>
      </div>
    </div>
  )
}
