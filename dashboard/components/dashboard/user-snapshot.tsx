"use client"

import { useEffect, useState } from "react"
import { TrendingUp, Shield, Activity } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { getUser } from "@/lib/auth"

export function UserSnapshot() {
  const [user, setUser] = useState<{ phone: string; name: string } | null>(null)
  const riskScore = 72
  const stabilityScore = 65

  useEffect(() => {
    setUser(getUser())
  }, [])

  const initials = user?.name
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "U"

  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center gap-4 mb-5">
        <Avatar className="w-14 h-14 ring-2 ring-blue-500/40 glow-blue">
          <AvatarImage src="/indian-professional-man-portrait.png" />
          <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-500 text-white">
            {initials}
          </AvatarFallback>
        </Avatar>
        <div>
          <h3 className="font-semibold text-foreground">{user?.name || "User"}</h3>
          <p className="text-xs text-muted-foreground">Premium Member</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between p-3 bg-secondary/30 rounded-lg">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-yellow-400" />
            <span className="text-sm text-muted-foreground">Income Pattern</span>
          </div>
          <span className="text-sm font-medium text-yellow-400">Irregular Earner</span>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-muted-foreground">Risk Score</span>
            </div>
            <span className="text-sm font-bold text-blue-400 neon-text-blue">{riskScore}/100</span>
          </div>
          <div className="h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-teal-400 rounded-full transition-all duration-500"
              style={{ width: `${riskScore}%` }}
            />
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-teal-400" />
              <span className="text-sm text-muted-foreground">Stability Meter</span>
            </div>
            <span className="text-sm font-bold text-teal-400 neon-text-teal">{stabilityScore}%</span>
          </div>
          <div className="h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-teal-500 to-green-400 rounded-full transition-all duration-500"
              style={{ width: `${stabilityScore}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-2">
          <div className="text-center p-3 bg-secondary/20 rounded-lg">
            <p className="text-lg font-bold text-foreground">₹45,200</p>
            <p className="text-xs text-muted-foreground">Avg. Monthly</p>
          </div>
          <div className="text-center p-3 bg-secondary/20 rounded-lg">
            <p className="text-lg font-bold text-foreground">8</p>
            <p className="text-xs text-muted-foreground">Active Accounts</p>
          </div>
        </div>
      </div>
    </div>
  )
}
