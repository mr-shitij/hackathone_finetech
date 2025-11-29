"use client"

import { AlertTriangle, TrendingUp, Calendar, Wallet } from "lucide-react"

const risks = [
  {
    title: "Low Balance Alert",
    description: "Savings account may drop below ₹5,000",
    icon: Wallet,
    severity: "high",
    time: "Expected in 3 days",
  },
  {
    title: "High Spend Spike",
    description: "Unusual spending detected this week",
    icon: TrendingUp,
    severity: "medium",
    time: "₹8,500 above normal",
  },
  {
    title: "EMI Due",
    description: "Home loan EMI payment pending",
    icon: Calendar,
    severity: "low",
    time: "Due on 15th Jan",
  },
]

const severityColors = {
  high: { bg: "bg-red-500/10", border: "border-red-500/30", icon: "text-red-400", glow: "shadow-red-500/20" },
  medium: {
    bg: "bg-yellow-500/10",
    border: "border-yellow-500/30",
    icon: "text-yellow-400",
    glow: "shadow-yellow-500/20",
  },
  low: { bg: "bg-blue-500/10", border: "border-blue-500/30", icon: "text-blue-400", glow: "shadow-blue-500/20" },
}

export function UpcomingRisks() {
  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-yellow-400" />
        <h3 className="text-lg font-semibold text-foreground">Upcoming Risks</h3>
      </div>

      <div className="space-y-3">
        {risks.map((risk, index) => {
          const colors = severityColors[risk.severity as keyof typeof severityColors]
          return (
            <div
              key={index}
              className={`p-4 rounded-xl ${colors.bg} border ${colors.border} shadow-lg ${colors.glow} transition-all hover:scale-[1.02]`}
            >
              <div className="flex items-start gap-3">
                <div className={`p-2 rounded-lg ${colors.bg}`}>
                  <risk.icon className={`w-4 h-4 ${colors.icon}`} />
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-foreground">{risk.title}</h4>
                  <p className="text-xs text-muted-foreground mt-0.5">{risk.description}</p>
                  <p className={`text-xs mt-2 ${colors.icon}`}>{risk.time}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
