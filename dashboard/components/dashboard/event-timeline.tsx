"use client"

import { AlertTriangle, TrendingUp, Wallet, CreditCard, Bell } from "lucide-react"

const events = [
  {
    time: "Today, 2:30 PM",
    title: "High Spend Detected",
    description: "₹8,500 spent in last 24 hours",
    icon: TrendingUp,
    color: "bg-yellow-500",
    iconColor: "text-yellow-400",
  },
  {
    time: "Today, 9:05 AM",
    title: "Payday Detected",
    description: "Salary ₹45,200 credited",
    icon: Wallet,
    color: "bg-green-500",
    iconColor: "text-green-400",
  },
  {
    time: "Yesterday, 6:15 PM",
    title: "Unexpected Debit",
    description: "Amazon ₹2,499 - flagged",
    icon: CreditCard,
    color: "bg-purple-500",
    iconColor: "text-purple-400",
  },
  {
    time: "Jan 22, 11:00 AM",
    title: "Low Balance Warning",
    description: "HDFC dropped below ₹10k",
    icon: AlertTriangle,
    color: "bg-red-500",
    iconColor: "text-red-400",
  },
  {
    time: "Jan 20, 3:45 PM",
    title: "AI Alert",
    description: "Spending pattern changed",
    icon: Bell,
    color: "bg-blue-500",
    iconColor: "text-blue-400",
  },
]

export function EventTimeline() {
  return (
    <div className="glass-card rounded-xl p-5">
      <h3 className="text-lg font-semibold text-foreground mb-4">Event Timeline</h3>

      <div className="relative">
        <div className="absolute left-[11px] top-2 bottom-2 w-0.5 bg-gradient-to-b from-blue-500 via-purple-500 to-teal-500 opacity-30" />

        <div className="space-y-4">
          {events.map((event, index) => (
            <div key={index} className="flex gap-4 relative">
              <div
                className={`w-6 h-6 rounded-full ${event.color} flex items-center justify-center shrink-0 z-10 shadow-lg`}
              >
                <event.icon className="w-3 h-3 text-white" />
              </div>
              <div className="flex-1 pb-4">
                <p className="text-xs text-muted-foreground">{event.time}</p>
                <p className="text-sm font-medium text-foreground mt-1">{event.title}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{event.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button className="w-full mt-2 p-2 rounded-lg bg-secondary/30 text-xs text-muted-foreground hover:bg-secondary/50 transition-colors">
        View Full History
      </button>
    </div>
  )
}
